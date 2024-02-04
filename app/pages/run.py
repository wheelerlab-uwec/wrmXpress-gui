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
import subprocess
import yaml
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
                                html.H4("Configuration summary",
                                        className="text-center"),
                                html.Br(),
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
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button('Begin Analysis',
                                                   id='submit-analysis',
                                                      className="d-grid gap-2 col-8 mx-auto",
                                                   color="primary",
                                                   n_clicks=0),
                                    ),
                                    dbc.Col(
                                        dbc.Button('Cancel Analysis',
                                                   id='cancel-analysis',
                                                      className="d-grid gap-2 col-8 mx-auto",
                                                   color="danger",
                                                   n_clicks=0),
                                    ),
                                ]),
                                html.Br(),
                                dbc.Progress(
                                    id='progress-bar-run-page',
                                    striped=True,
                                    color="primary",
                                    value=0,
                                    animated=True,
                                ),
                                dcc.Loading(
                                    id="loading-2",
                                    children=[
                                        html.Div([
                                            dcc.Graph(
                                                id='image-analysis-preview',
                                                figure={'layout': layout},
                                                className='h-100 w-100'
                                            ),
                                        ])],
                                    type="cube",
                                    color='#3b4d61'
                                ),

                            ])
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4(
                                    "Run diagnosis", className="text-center"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='analysis-dropdown',
                                                placeholder='Select diagnostic image to view...'
                                            ),
                                            width=8
                                        ),
                                        dbc.Col(
                                            dbc.Button(
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
                                    "File:", className="card-subtitle"),
                                html.Br(),
                                dcc.Markdown(
                                    id='analysis-postview-message'),
                                dcc.Loading(
                                    id="loading-2",
                                    children=[
                                        html.Div([
                                            dcc.Graph(
                                                id='analysis-postview',
                                                figure={'layout': layout},
                                                className='h-100 w-100'
                                            ),
                                        ])],
                                    type="cube",
                                    color='#3b4d61'
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
    [Output('analysis-postview', 'figure'),
     Output('analysis-postview-message', 'children')],
    State('analysis-dropdown', 'value'),
    Input('load-analysis-img', 'n_clicks'),
    State('store', 'data'),
    allow_duplicate=True,
    prevent_initial_call=True,
)
def load_analysis_img(selection, n_clicks, store):
    volume = store['mount']
    platename = store['platename']

    if n_clicks:
        # check to see if selection option exists in output thumbs folder
        output_thumbs_path = Path(
            volume, f'output/thumbs/{platename}_{selection}.png'
        )
        print(output_thumbs_path)
        if os.path.exists(output_thumbs_path):
            img = np.array(Image.open(output_thumbs_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            return fig, f'```{output_thumbs_path}```'
    else:
        return None, None


@callback(
    Output('analysis-dropdown', 'options'),
    # update the option dropdown when the run analysis is clicked
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def get_options_analysis(nclicks, store):

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
