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
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button('Begin Analysis',
                                           id='submit-analysis',
                                           className="d-grid gap-2 col-6 mx-auto",
                                           color="primary",
                                           n_clicks=0),
                                    ),
                                    dbc.Col(
                                        dbc.Button('Cancel Analysis',
                                                   id = 'cancel-analysis',
                                                    className="d-grid gap-2 col-6 mx-auto",
                                                    color="danger",
                                                    n_clicks=0),
                                    ),
                                ]),
                                html.Br(),
                                dbc.Alert(children=[
                                    dbc.Progress(
                                        id='progress-bar-run-page',
                                        striped=True,
                                        color="primary",
                                        value=50,
                                        animated=True,
                                    ),
                                ], is_open=True, color='success', id='alert-progress-bar-run-page',
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

