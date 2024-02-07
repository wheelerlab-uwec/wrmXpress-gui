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
import os
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
                                    html.H4(
                                        "Input preview", # Header of input preview
                                        className="text-center mb-5"
                                    ),
                                    dbc.Row([
                                        dbc.Button(
                                            'Preview Analysis', # Button to preview analysis
                                            id='submit-val',
                                            className="d-grid gap-2 col-6 mx-auto",
                                            color="primary", # Color of the button (wrmXpress) blue
                                            n_clicks=0 # Number of times the button has been clicked
                                        ),
                                    ]),
                                    html.Br(),
                                    dbc.Alert(
                                        id='no-store-data-alert',
                                        color='danger', # Color of the alert (red)
                                        is_open=False, # Whether the alert is open
                                        children=[
                                            # Default Alert message
                                            "No configuration found. Please go to the configuration page to set up the analysis."
                                        ]
                                    ),
                                    html.H6(
                                        "Path:", # Header of path
                                        className="card-subtitle"
                                    ),
                                    html.Br(),
                                    dcc.Markdown(
                                        id='input-path-output' # Output of the path id displayed in markdown
                                    ),
                                    html.Div(
                                        dbc.Alert(
                                            id='input-img-view-alert', # Alert for input image view
                                            color='light', # Color of the alert (light)
                                            is_open=True, # Whether the alert is open
                                            children=[
                                                dcc.Loading(
                                                    id='loading-1', # Loading element id
                                                    children=[
                                                        html.Div([
                                                            dcc.Graph(
                                                                # Graph for input preview
                                                                id='input-preview',
                                                                figure={
                                                                    'layout': layout
                                                                },
                                                                className='h-100 w-100'
                                                            )
                                                        ]),
                                                    ],
                                                    type='cube', # Type of loading element (cube)
                                                    color='#3b4d61' # Color of the loading element (wrmXpress) blue
                                                ),
                                            ]
                                        ),
                                    ),
                                ]
                                ),
                                # Style of the card
                                style={'height': '100%',
                                       'width': '99%'},
                            ),
                            width={'size': 6},
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4(
                                        "Analysis preview", # Header of analysis preview
                                        className="text-center"
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='preview-dropdown', # Dropdown for preview
                                                    placeholder='Select image to preview...' # Placeholder for the dropdown
                                                ),
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "Load Image", # Button to load image
                                                    id="preview-change-img-button",
                                                    className="d-grid gap-2 col-6 mx-auto",
                                                    color="primary", # Color of the button (wrmXpress) blue
                                                    disabled=True, # Whether the button is disabled
                                                    n_clicks=0 # Number of times the button has been clicked
                                                ),
                                            )
                                        ]
                                    ),
                                    html.Br(),
                                    html.H6(
                                        "Command:", # Header of command
                                        className="card-subtitle"
                                    ),
                                    html.Br(),
                                    dcc.Markdown(
                                        # Output of the command id displayed in markdown
                                        id='analysis-preview-message'
                                    ),
                                    dbc.Alert(
                                        id='preview-img-view-alert', # Alert for preview image view
                                        color='light',
                                        is_open=True,
                                        children=[
                                            dcc.Loading(
                                                # Loading element for preview image
                                                id="loading-2",
                                                children=[
                                                    html.Div([
                                                        dcc.Graph(
                                                            # Graph for analysis preview
                                                            id='analysis-preview',
                                                            figure={
                                                                'layout': layout
                                                            },
                                                            className='h-100 w-100'
                                                        ),
                                                    ])],
                                                type="cube", # Type of loading element (cube)
                                                color='#3b4d61' # Color of the loading element (wrmXpress) blue
                                            ),
                                        ],
                                    ),
                                    dbc.Alert(
                                        # Alert for post analysis first well image view
                                        id='post-analysis-first-well-img-view-alert',
                                        color='light', # Color of the alert (light)
                                        is_open=False, # Whether the alert is open 
                                        children=[
                                            dcc.Loading(
                                                # Loading element for post analysis first well image
                                                id="loading-2",
                                                children=[
                                                    html.Div([
                                                        dcc.Graph(
                                                            # Graph for post analysis first well
                                                            id='analysis-preview-other-img',
                                                            figure={
                                                                'layout': layout
                                                            },
                                                            className='h-100 w-100'
                                                        ),
                                                    ])],
                                                type="cube", # Type of loading element (cube)
                                                color='#3b4d61' # Color of the loading element (wrmXpress) blue
                                            ),
                                        ],
                                    ),
                                    dbc.Alert(
                                        # Alert for resolving error issue preview
                                        id='resolving-error-issue-preview',
                                        is_open=False,
                                        color='success',
                                        duration=6000
                                    ),
                                    dbc.Alert(
                                        # Alert for no store data
                                        id='view-docker-logs',
                                        is_open=False,
                                        color='success',
                                        duration=30000
                                    ),
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
    Output("no-store-data-alert", 'is_open'),
    Output("submit-val", "disabled"),
    State("preview-dropdown", 'value'),
    Input("preview-change-img-button", 'n_clicks'),
    State('store', 'data'),
)
def update_analysis_preview_imgage(selection, nclicks, store):
    """
    This function updates the analysis preview image based on the selection
    =======================================================================
    Arguments:
        - selection : str : The selection from the dropdown
        - nclicks : int : The number of times the button has been clicked
        - store : dict : The store data
    =======================================================================
    Returns:
        - fig : plotly.graph_objs._figure.Figure : The figure to be displayed
        - is_open : bool : Whether the (preview-imgage) alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - is_open : bool : Whether the (post analysis first well) alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - is_open : bool : Whether the (no store )alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - disabled : bool : Whether the button is disabled
            +- True : The button is disabled
            +- False : The button is enabled
    """
    # Check if store is empty
    if not store:
        return None, True, False, True, True

    if nclicks:  # If the button has been clicked

        # Get the store data
        volume = store['mount']
        platename = store['platename']
        wells = store["wells"]

        # assumes IX-like file structure
        img_path = Path(
            f'{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}_{selection}.png'
        )

        # Check if the image exists
        if os.path.exists(img_path):

            # checking the selection and changing the scale accordingly
            if selection == 'motility':
                scale = 'inferno'
            else:
                scale = 'gray'

            # Open the image and create a figure
            img = np.array(Image.open(img_path))
            fig = px.imshow(img, color_continuous_scale=scale)
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)

            # Return the figure and the open status of the alerts
            return fig, False, True, False, ''
        else:
            return None, True, False, False, False
    return None, True, False,  False, False


@callback(
    Output('input-path-output', 'children'),
    Output('input-preview', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def update_preview_image(n_clicks, store):
    """
    This function updates the input preview image
    =======================================================
    Arguments:
        - n_clicks : int : The number of times the button has been clicked
        - store : dict : The store data
    =======================================================
    Returns:
        - str : The path to the image
        - fig : plotly.graph_objs._figure.Figure : The figure to be displayed
    """
    # Obtaining the store data
    wells = store['wells']  # Get the wells
    first_well = wells[0].replace(', ', '')  # Get the first well
    platename = store['platename']  # Get the platename
    plate_base = platename.split("_", 1)[0]  # Get the plate base
    volume = store['mount']  # Get the volume

    # Check if the button has been clicked
    if n_clicks >= 1:

        # assumes IX-like file structure
        img_path = Path(
            volume, f'{platename}/TimePoint_1/{plate_base}_{first_well}.TIF'
        )

        # Open the image and create a figure
        img = np.array(Image.open(img_path))
        fig = px.imshow(img, color_continuous_scale="gray")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return f'```{img_path}```', fig  # Return the path and the figure
    n_clicks = 0


@callback(
    Output('preview-dropdown', 'options'),

    # update the option dropdown when the previous load is clicked
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def get_options(nclicks, store):
    """
    This function gets the options for the dropdown
    =======================================================
    Arguments:
        - nclicks : int : The number of times the button has been clicked
        - store : dict : The store data
    =======================================================
    Returns:
        - list : The options for the dropdown
    """
    # Get the store data
    motility = store['motility']
    segment = store['segment']

    # Create a dictionary of the options
    selection_dict = {'motility': 'motility', 'segment': 'binary'}
    option_dict = {}

    # Check if the button has been clicked
    if nclicks is not None:

        # Iterate through the selection dictionary
        for selection in selection_dict.keys():

            # Check if the selection is True
            if eval(selection) == 'True':
                # Add the selection to the option dictionary
                option_dict[selection] = selection_dict[selection]

    # Return the options
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
    """
    This function runs the analysis of the first well if the first well has not been run before and the button has been clicked
    =======================================================
    Arguments:
        - nclicks : int : The number of times the button has been clicked
        - store : dict : The store data
    =======================================================
    Returns:
        - str : The command message
        - fig : plotly.graph_objs._figure.Figure : The figure to be displayed
        - is_open : bool : Whether the alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - str : The message to be displayed
        - disabled : bool : Whether the button is disabled
            +- True : The button is disabled
            +- False : The button is enabled
    """

    # Obtain the store data
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    motility_selection = store['motility']
    segment_selection = store['segment']

    # Check if motility or segment selection is True
    if motility_selection == 'True':
        selection1 = '_motility'
        selection = 'motility'
    elif segment_selection == 'True':
        selection1 = '_segment'
        selection = 'segment'
    else:
        selection1 = ''

    # Check if the button has been clicked
    if nclicks:

        # Checking if wrmXpress container exists and is the latest image
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
            volume, 'work', f'{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection1}.png'
        )

        # Check if the first well path exists
        if os.path.exists(first_well_path):

            # checking the selection and changing the scale accordingly
            if selection == 'motility':
                scale = 'inferno'
            else:
                scale = 'gray'

            # Open the image and create a figure
            img = np.array(Image.open(first_well_path))
            fig = px.imshow(img, color_continuous_scale=scale)
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            # Return the path and the figure and the open status of the alerts
            return f"```{first_well_path}```", fig, False, f'', False

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

        # Checking if input folder exists, and if not, create it,
        # then subsequently copy the images into this folder
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

        # filepath of the yaml file
        yaml_file = Path(platename + '.yml')

        print(client)  # Print the client

        # The command to be run
        command = f"python wrmXpress/wrapper.py {preview_yaml_platename} {platename}"
        # The command message
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
            volume, 'work', f'{platename}/{first_well}/img/{platename}_{first_well}{selection1}.png')

        # Wait for the image to be created
        while not os.path.exists(img_path):
            time.sleep(1)

        # checking the selection and changing the scale accordingly
        img = np.array(Image.open(img_path))
        if selection == 'motility':
            scale = 'inferno'
        else:
            scale = 'gray'

        # Open the image and create a figure
        fig = px.imshow(img, color_continuous_scale=scale)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        # Return the command message, the figure, and the open status of the alerts
        return command_message, fig, False, f'', False
