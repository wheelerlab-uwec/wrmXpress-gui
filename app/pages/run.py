########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
import os
import dash
from dash.long_callback import DiskcacheLongCallbackManager

# importing utils
from app.utils.styling import layout
from app.utils.callback_functions import send_ctrl_c

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
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button(
                                            # Begin Analysis
                                            'Begin Analysis',
                                            id='submit-analysis',
                                            className="d-grid gap-2 col-8 mx-auto",
                                            # Defines the color of the button (wrmxpress) blue
                                            color="primary",
                                            n_clicks=0,  # Defines the number of clicks
                                            disabled=False  # Defines if the button is disabled or not
                                        ),
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            # Cancel Analysis
                                            'Cancel Analysis',
                                            id='cancel-analysis',
                                            className="d-grid gap-2 col-8 mx-auto",
                                            # Defines the color of the button (wrmxpress) red
                                            color="danger",
                                            n_clicks=0,
                                            disabled=True  # Defines if the button is disabled or not
                                        ),
                                    ),
                                ]),
                                dbc.Alert(
                                    # Alert for no store
                                    id='run-page-no-store-alert',
                                    # Defines the color of the alert (red)
                                    color='danger',
                                    is_open=False,  # Defines if the alert is open or not
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
                                        # Defines the color of the alert (red)
                                        color='danger',
                                        is_open=False,  # Defines if the alert is open or not
                                        # Defines the duration of the alert in milliseconds (30 seconds)
                                        duration=30000,
                                    ),
                                ]),
                                html.Br(),
                                dbc.Progress(
                                    # Progress bar for run page
                                    id='progress-bar-run-page',
                                    striped=True,  # Defines if the progress bar is striped or not
                                    # Defines the color of the progress bar (wrmxpress) blue
                                    color="primary",
                                    value=0,  # Defines the default value of the progress bar
                                    animated=True,  # Defines if the progress bar is animated or not
                                ),
                                html.Br(),
                                html.Div(
                                    # Progress message for analysis
                                    id='progress-message-run-page',
                                    children=[
                                        dcc.Markdown(  # Markdown for the progress message
                                            children=[],
                                            id='progress-message-run-page-markdown',
                                            style={'white-space': 'pre-line',
                                                   'text-align': 'left'}
                                        )
                                    ],
                                    className='div-with-scroll',
                                    style={
                                        'height': '500px',
                                        'overflowY': 'scroll',  # Always show vertical scrollbar
                                    }
                                )
                            ]),
                            style={'height': '100%',
                                   'width': '99%'},
                        ),
                        width=6
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
                        ),
                        width=6
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
    This function cancels the analysis by typing "Control" + "C" in the terminal.
    =========================================================================================
    Arguments:
        - n_clicks : int : The number of clicks
    =========================================================================================
    Returns:
        - n_clicks : int : The number of clicks
    """
    if n_clicks:

        # Replace `1234` with the actual PID
        send_ctrl_c(1234)
        print('Control + C', 'wrmxpress analysis cancelled')

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

            # return the figure and the output thumbs path
            return fig, f'```{output_plate_path}```', False, True

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

            # return the figure and the output thumbs path
            return fig, f'```{output_thumbs_path}```', False, True
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
    pipeline_selection = store['pipeline_selection']
    if pipeline_selection == 'motility':

        # create the options
        selection_dict = {'motility': 'motility', 'segment': 'binary', 'plate': 'plate'}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict  # return the option dictionary
    elif pipeline_selection == 'fecundity':
            
        # create the options
        selection_dict = {'binary': 'binary', 'plate': 'plate'}
    
        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == 'tracking':
            
        # create the options
        selection_dict = {'tracks': 'tracks', 'plate': 'plate'}
        
        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == "wormsize_intensity_cellpose":
                
        # create the options
        selection_dict = {'plate': 'plate', 'straightened_worms': 'straightened_worms'}
        
         # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == 'mf_celltox':
                
            # create the options
            selection_dict = {'plate': 'plate'}
            
            # check to see if the button has been clicked (nclicks)
            if nclicks is not None:
                return selection_dict
    elif pipeline_selection == 'wormsize':
        # create the options
        selection_dict = {'plate': 'plate', 'straightened_worms': 'straightened_worms'}
        
         # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == 'feeding':
       # obtain the wavelength options
        volume = store['mount']
        platename = store['platename']
        thumbs_file_path = Path(volume, 'output/thumbs/')
        
        # create the options
        selection_dict = {
            'plate': 'plate',
            'straightened_worms': 'straightened_worms',
        }

        # New code to add: list all matching files and extract unique identifiers
        pattern = f"{platename}*.png"
        # Using glob to match the pattern
        all_files = list(thumbs_file_path.glob(pattern))
        # Extracting unique identifiers from filenames (e.g., _w1, _w2, etc.)
        wavelengths = set()
        for file_path in all_files:
            parts = file_path.name.split('_')
            if len(parts) > 1 and parts[-1].startswith('w') and parts[-1].endswith('.png'):
                wavelengths.add(parts[-1].replace('.png', ''))

        # Adding these wavelengths to the selection dictionary
        for wave in sorted(wavelengths):
            selection_key = f'wavelength_{wave}'  # Format the key as you see fit
            selection_dict[selection_key] = wave

        # Assuming nclicks is some condition you've checked elsewhere
        nclicks = 1
        if nclicks is not None:
            return selection_dict
    else:   
        return {'plate': 'plate'}
