########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import docker
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
import os
import dash
import plotly.graph_objs as go
import subprocess
import shutil
import yaml

# importing utils
from app.utils.styling import layout

dash.register_page(__name__)

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

layout = dbc.ModalBody(
    [
        # Preview page contents
        html.Div([
            html.Div([
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Configure Summary",
                                        className="text-center"),
                                dcc.Markdown(
                                    id='img-mode-output',
                                    className="card-subtitle"),
                                dcc.Markdown(
                                    id='file-structure-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='plate-format-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='img-masking-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='mod-selection-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='volume-name-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='plate-name-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='wells-content-output',
                                    className='card-subtitle'),
                                dbc.Button('Begin Analysis',
                                           id='submit-analysis',
                                           className="d-grid gap-2 col-6 mx-auto",
                                           color="primary",
                                           n_clicks=0),
                                html.Br(),
                                dbc.Alert(children=[
                                    dbc.Progress(
                                        id = 'progress-bar-run-page',
                                        striped = True,
                                        color = "primary",
                                        value = 50,
                                        animated=True,
                                    ),
                                ], is_open = True, color = 'success', id = 'alert-progress-bar-run-page', 
                                ),
                                dcc.Loading(
                                    id="loading-2",
                                    children=[
                                        html.Div([
                                            dcc.Graph(
                                                id='image-analysis-preview',
                                                # Empty layout for now
                                                figure={'layout': {}},
                                                className='h-100 w-100'
                                            ),
                                        ])],
                                    type="cube",
                                ),

                            ])
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4(
                                    "Run Diagnosis", className="text-center"),
                                dcc.Loading(
                                    id="loading-2",
                                    children=[
                                        html.Div([
                                            dcc.Graph(
                                                id='analysis-postview',
                                                # Empty layout for now
                                                figure={'layout': {}},
                                                className='h-100 w-100'
                                            ),
                                        ])],
                                    type="cube",
                                ),

                                dcc.Loading(
                                    id="loading-2",
                                    children=[
                                        html.Div([
                                            dcc.Graph(
                                                id='analysis-postview-another',
                                                # Empty layout for now
                                                figure={'layout': {}},
                                                className='h-100 w-100'
                                            ),
                                        ])],
                                    type="cube",
                                ),

                            ])
                        )
                    ),
                ]),
                dbc.Row([
                    dbc.Alert(
                        id='run-page-alert',
                        color='success',
                        is_open=False,
                        duration=30000,
                    ),
                ])
            ])
        ])
    ]
)

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@callback(
    Output("img-mode-output", 'children'),
    Output('file-structure-output', 'children'),
    Output('plate-format-output', 'children'),
    Output('img-masking-output',  'children'),
    Output('mod-selection-output', 'children'),
    Output('volume-name-output', 'children'),
    Output('plate-name-output',  'children'),
    Output('wells-content-output',  'children'),
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_results_message_for_run_page(
    nclicks,
    store
):
    img_mode = f'Imaging Mode: {store["img_mode"]}'
    file_structure = f'File Structure: {store["file_structure"]}'
    plate_format = f'Plate Format: Rows = {store["rows"]}, Cols = {store["cols"]}'
    img_masking = f'Image Masking: {store["img_masking"]}'
    mod_selection = f'Module Selection: {store["motility"]}'
    volume = f'Volume: {store["mount"]}'
    platename = f'Platename: {store["platename"]}'
    wells = f'Wells: {store["wells"]}'
    results = [
        img_mode,
        file_structure,
        plate_format,
        img_masking,
        mod_selection,
        volume,
        platename,
        wells
    ]
    if nclicks:
        return results


@callback(
    Output('image-analysis-preview', 'figure'),
    Output('analysis-postview', 'figure'),
    Output('analysis-postview-another', 'figure'),
    Output('run-page-alert', 'is_open'),
    Output('run-page-alert', 'children'),
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def run_analysis(
    nclicks,
    store
):
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]

    if nclicks:

        """
        Checking if input folder exists, and if not, create it, 
        then subsequently copy the images into this folder
        """

        ########################################################
        ####                                                ####
        ####        Bypassing the wrmxpress bug             ####
        ####                                                ####
        ########################################################
        """
        remove this section following the fix in the wrmxpress bug
        """
        # check to see if we are analyzing one well
        if wells != 'All' and len(wells) == 1:
            # redo yaml file to include "All" wells -- bypass wrmxpress bug for now

            # defining the yaml file path (same as the filepath from configure.py)
            full_yaml = Path(volume, platename + '.yml')

            # reading in yaml file
            with open(full_yaml, 'r') as file:
                data = yaml.safe_load(file)

            # assigning first well to the well value
            data['wells'] = "All"

            # Dump preview data to temp YAML file
            with open(full_yaml, 'w') as yaml_file:
                yaml.dump(data, yaml_file,
                        default_flow_style=False)
        """
        end of remove section following wrmxpress bug fix
        """

        # input and platename input folder paths
        input_folder = Path(volume, 'input')
        platename_input_folder = Path(input_folder, platename)

        # if the input folder does not exist, create it
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
            os.system(f'cp -r {Path(volume, platename)} {input_folder}')

        # if the input folder exists, but the platename folder does not exist, create it
        if os.path.exists(input_folder):
            if not os.path.exists(platename_input_folder):
                os.system(f'cp -r {Path(volume, platename)} {input_folder}')

            # if the input folder exists, and the platename folder exists, replace the platename folder with the input folder
            if os.path.exists(platename_input_folder):
                os.system(f'cp -rf {Path(volume, platename)} {input_folder}')

        client = docker.from_env()
        print(client)

        command = f"python wrmXpress/wrapper.py {platename}.yml {platename}"
        command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

        container = client.containers.run('zamanianlab/wrmxpress', command=f"{command}", detach=True,
                                          volumes={f'{volume}/input/': {'bind': '/input/', 'mode': 'rw'},
                                                   f'{volume}/output/': {'bind': '/output/', 'mode': 'rw'},
                                                   f'{volume}/work/': {'bind': '/work/', 'mode': 'rw'},
                                                   f'{volume}/{platename}.yml': {'bind': f'/{platename}.yml', 'mode': 'rw'}
                                                   })
        # Get the name of the most recent container
        container_name = container.name

        # Wait for the container to finish running (adjust timeout as needed)
        container.wait(timeout=300)

        # Retrieve and process the logs after the container has finished
        result = subprocess.run(
            ['docker', 'logs', container_name], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()

        # ensure that these rows of the output are not indented
        non_indented = [
            'instrument settings:',
            "wormzzzz:",
            "modules:",
            "run-time settings:",
            "HTD metadata:",
        ]
        # Convert each line into an HTML paragraph element
        markdown_lines = [dcc.Markdown(f"```{line}```", className='mb-0') if line in non_indented else dcc.Markdown(
            f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```{line}```", className='mb-0') for line in output_lines]

        # assumes IX-like file structure
        img_path = Path(
            volume, 'output', 'thumbs', f'{platename}.png')

        # directory path to the thumbs
        file_path = Path(
            volume, 'output', 'thumbs'
        )

        # ensures that the images have been processed
        while not os.path.exists(img_path):
            time.sleep(1)

        # empty list of filepaths which will be added to later
        files_with_png = []

        # Iterate through all files and subdirectories
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.lower().endswith('.png'):  # Check if the file is a PNG file
                    # Get the full file path
                    file_path = os.path.join(root, file)
                    # append the file path to the list
                    files_with_png.append(file_path)

        # empty list for the figures to be added to once they have been processed
        figs = []

        # iterating through each file path and getting the subsequent image
        for i, file_path in enumerate(files_with_png):
            img = np.array(Image.open(file_path))  # Open the image using PIL
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            figs.append(fig)  # appending this image to the list
        # Return the figures as a tuple

        return figs[0], figs[1], figs[2], True, markdown_lines
