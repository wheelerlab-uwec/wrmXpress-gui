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
                children=dbc.NavLink(f"{page['name']}",
                                     href=page["relative_path"],
                                     active='exact'
                                     ),
                pills=True,
                vertical=True
            ) for page in dash.page_registry.values()
        ])
    ],
    style=SIDEBAR_STYLE
)

app.layout = html.Div([
    dcc.Store(id='store', data={}),
    sidebar,
    html.Div(id="page-content",
             children=[header, dash.page_container],
             style=CONTENT_STYLE)])

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

    cancel=[Input("cancel-analysis", "n_clicks")],
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
    if not store:
        return None, True, True, "No configuration found. Please go to the configuration page to set up the analysis."
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    if n_clicks:
        """
        Checking if wrmXpress container exists
        """
        try:
            good_to_go = False
            check_for_names = ['zamanianlab/wrmxpress', 'latest']
            client = docker.from_env()
            images_in_docker = client.images.list()
            for img in images_in_docker:
                img = f"{img}"
                # Remove angle brackets, quotes, and split
                image_info = img.strip()[8:-1].strip("'").split("', '")
                image_tag = image_info[-1]
                if check_for_names[0] in image_tag:
                    good_to_go = True
                if check_for_names[1] in image_tag:
                    good_to_go = True

            if good_to_go == False:
                return None, True, True, "wrmXpress container not found. Please install the container and try again."
        except ValueError as ve:
            return None, True, True, f"Error: {ve}"

        """
        Replace this section following the fix in the wrmXpress bug
        """
        folder_containing_img = Path(volume, platename)
        input_folder = Path(volume, 'input')
        platename_input_folder = Path(input_folder, platename)
        plate_base = platename.split("_", 1)[0]
        htd_file_path = folder_containing_img / f'{plate_base}.HTD'

        full_yaml = Path(volume, platename + '.yml')

        # reading in yaml file
        with open(full_yaml, 'r') as file:
            data = yaml.safe_load(file)

        # assigning first well to the well value
        data['wells'] = ['All']

        # Dump preview data to temp YAML file
        with open(full_yaml, 'w') as yaml_file:
            yaml.dump(data, yaml_file,
                      default_flow_style=False)

        # check to see if input folder exists, if not create it
        # then copy necessay files into input folder
        if not os.path.exists(Path(volume, 'input')):
            os.makedirs(Path(volume, 'input'))
            os.makedirs(Path(volume, 'input', platename))

            # Copy .HTD file into platename input folder
            shutil.copy(htd_file_path, platename_input_folder)
            # Collecting the time point folders
            folders = [item for item in os.listdir(folder_containing_img) if os.path.isdir(
                Path(folder_containing_img, item))]
            # Iterate through each time point
            for folder in folders:
                time_point_folder = Path(platename_input_folder, folder)
                os.makedirs(time_point_folder, exist_ok=True)
                for well in store["wells"]:
                    # Copy necessary wells image into time point folder
                    well_path = Path(folder_containing_img,
                                     folder, f'{plate_base}_{well}.TIF')
                    shutil.copy(well_path, time_point_folder)
        # if input folder exists, check to see if platename folder exists, if not create it
        # then copy necessay files into platename folder
        elif os.path.exists(Path(volume, 'input')):
            if not os.path.exists(htd_file_path):
                shutil.copy(htd_file_path, platename_input_folder)

            if not os.path.exists(platename_input_folder):
                os.makedirs(platename_input_folder)
                # Collecting the time point folders
                folders = [item for item in os.listdir(folder_containing_img) if os.path.isdir(
                    Path(folder_containing_img, item))]
                # Iterate through each time point
                for folder in folders:
                    time_point_folder = Path(platename_input_folder, folder)
                    os.makedirs(time_point_folder, exist_ok=True)
                    for well in store["wells"]:
                        # Copy necessary wells image into time point folder
                        well_path = Path(folder_containing_img,
                                         folder, f'{plate_base}_{well}.TIF')
                        shutil.copy(well_path, time_point_folder)

            # if input folder & platname folder exist, clear platename folder and copy necessary files into it
            elif os.path.exists(platename_input_folder):
                os.system(f'rm -rf {platename_input_folder}')
                os.makedirs(platename_input_folder)
                shutil.copy(htd_file_path, platename_input_folder)
                # Collecting the time point folders
                folders = [item for item in os.listdir(folder_containing_img) if os.path.isdir(
                    Path(folder_containing_img, item))]
                # Iterate through each time point
                for folder in folders:
                    time_point_folder = Path(platename_input_folder, folder)
                    if not os.path.exists(time_point_folder):
                        os.makedirs(time_point_folder, exist_ok=True)
                        for well in store["wells"]:
                            # Copy necessary wells image into time point folder
                            well_path = Path(folder_containing_img,
                                             folder, f'{plate_base}_{well}.TIF')
                            shutil.copy(well_path, time_point_folder)

        # check to see if work folder exists, if it does delete it
        if os.path.exists(Path(volume, 'work')):
            for filename in os.listdir(Path(volume, 'work')):
                file_path = os.path.join(Path(volume, 'work'), filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s because %s' % (file_path, e))

        # check to see if output folder exists, if it does delete it
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
        """
        End of section to replace 
        """

        print(client)

        command = f"python -u wrmXpress/wrapper.py {platename}.yml {platename}"
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

        while container_status in ['created', 'running']:
            container.reload()
            container_status = container.status
            time.sleep(1)
            # Retrieve and process the logs after the container has finished
            result = subprocess.run(
                ['docker', 'logs', container_name], capture_output=True, text=True)
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                if "Running" in line:
                    well_running = line.split(" ")[-1]
                    if well_running not in wells_analyzed:
                        wells_analyzed.append(well_running)
                        current_well = wells_analyzed[-1]
                        # Optain filepath for the well being analyzed
                        img_path = Path(
                            volume, f'{platename}/TimePoint_1/{plate_base}_{wells_analyzed[-1]}.TIF')
                        img = np.array(Image.open(img_path))
                        fig = px.imshow(img, color_continuous_scale="gray")
                        fig.update_layout(coloraxis_showscale=False)
                        fig.update_xaxes(showticklabels=False)
                        fig.update_yaxes(showticklabels=False)

                        set_progress((
                            str(len(wells_analyzed)),
                            str(wells_to_be_analyzed),
                            fig,
                            f'```{img_path}```'
                        ))

        # get all files in output folder that have .png extension
        output_path = Path(volume, 'output', 'thumbs', platename + '.png')
        img1 = np.array(Image.open(output_path))
        fig_1 = px.imshow(img1, color_continuous_scale="gray")
        fig_1.update_layout(coloraxis_showscale=False)
        fig_1.update_xaxes(showticklabels=False)
        fig_1.update_yaxes(showticklabels=False)
        
        return fig_1, False, False, ''

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)
