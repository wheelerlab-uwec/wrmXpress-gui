########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, DiskcacheManager
from dash.dependencies import Input, Output, State
import time
from pathlib import Path
import os
import subprocess
import shlex
import pandas as pd
import re

# Importing Components
from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header
from app.utils.callback_functions import clean_and_create_directories, copy_files_to_input_directory, create_figure_from_filepath, update_yaml_file

# importing utils
from app.utils.styling import layout

# Diskcache
import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__,
           long_callback_manager=background_callback_manager,
           use_pages=True,
           pages_folder='app/pages',
           external_stylesheets=[
               dbc.themes.FLATLY,
               dbc.icons.FONT_AWESOME],
           suppress_callback_exceptions=True)

########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

sidebar = html.Div(
    [
        html.A(
            html.Img(src='https://github.com/zamanianlab/wrmXpress/blob/main/img/logo/output.png?raw=true',  # wrmXpress image
                     height="200px"),

            # clicked takes user to wrmXpress github
            href="https://github.com/zamanianlab/wrmxpress",
            style={"textDecoration": "none"},
            className='ms-3'
        ),
        html.Hr(),
        html.Div([
            dbc.Nav(
                children=dbc.NavLink(
                    # Page name
                    f"{page['name']}",
                    href=page["relative_path"],  # Page path
                    active='exact'
                ),
                pills=True,  # Style of the navigation
                vertical=True  # Style of the navigation
            ) for page in dash.page_registry.values()  # Iterate through each page
        ])
    ],
    style=SIDEBAR_STYLE  # Style of the sidebar, see styling.py
)

app.layout = html.Div([
    dcc.Store(id='store', data={}),  # Store data
    sidebar,  # Sidebar see above
    html.Div(
        id="page-content",
        children=[
            header,  # Header see header.py
            dash.page_container  # Page container, see app/pages/
        ],
        style=CONTENT_STYLE  # Style of the content, see styling.py
    )])

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@app.callback(
    output=[
        Output("image-analysis-preview", "figure"),
        Output('load-analysis-img', 'disabled'),
        Output("run-page-alert", 'is_open'),
        Output("run-page-alert", 'children'),
        Output("progress-message-run-page-markdown", "children"),
    ],
    inputs=[
        Input("submit-analysis", "n_clicks"),
        State("store", "data"),
    ],
    running=[
        (
            Output("submit-analysis", "disabled"), True, False
        ),
        (
            Output("cancel-analysis", "disabled"), False, True
        ),
        (
            Output("image-analysis-preview", "style"),
            {"visibility": "visible"},
            {"visibility": "visible"}
        ),
        (
            Output("progress-bar-run-page", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"}
        ),
        (
            Output("progress-message-run-page-for-analysis", "style"),
            {'visibility': 'visible'},
            {'visibility': 'hidden'}
        ),
    ],

    cancel=[
        Input("cancel-analysis", "n_clicks")
    ],
    progress=[
        Output("progress-bar-run-page", "value"),
        Output("progress-bar-run-page", "max"),
        Output("image-analysis-preview", "figure"),
        Output("progress-message-run-page-for-analysis", "children"),
        Output("progress-message-run-page-markdown", "children"),
    ],
    prevent_initial_call=True,
    allow_duplicate=True,
    background=True
)
def callback(set_progress, n_clicks, store):
    """
    This function runs the analysis on the wrmXpress container
    ===============================================================================
    Arguments:
        - set_progress : function : A function that sets the progress of the analysis        
        - n_clicks : int : The number of times the submit button has been clicked
        - store : dict : A dictionary containing the data from the store
    ===============================================================================
    Returns:
        - fig_1 : plotly.graph_objs._figure.Figure : A figure showing the analysis
        - disabled : bool : A boolean value indicating whether the load button is disabled
            +- True : The load button is disabled
            +- False : The load button is not disabled
        - is_open : bool : A boolean value indicating whether the alert is open
            +- True : The alert is open
            +- False : The alert is not open
        - children : str : A string containing the alert message
    ===============================================================================
    Runnning:
        - submit-analysis : disabeled : A boolean value indicating whether the submit button has been disabeled
            +- True : The submit button has been disabeled
            +- False : The submit button has not been disabeled
        - cancel-analysis : disabeled : A boolean value indicating whether the cancel button has been disabeled
            +- True : The cancel button has been disabeled
            +- False : The cancel button has not been disabeled
        - image-analysis-preview : style : A dictionary containing the style of the image analysis preview
            +- {'visibility': 'visible'} : The image analysis preview is visible
            +- {'visibility': 'hidden'} : The image analysis preview is hidden
        - progress-bar-run-page : style : A dictionary containing the style of the progress bar
            +- {'visibility': 'visible'} : The progress bar is visible
            +- {'visibility': 'hidden'} : The progress bar is hidden
    ===============================================================================
    Cancel:
        - cancel-analysis : n_clicks : The number of times the cancel button has been clicked
            +- will cancel the analysis upon a single click
    ===============================================================================
    Progress:
        - progress-bar-run-page : value : The value of the progress bar
        - progress-bar-run-page : max : The maximum value of the progress bar
        - image-analysis-preview : figure : A figure showing the analysis
        - progress-message-run-page-for-analysis : children : A string containing the progress message
    ===============================================================================
    """
    # Check if store is empty
    if not store:
        return None, True, True, "No configuration found. Please go to the configuration page to set up the analysis.", "No configuration found. Please go to the configuration page to set up the analysis."

    # obtain the necessary data from the store
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    motility = store["motility"]
    segment = store["segment"]
    cellprofiler = store["cellprofiler"]
    cellprofilepipeline = store["cellprofilepipeline"]
    # Check if the submit button has been clicked
    if n_clicks:

        print('Running wrmXpress.')

        # necessary file paths
        img_dir = Path(volume, platename)
        input_dir = Path(volume, 'input')
        platename_input_dir = Path(input_dir, platename)
        plate_base = platename.split("_", 1)[0]
        htd_file = Path(img_dir, f'{plate_base}.HTD')
        full_yaml = Path(volume, platename + '.yml')

        update_yaml_file(
            full_yaml,
            full_yaml,
            {'wells': ['All']}
        )

        # clean and create directories
        clean_and_create_directories(
            input_path=Path(volume, 'input', platename), 
            work_path=Path(volume, 'work', platename),
            output_path=Path(volume, 'output')
        )

        copy_files_to_input_directory(
            platename_input_dir=platename_input_dir,
            htd_file=htd_file,
            img_dir=img_dir,
            plate_base=plate_base,
            wells=wells,
        )

        # Command message
        command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

        wrmxpress_command = f'python -u wrmXpress/wrapper.py {volume}/{platename}.yml {platename}'
        wrmxpress_command_split = shlex.split(wrmxpress_command)
        output_folder = Path(volume, 'work', platename)
        output_file = Path(volume, 'work', platename, f"{platename}_run.log")  # Specify the name and location of the output file

        if motility == 'True' or segment == 'True':
            while not os.path.exists(output_folder):
                time.sleep(1)
            with open(output_file, "w") as file:
            
                process = subprocess.Popen(
                    wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

                # Create an empty list to store the docker output
                docker_output = []
                wells_analyzed = []
                wells_to_be_analyzed = len(wells)

                for line in iter(process.stdout.readline, b''):
                    # Add the line to docker_output for further processing
                    docker_output.append(line)
                    file.write(line)
                    file.flush()
                    # Break the loop if 'Generating' is in the line
                    if "Generating" in line:
                        break

                    # Process the line if 'Running' is in the line
                    if "Running" in line:
                        well_running = line.split(" ")[-1]
                        if well_running not in wells_analyzed:
                            # Remove the '\n' from the well_running
                            well_running = well_running.replace('\n', '')
                            wells_analyzed.append(well_running)

                            img_path = Path(
                                volume, f'{platename}/TimePoint_1/{plate_base}_{wells_analyzed[-1]}.TIF')
                            fig = create_figure_from_filepath(img_path)

                            docker_output_formatted = ''.join(docker_output) 
                            set_progress((
                                str(len(wells_analyzed)),
                                str(wells_to_be_analyzed),
                                fig,
                                f'```{img_path}```',
                                f'```{docker_output_formatted}```'
                            ))
                

                # get the platename (default) file in output dir that have .png extension
                output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                while not os.path.exists(output_path):
                    time.sleep(1)

                # create a figure for the output
                fig_1 = create_figure_from_filepath(output_path) 
                
                print('wrmXpress has finished.')
                docker_output.append('wrmXpress has finished.')
                docker_output_formatted = ''.join(docker_output) 
                
                    
                # Return the figure, False, False, and an empty string
                return fig_1, False, False, f'', f'```{docker_output_formatted}```'
            
        if cellprofiler == 'True': 
            if cellprofilepipeline == 'wormsize':
                while not os.path.exists(output_folder):
                    time.sleep(1)
                with open(output_file, "w") as file:
                    process = subprocess.Popen(
                        wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    docker_output = []
                    wells_analyzed = []
                    wells_to_be_analyzed = len(wells)

                    # After starting the subprocess and opening the output file
                    for line in iter(process.stdout.readline, b''):
                        docker_output.append(line)
                        file.write(line)
                        file.flush()

                        # load the csv file which indicates which well is being analyzed
                        csv_file_path = Path(
                                    volume, 'input', f'image_paths_{cellprofilepipeline}.csv')
                        while not os.path.exists(csv_file_path):
                            time.sleep(1)

                        read_csv = pd.read_csv(csv_file_path)
                        # find the row titled Metadata_Well
                        well_column = read_csv['Metadata_Well']
                        
                        if 'Execution halted' in line:
                            output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                            while not os.path.exists(output_path):
                                time.sleep(1)

                            # create a figure for the output
                            fig_1 = create_figure_from_filepath(output_path)
                            
                            print('wrmXpress has finished.')
                            docker_output.append('wrmXpress has finished.')
                            docker_output_formatted = ''.join(docker_output) 
                            return fig_1, False, False, '', f'```{docker_output_formatted}```'

                        # Check for the 'Image #' pattern and extract the number
                        elif 'Image #' in line:
                            # Extracting the image number
                            image_number_pattern = re.search(r'Image # (\d+)', line)
                            if image_number_pattern:
                                image_number = int(image_number_pattern.group(1))
                                
                                # Find the well from the CSV using the image number
                                well_id = well_column.iloc[image_number - 1]  # Adjusting for zero indexing

                                # Construct the image path
                                img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}.TIF')
                                if img_path.exists():
                                    # Load and display the image
                                    fig = create_figure_from_filepath(img_path)

                                    docker_output_formatted = ''.join(docker_output) 

                                    # Update progress
                                    set_progress((str(image_number), str(len(wells)), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))

            elif cellprofilepipeline == 'wormsize_intensity_cellpose':
                while not os.path.exists(output_folder):
                    time.sleep(1)
                with open(output_file, "w") as file:
                    process = subprocess.Popen(
                        wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    docker_output = []
                    wells_analyzed = []
                    wells_to_be_analyzed = len(wells)
                    progress = 0
                    total_progress = 2 * wells_to_be_analyzed
                    # After starting the subprocess and opening the output file
                    for line in iter(process.stdout.readline, b''):
                        docker_output.append(line)
                        file.write(line)
                        file.flush()
                        
                        if 'Generating w1 thumbnails' in line:
                            output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                            while not os.path.exists(output_path):
                                time.sleep(1)

                            # create a figure for the output
                            fig_1 = create_figure_from_filepath(output_path)
                            print('wrmXpress has finished.')
                            docker_output.append('wrmXpress has finished.')
                            docker_output_formatted = ''.join(docker_output) 
                            return fig_1, False, False, f'', f'```{docker_output_formatted}```'
                        else:
                            # Check for the 'Image #' pattern and extract the number
                            if 'Image #' in line:

                                # load the csv file which indicates which well is being analyzed
                                csv_file_path = Path(
                                            volume, 'input', f'image_paths_{cellprofilepipeline}.csv')
                                while not os.path.exists(csv_file_path):
                                    time.sleep(1)

                                read_csv = pd.read_csv(csv_file_path)
                                # find the row titled Metadata_Well
                                well_column = read_csv['Metadata_Well']

                                # Extracting the image number
                                image_number_pattern = re.search(r'Image # (\d+)', line)
                                if image_number_pattern:
                                    image_number = int(image_number_pattern.group(1))
                                    
                                    # Find the well from the CSV using the image number
                                    well_id = well_column.iloc[image_number - 1]  # Adjusting for zero indexing

                                    # Construct the image path
                                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}.TIF')
                                    if img_path.exists():
                                        # Load and display the image
                                        fig = create_figure_from_filepath(img_path)
                                        progress = int(progress) + 1
                                        docker_output_formatted = ''.join(docker_output) 

                                        # Update progress
                                        set_progress((str(len(wells) + image_number), str(2*len(wells)), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
                            elif "[INFO]" in line:
                                if "%" in line:
                                    info_well_analyzed = line.split("/")[0].split(' ')[-1]
                                    info_total_wells = line.split("/")[1].split(' ')[0]
                                    if info_total_wells == info_well_analyzed:
                                        current_well = wells[int(info_well_analyzed)-1]
                                        img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{current_well}.TIF')
                                        if os.path.exists(img_path):
                                            fig = create_figure_from_filepath(img_path)
                                            docker_output_formatted = ''.join(docker_output)
                                            
                                            set_progress((str(progress), str(total_progress), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))

                                    elif info_well_analyzed != info_total_wells:
                                        current_well = wells[int(info_well_analyzed)]
                                        img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{current_well}.TIF')
                                        if os.path.exists(img_path):
                                            fig = create_figure_from_filepath(img_path, 'gray')
                                            docker_output_formatted = ''.join(docker_output)
                                            progress = int(progress) + 1
                                            set_progress((str(progress), str(total_progress), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
            elif cellprofilepipeline == "mf_celltox":
                while not os.path.exists(output_folder):
                    time.sleep(1)
                with open(output_file, "w") as file:
                    process = subprocess.Popen(
                        wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    docker_output = []
                    wells_analyzed = []
                    wells_to_be_analyzed = len(wells)
                    progress = 0
                    total_progress = 2 * wells_to_be_analyzed
                    # After starting the subprocess and opening the output file
                    for line in iter(process.stdout.readline, b''):
                        docker_output.append(line)
                        file.write(line)
                        file.flush()

                        if 'Generating w1 thumbnails' in line:
                            output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                            while not os.path.exists(output_path):
                                time.sleep(1)

                            # create a figure for the output
                            fig_1 = create_figure_from_filepath(output_path)
                            print('wrmXpress has finished.')
                            docker_output.append('wrmXpress has finished.')
                            docker_output_formatted = ''.join(docker_output) 
                            return fig_1, False, False, f'', f'```{docker_output_formatted}```'
                        
                        elif "Stitching w1 of multi-site images" in line:
                            wells_analyzed.append(wells[int(progress)])
                            progress = int(progress) + 1
                            img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{wells_analyzed[-1]}_s1.TIF')
                            if os.path.exists(img_path):
                                fig = create_figure_from_filepath(img_path)
                                docker_output_formatted = ''.join(docker_output)
                                set_progress((str(progress), str(total_progress), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
                        
            elif cellprofilepipeline == "feeding":
                while not os.path.exists(output_folder):
                    time.sleep(1)
                with open(output_file, "w") as file:
                    process = subprocess.Popen(
                        wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    docker_output = []
                    wells_analyzed = []
                    wells_to_be_analyzed = len(wells)

                    # After starting the subprocess and opening the output file
                    for line in iter(process.stdout.readline, b''):
                        docker_output.append(line)
                        file.write(line)
                        file.flush()

                        # load the csv file which indicates which well is being analyzed
                        csv_file_path = Path(
                                    volume, 'input', f'image_paths_{cellprofilepipeline}.csv')
                        while not os.path.exists(csv_file_path):
                            time.sleep(1)

                        read_csv = pd.read_csv(csv_file_path)
                        # find the row titled Metadata_Well
                        well_column = read_csv['Metadata_Well']
                        
                        if 'Generating w1 thumbnails' in line:
                            output_path = Path(volume, 'output', 'thumbs', platename + "_w1" + '.png')
                            while not os.path.exists(output_path):
                                time.sleep(1)

                            # create a figure for the output
                            fig_1 = create_figure_from_filepath(output_path)
                            
                            print('wrmXpress has finished.')
                            docker_output.append('wrmXpress has finished.')
                            docker_output_formatted = ''.join(docker_output) 
                            return fig_1, False, False, '', f'```{docker_output_formatted}```'

                        # Check for the 'Image #' pattern and extract the number
                        elif 'Image #' in line:
                            # Extracting the image number
                            image_number_pattern = re.search(r'Image # (\d+)', line)
                            if image_number_pattern:
                                image_number = int(image_number_pattern.group(1))
                                
                                # Find the well from the CSV using the image number
                                well_id = well_column.iloc[image_number - 1]  # Adjusting for zero indexing

                                # Construct the image path
                                img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}_w1.TIF')
                                if img_path.exists():
                                    # Load and display the image
                                    fig = create_figure_from_filepath(img_path)

                                    docker_output_formatted = ''.join(docker_output) 

                                    # Update progress
                                    set_progress((str(image_number), str(len(wells)), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
                                
                            
                            
                        

                            

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)
