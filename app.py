########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import docker
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
import os
import subprocess
import yaml
from dash.long_callback import DiskcacheLongCallbackManager
import shutil

# Importing Components
from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header

# importing utils
from app.utils.styling import layout

# Diskcache
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = Dash(__name__,
           long_callback_manager=long_callback_manager,
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


@app.long_callback(
    output=[
        Output("image-analysis-preview", "figure"),
        Output('load-analysis-img', 'disabled'),
        Output("run-page-alert", 'is_open'),
        Output("run-page-alert", 'children'),
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
    ],
    prevent_initial_call=True,
    allow_duplicate=True
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
        return None, True, True, "No configuration found. Please go to the configuration page to set up the analysis."

    # obtain the necessary data from the store
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]

    # Check if the submit button has been clicked
    if n_clicks:

        # Checking if wrmXpress container exists
        try:
            good_to_go = False  # Set good_to_go to False
            # Set check_for_names to a list containing the names of the container
            check_for_names = ['zamanianlab/wrmxpress', 'latest']
            client = docker.from_env()  # Create a docker client
            images_in_docker = client.images.list()  # List all images in the docker client
            for img in images_in_docker:  # Iterate through each image in the docker client
                img = f"{img}"  # Convert the image to a string

                # Remove angle brackets, quotes, and split
                image_info = img.strip()[8:-1].strip("'").split("', '")
                image_tag = image_info[-1]

                # Check if the image tag is in the list of names
                if check_for_names[0] in image_tag:
                    good_to_go = True
                    if check_for_names[1] not in image_tag:
                        good_to_go = False

            # If good_to_go is False, return an error message
            if good_to_go == False:
                return None, True, True, "wrmXpress container not found. Please install the container and try again."

        # return an error message if an error occurs that was not anticipated
        except ValueError as ve:
            return None, True, True, f"Error: {ve}"


        # necessary file paths
        img_dir = Path(volume, platename)
        input_dir = Path(volume, 'input')
        platename_input_dir = Path(input_dir, platename)
        plate_base = platename.split("_", 1)[0]
        htd_file = Path(img_dir, f'{plate_base}.HTD')
        full_yaml = Path(volume, platename + '.yml')

        # reading in yaml file
        with open(full_yaml, 'r') as file:
            data = yaml.safe_load(file)

        # replace the YAML config option with ['All'] as a workaround for wrmXpress bug
        # instead, we'll copy the selected files to input and analyze all of them
        data['wells'] = ['All']

        with open(full_yaml, 'w') as yaml_file:
            yaml.dump(data, yaml_file,
                      default_flow_style=False)
            
        # wipe previous runs
        if os.path.exists(Path(volume, 'work', platename)):
            shutil.rmtree(Path(volume, 'work', platename))
            Path(volume, 'work', platename).mkdir(parents=True, exist_ok=True)
        else:
            Path(volume, 'work', platename).mkdir(parents=True, exist_ok=True)

        if os.path.exists(Path(volume, 'input', platename)):
            shutil.rmtree(Path(volume, 'input', platename))
            Path(volume, 'input', platename).mkdir(parents=True, exist_ok=True)
        else:
            Path(volume, 'input', platename).mkdir(parents=True, exist_ok=True)

        # wipe contents of output (different logic because backend doesn't put all output in a platename dir)
        if os.path.exists(Path(volume, 'output')):
            for filename in os.listdir(Path(volume, 'output')):
                file_path = os.path.join(Path(volume, 'output'), filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s because %s' % (file_path, e))

        # Copy .HTD file into platename input dir
        shutil.copy(htd_file, platename_input_dir)

        # Iterate through each time point and copy images into new dirs
        time_points = [item for item in os.listdir(img_dir) if os.path.isdir(
            Path(img_dir, item))]

        for time_point in time_points:
            time_point_dir = Path(platename_input_dir, time_point)
            time_point_dir.mkdir(parents=True, exist_ok=True)
            
            for well in store["wells"]:
                well_path = Path(img_dir,
                                 time_point, f'{plate_base}_{well}.TIF')
                shutil.copy(well_path, time_point_dir)
        """
        End of section to replace 
        """

        print(client)  # Print the client

        # Command to run the analysis
        command = f"python -u wrmXpress/wrapper.py {platename}.yml {platename}"
        # Command message
        command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

        container = client.containers.run('zamanianlab/wrmxpress', command=f"{command}", detach=True,
                                          volumes={f'{volume}/input/': {'bind': '/input/', 'mode': 'rw'},
                                                   f'{volume}/output/': {'bind': '/output/', 'mode': 'rw'},
                                                   f'{volume}/work/': {'bind': '/work/', 'mode': 'rw'},
                                                   f'{volume}/{platename}.yml': {'bind': f'/{platename}.yml', 'mode': 'rw'}
                                                   })

        # Get the name of the most recent container
        container_name = container.name
        container_status = container.status
        wells_to_be_analyzed = len(store["wells"])
        wells_analyzed = []

        # While the container is running
        while container_status in ['created', 'running']:
            container.reload()  # Reload the container
            container_status = container.status  # Get the status of the container
            time.sleep(1)  # Sleep for 1 second

            # Retrieve and process the logs after the container has finished
            result = subprocess.run(
                ['docker', 'logs', container_name], capture_output=True, text=True)

            output_lines = result.stdout.splitlines()  # Split the output lines

            for line in output_lines:  # Iterate through each line in the output lines

                if "Running" in line:  # If "Running" is in the line

                    # Get the well that is running
                    well_running = line.split(" ")[-1]

                    if well_running not in wells_analyzed:  # If the well that is running is not in the wells analyzed

                        # Append the well that is running to the wells analyzed
                        wells_analyzed.append(well_running)

                        # Optain filepath for the well being analyzed
                        img_path = Path(
                            volume, f'{platename}/TimePoint_1/{plate_base}_{wells_analyzed[-1]}.TIF')

                        # create a figure for the well being analyzed
                        img = np.array(Image.open(img_path))
                        fig = px.imshow(img, color_continuous_scale="gray")
                        fig.update_layout(coloraxis_showscale=False)
                        fig.update_xaxes(showticklabels=False)
                        fig.update_yaxes(showticklabels=False)

                        # Set the progress of the analysis which
                        # includes the number of wells analyzed, the number of wells to be analyzed,
                        # the figure, and the image path
                        set_progress((
                            str(len(wells_analyzed)),
                            str(wells_to_be_analyzed),
                            fig,
                            f'```{img_path}```'
                        ))

        # get the platename (default) file in output dir that have .png extension
        output_path = Path(volume, 'output', 'thumbs', platename + '.png')

        # create a figure for the output
        img1 = np.array(Image.open(output_path))
        fig_1 = px.imshow(img1, color_continuous_scale="gray")
        fig_1.update_layout(coloraxis_showscale=False)
        fig_1.update_xaxes(showticklabels=False)
        fig_1.update_yaxes(showticklabels=False)

        # Return the figure, False, False, and an empty string
        return fig_1, False, False, ''

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)
