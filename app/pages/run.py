########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import docker
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
import os
import dash
from dash.long_callback import DiskcacheLongCallbackManager

# importing utils
from app.utils.styling import layout

# Diskcache
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

dash.register_page(__name__, long_callback_manager=long_callback_manager)

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
                                    # Header of Configuration Summary
                                    "Configuration summary",
                                    className="text-center"
                                ),
                                html.Br(),
                                dcc.Markdown(
                                    # Imaging Mode
                                    id='img-mode-output',
                                    className="card-subtitle"
                                ),
                                dcc.Markdown(
                                    # File Structure
                                    id='file-structure-output',
                                    className='card-subtitle'
                                ),
                                dcc.Markdown(
                                    # Plate Format
                                    id='plate-format-output',
                                    className='card-subtitle'
                                ),
                                dcc.Markdown(
                                    # Image Masking
                                    id='img-masking-output',
                                    className='card-subtitle'
                                ),
                                dcc.Markdown(
                                    # Module Selection
                                    id='mod-selection-output',
                                    className='card-subtitle'
                                ),
                                dcc.Markdown(
                                    # Volume Name
                                    id='volume-name-output',
                                    className='card-subtitle'
                                ),
                                dcc.Markdown(
                                    # Plate Name
                                    id='plate-name-output',
                                    className='card-subtitle'
                                ),
                                dcc.Markdown(
                                    # Wells Content
                                    id='wells-content-output',
                                    className='card-subtitle'
                                ),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button(
                                            # Begin Analysis
                                            'Begin Analysis',
                                            id='submit-analysis',
                                            className="d-grid gap-2 col-8 mx-auto",
                                            color="primary", # Defines the color of the button (wrmxpress) blue
                                            n_clicks=0, # Defines the number of clicks
                                            disabled=False # Defines if the button is disabled or not
                                        ),
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            # Cancel Analysis
                                            'Cancel Analysis',
                                            id='cancel-analysis',
                                            className="d-grid gap-2 col-8 mx-auto",
                                            color="danger", # Defines the color of the button (wrmxpress) red
                                            n_clicks=0,
                                            disabled=True # Defines if the button is disabled or not
                                        ),
                                    ),
                                ]),
                                dbc.Alert(
                                    # Alert for no store
                                    id='run-page-no-store-alert',
                                    color='danger', # Defines the color of the alert (red)
                                    is_open=False, # Defines if the alert is open or not
                                    children=[
                                        # Alert message
                                        'No configuration found. Please go to the configuration page to set up the analysis.'
                                    ]
                                ),
                                html.Br(),
                                dbc.Row([
                                    dbc.Alert(
                                        # Alert message
                                        id='run-page-alert',
                                        color='danger', # Defines the color of the alert (red)
                                        is_open=False, # Defines if the alert is open or not
                                        duration=30000, # Defines the duration of the alert in milliseconds (30 seconds)
                                    ),
                                ]),
                                html.Br(),
                                dbc.Progress(
                                    # Progress bar for run page
                                    id='progress-bar-run-page',
                                    striped=True, # Defines if the progress bar is striped or not
                                    color="primary", # Defines the color of the progress bar (wrmxpress) blue
                                    value=0, # Defines the default value of the progress bar
                                    animated=True, # Defines if the progress bar is animated or not
                                ),
                            ]),
                            style={'height': '100%',
                                   'width': '99%'},
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4(
                                    # Header for Run Diagnosis
                                    "Run diagnosis",
                                    className="text-center"
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                # Dropdown for analysis
                                                id='analysis-dropdown',
                                                placeholder='Select diagnostic image to view...'
                                            ),
                                            width=8
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                # Load Image button
                                                id='load-analysis-img',
                                                children='Load Image',
                                                disabled=True
                                            ),
                                            width=4
                                        )
                                    ]
                                ),
                                html.Br(),
                                html.H6(
                                    # File
                                    "File:", className="card-subtitle"
                                ),
                                dcc.Markdown(
                                    # Progress message for progress file paths
                                    id='progress-message-run-page-for-analysis'
                                ),
                                html.Br(),
                                dcc.Markdown(
                                    # Message for analysis
                                    id='analysis-postview-message'
                                ),
                                dbc.Alert(
                                    # Alert for first view of analysis
                                    id='first-view-of-analysis-alert',
                                    color='light',
                                    is_open=True,
                                    children=[
                                        dcc.Graph(
                                            # Image analysis preview
                                            id='image-analysis-preview',
                                            figure={
                                                'layout': layout
                                            },
                                            className='h-100 w-100'
                                        ),
                                    ]
                                ),
                                dbc.Alert(
                                    # Alert for additional view of analysis
                                    id='additional-view-of-analysis-alert',
                                    color='light',
                                    is_open=False,
                                    children=[
                                        dcc.Loading(
                                            # Loading for analysis
                                            id="loading-2",
                                            children=[
                                                html.Div([
                                                    dcc.Graph(
                                                        # Image analysis postview
                                                        id='analysis-postview',
                                                        figure={
                                                            'layout': layout
                                                        },
                                                        className='h-100 w-100'
                                                    ),
                                                ])],
                                            type="cube",
                                            color='#3b4d61'
                                        ),
                                    ]
                                ),
                            ]),
                            style={'height': '100%',
                                   'width': '99%'},
                        )
                    ),
                ]),
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
    Output("cancel-analysis", 'n_clicks'),
    Input("cancel-analysis", 'n_clicks')
)
def cancel_analysis(n_clicks):
    """
    This function cancels the analysis by killing the most recent container.
    =========================================================================================
    Arguments:
        - n_clicks : int : The number of clicks
    =========================================================================================
    Returns:
        - n_clicks : int : The number of clicks
    """
    if n_clicks:
       # Connect to the Docker daemon
        client = docker.from_env()

        # Get a list of all running containers
        containers = client.containers.list()

        # Find the most recent container based on creation timestamp
        most_recent_container = max(
            containers, key=lambda c: c.attrs['Created'])

        # Kill the most recent container
        most_recent_container.kill()

    return n_clicks


@callback(
    [
        Output('analysis-postview', 'figure'),
        Output('analysis-postview-message', 'children'),
        Output('first-view-of-analysis-alert', 'is_open'),
        Output('additional-view-of-analysis-alert', 'is_open')
    ],
    State('analysis-dropdown', 'value'),
    Input('load-analysis-img', 'n_clicks'),
    State('store', 'data'),
    allow_duplicate=True,
    prevent_initial_call=True,
)
def load_analysis_img(selection, n_clicks, store):
    """
    This function loads the analysis image based on the selection.
    =========================================================================================
    Arguments:
        - selection : str : The selection
        - n_clicks : int : The number of clicks
        - store : dict : The store data
    =========================================================================================
    Returns:
        - fig : plotly.graph_objs._figure.Figure : The figure
        - f'```{output_thumbs_path}```' : str : The output thumbs path
        - is_open : bool : weather the (first-view-of-analysis) alert is open or not
            +- True : if the alert is open
            +- False : if the alert is not open
        - is_open : bool : weather the (additional view of analysis) alert is open or not
            +- True : if the alert is open
            +- False : if the alert is not open
    """
    # check to see if store exists
    if not store:
        return None, None, False, False

    # get the store from the data
    volume = store['mount']
    platename = store['platename']

    # check to see if selection option exists in output thumbs folder
    if n_clicks:

        # check to see if selection is plate
        if selection == 'plate':

            # obtaining the output plate path
            output_plate_path = Path(volume, f'output/thumbs/{platename}.png')

            # creating the image
            img = np.array(Image.open(output_plate_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)

            return fig, f'```{output_plate_path}```', False, True # return the figure and the output thumbs path

        # check to see if selection option exists in output thumbs folder
        output_thumbs_path = Path(
            volume, f'output/thumbs/{platename}_{selection}.png'
        )

        # check to see if the output thumbs path exists
        if os.path.exists(output_thumbs_path):

            # creating the image
            img = np.array(Image.open(output_thumbs_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)

            return fig, f'```{output_thumbs_path}```', False, True # return the figure and the output thumbs path
    else:
        return None, None, True, False


@callback(
    Output('analysis-dropdown', 'options'),

    # update the option dropdown when the run analysis is clicked
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def get_options_analysis(nclicks, store):
    """
    This function gets the options for the analysis.
    =========================================================================================
    Arguments:
        - nclicks : int : The number of clicks
        - store : dict : The store data
    =========================================================================================
    Returns:
        - options : list : The options
    """

    # check to see if store exists
    if not store:
        return []
    
    # get the store from the data
    motility = store['motility']
    segment = store['segment']
    platename = store['platename']

    # create the options
    selection_dict = {'motility': 'motility', 'segment': 'binary'}
    option_dict = {}

    # check to see if the button has been clicked (nclicks)
    if nclicks is not None:

        # iterate through the selection dictionary
        for selection in selection_dict.keys():
            if eval(selection) == 'True': # check to see if the selection is true
                option_dict[selection] = selection_dict[selection] # add the selection to the option dictionary
    dict_option = {v: k for k, v in option_dict.items()}
    dict_option['plate'] = 'plate' # add the plate to the option dictionary
    return dict_option # return the option dictionary


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
    """
    This function updates the results message for the run page.
    =========================================================================================
    Arguments:
        - nclicks : int : The number of clicks
        - store : dict : The store data
    =========================================================================================
    Returns:
        - results : list : The results
    """
    # check to see if store exists
    if not store:
        return None, None, None, None, None, None, None, None

    # checking to see if the rows and cols are None
    if store['rows'] == None:
        rows = 8
    if store['cols'] == None:
        cols = 12

    # get the store from the data and create the results
    img_mode = f'Imaging Mode: {store["img_mode"]}'
    file_structure = f'File Structure: {store["file_structure"]}'
    plate_format = f'Plate Format: Rows = {rows}, Cols = {cols}'
    img_masking = f'Image Masking: {store["img_masking"]}'
    mod_selection = f'Module Selection: {store["motility"]}'
    volume = f'Volume: {store["mount"]}'
    platename = f'Platename: {store["platename"]}'
    wells = f'Wells: {store["wells"]}'

    # create a list of the results
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
    if nclicks: # check to see if the button has been clicked
        return results # return the results
