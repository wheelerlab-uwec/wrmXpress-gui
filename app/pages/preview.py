########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import docker
import yaml
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
from app.utils.callback_functions import prep_yaml
import os
import plotly.graph_objs as go
import subprocess
import shutil

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
                                    html.H4("Input preview",
                                            className="text-center mb-5"),
                                    dbc.Row([
                                        dbc.Button('Preview Analysis',
                                               id='submit-val',
                                               className="d-grid gap-2 col-6 mx-auto",
                                               color="primary",
                                               n_clicks=0),
                                    ]),
                                    html.Br(),
                                    html.H6(
                                        "Path:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(id='input-path-output'),
                                    html.Div(
                                        dbc.Alert(
                                            id='input-img-view-alert',
                                            color='light',
                                            is_open=True,
                                            children=[
                                                dcc.Loading(
                                                    id='loading-1',
                                                    children=[
                                                        html.Div([
                                                            dcc.Graph(
                                                                id='input-preview',
                                                                figure={
                                                                    'layout': layout},
                                                                className='h-100 w-100'
                                                            )
                                                        ]),
                                                    ],
                                                    type='cube',
                                                    color='#3b4d61'
                                                ),
                                            ]
                                        ),
                                    ),
                                ]
                                ),
                                style={'height': '100%',
                                       'width': '99%'},
                            ),
                            width={'size': 6},
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4(
                                        "Analysis preview", className="text-center"),
                                    html.Br(),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='preview-dropdown',
                                                    placeholder='Select image to preview...'
                                                ),
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "Load Image",
                                                    id="preview-change-img-button",
                                                    className="d-grid gap-2 col-6 mx-auto",
                                                    color="primary",
                                                    disabled=True,
                                                    n_clicks=0
                                                ),
                                            )
                                        ]
                                    ),
                                    html.Br(),
                                    html.H6(
                                        "Command:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(
                                        id='analysis-preview-message'),
                                    dbc.Alert(
                                        id='preview-img-view-alert',
                                        color='light',
                                        is_open=True,
                                        children=[
                                            dcc.Loading(
                                                id="loading-2",
                                                children=[
                                                    html.Div([
                                                        dcc.Graph(
                                                            id='analysis-preview',
                                                            figure={
                                                                'layout': layout},
                                                            className='h-100 w-100'
                                                        ),
                                                    ])],
                                                type="cube",
                                                color='#3b4d61'
                                            ),
                                        ],
                                    ),
                                    dbc.Alert(
                                        id='post-analysis-first-well-img-view-alert',
                                        color='light',
                                        is_open=False,
                                        children=[
                                            dcc.Loading(
                                                id="loading-2",
                                                children=[
                                                    html.Div([
                                                        dcc.Graph(
                                                            id='analysis-preview-other-img',
                                                            figure={
                                                                'layout': layout},
                                                            className='h-100 w-100'
                                                        ),
                                                    ])],
                                                type="cube",
                                                color='#3b4d61'
                                            ),
                                        ],
                                    ),
                                    dbc.Alert(id='resolving-error-issue-preview',
                                              is_open=False, color='success', duration=6000),
                                    dbc.Alert(
                                        id='view-docker-logs', is_open=False, color='success', duration=30000),
                                ]
                                ),
                                style={'height': '100%',
                                       'width': '99%'},
                            ),
                            width={'size': 6}
                        )
                        ])
            ]
            )
        ]
        )
    ],
)


########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################

@callback(
    Output("analysis-preview-other-img", "figure"),
    Output("preview-img-view-alert", "is_open"),
    Output("post-analysis-first-well-img-view-alert", "is_open"),
    State("preview-dropdown", 'value'),
    Input("preview-change-img-button", 'n_clicks'),
    State('store', 'data'),
)
def update_analysis_preview_imgage(selection, nclicks, store):
    if nclicks:
        volume = store['mount']
        platename = store['platename']
        wells = store["wells"]

        # assumes IX-like file structure
        img_path = Path(
            f'{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}_{selection}.png')
        if os.path.exists(img_path):
            if selection == 'motility':
                scale = 'inferno'
            else:
                scale = 'gray'
            img = np.array(Image.open(img_path))
            fig = px.imshow(img, color_continuous_scale=scale)
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            return fig, False, True
        else:
            return None,True, False
    return None, True, False

@callback(
    Output('input-path-output', 'children'),
    Output('input-preview', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def update_preview_image(n_clicks, store):

    wells = store['wells']
    first_well = wells[0].replace(', ', '')

    platename = store['platename']
    plate_base = platename.split("_", 1)[0]

    volume = store['mount']
    if n_clicks >= 1:
        # assumes IX-like file structure
        img_path = Path(
            volume, f'{platename}/TimePoint_1/{plate_base}_{first_well}.TIF')
        img = np.array(Image.open(img_path))
        fig = px.imshow(img, color_continuous_scale="gray")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return f'```{img_path}```', fig
    n_clicks = 0


@callback(
    Output('preview-dropdown', 'options'),
    # update the option dropdown when the previous load is clicked
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def get_options(nclicks, store):

    motility = store['motility']
    segment = store['segment']
    selection_dict = {'motility': 'motility', 'segment': 'binary'}
    option_dict = {}

    if nclicks is not None:
        for selection in selection_dict.keys():
            if eval(selection) == 'True':
                option_dict[selection] = selection_dict[selection]

    dict_option = {v: k for k, v in option_dict.items()}
    return dict_option


@callback(
    Output('analysis-preview-message', 'children'),
    Output('analysis-preview', 'figure'),
    Output('resolving-error-issue-preview', 'is_open'),
    Output('resolving-error-issue-preview', 'children'),
    Output("preview-change-img-button", "disabled"),
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def run_analysis(
    nclicks,
    store,
):
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    motility_selection = store['motility']
    segment_selection = store['segment']

    if motility_selection == 'True':
        selection = '_motility'
    elif segment_selection == 'True':
        selection = '_segment'
    else:
        selection = ''
    if nclicks:
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
                return None, None, True, f'Please ensure that you have the Image "{check_for_names[0]}" and is the "{check_for_names[1]}" image.', True
        except ValueError as ve:
            return None, None, True, 'An error occured somewhere', True
        # Check to see if first well already exists, if it does insert the img
        # rather than running wrmXpress again
        first_well_path = Path(
            volume, 'work', f'{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection}.png')
        if os.path.exists(first_well_path):
            if selection == 'motility':
                scale = 'inferno'
            else:
                scale = 'gray'
            img = np.array(Image.open(first_well_path))
            fig = px.imshow(img, color_continuous_scale=scale)
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            return f"```{first_well_path}```", fig, False, f'', False
        ########################################################################
        ####                                                                ####
        ####                  Preview YAML Creation                         ####
        ####                                                                ####
        ########################################################################
        """
        Remove this section following the fix in the wrmXpress bug
        """
        if wells != 'All':
            first_well = ['All']

        # defining the yaml file path (same as the filepath from configure.py)
        preview_yaml_platename = '.' + platename + '.yml'
        preview_yaml_platenmaefull_yaml = Path(volume, preview_yaml_platename)
        full_yaml = Path(volume, platename + '.yml')

        # reading in yaml file
        with open(full_yaml, 'r') as file:
            data = yaml.safe_load(file)

        # assigning first well to the well value
        data['wells'] = first_well

        # Dump preview data to temp YAML file
        with open(preview_yaml_platenmaefull_yaml, 'w') as yaml_file:
            yaml.dump(data, yaml_file,
                      default_flow_style=False)
        if wells == 'All':
            first_well = "A01"
        else:
            first_well = wells[0]
        """
        End of section to remove following the fix in the wrmXpress bug
        """

        """
        Checking if input folder exists, and if not, create it, 
        then subsequently copy the images into this folder
        """

        # Input and platename input folder paths
        folder_containing_img = Path(volume, platename)
        input_folder = Path(volume, 'input')
        platename_input_folder = Path(input_folder, platename)
        os.makedirs(platename_input_folder, exist_ok=True)

        # Copy .HTD file into platename input folder
        htd_file_path = folder_containing_img / f'{plate_base}.HTD'
        shutil.copy(htd_file_path, platename_input_folder)

        # Collecting the time point folders
        folders = [item for item in os.listdir(folder_containing_img) if os.path.isdir(
            Path(folder_containing_img, item))]

        # Iterate through each time point
        for folder in folders:
            time_point_folder = Path(platename_input_folder, folder)
            os.makedirs(time_point_folder, exist_ok=True)

            # Copy first and second well image into time point folder
            first_well_path = Path(folder_containing_img,
                                   folder, f'{plate_base}_{first_well}.TIF')
            shutil.copy(first_well_path, time_point_folder)

        yaml_file = Path(platename + '.yml')

        print(client)

        command = f"python wrmXpress/wrapper.py {preview_yaml_platename} {platename}"
        command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

        container = client.containers.run('zamanianlab/wrmxpress', command=f"{command}", detach=True,
                                          volumes={f'{volume}/input/': {'bind': '/input/', 'mode': 'rw'},
                                                   f'{volume}/output/': {'bind': '/output/', 'mode': 'rw'},
                                                   f'{volume}/work/': {'bind': '/work/', 'mode': 'rw'},
                                                   f'{volume}/{preview_yaml_platename}': {'bind': f'/{preview_yaml_platename}', 'mode': 'rw'}
                                                   })
        # Get the name of the most recent container
        container_name = container.name

        # Wait for the container to finish running (adjust timeout as needed)
        container.wait(timeout=300)

        # Retrieve and process the logs after the container has finished
        result = subprocess.run(
            ['docker', 'logs', container_name], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()

        # Convert each line into an HTML paragraph element
        result = [dcc.Markdown(f"```{line}```", className="mb-0")
                  for line in output_lines]

        # assumes IX-like file structure
        img_path = Path(
            volume, 'work', f'{platename}/{first_well}/img/{platename}_{first_well}{selection}.png')

        while not os.path.exists(img_path):
            time.sleep(1)

        img = np.array(Image.open(img_path))
        if selection == 'motility':
            scale = 'inferno'
        else:
            scale = 'gray'
        fig = px.imshow(img, color_continuous_scale=scale)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        return command_message, fig, False, f'', False
