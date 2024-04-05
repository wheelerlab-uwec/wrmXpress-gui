########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, callback, dash_table
import pandas as pd
from pathlib import Path
import os

# components
from app.components.metadata_components import metadata_checklist

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

metadata_layout = dbc.Container(
    [
        html.Div(
            [   dbc.Row([
                dbc.Col([
                metadata_checklist,  # Metadata checklist, see metadata_components.py
                html.Br(),
                dbc.Row(
                    [
                        # Label for Plate Format
                        dbc.Col(
                            html.H6(
                                "Add new table:"  # Label for adding new table
                            )
                        ),
                    ],
                    align="center"  # Align the label to the center
                ),
                dbc.Row(
                    [
                        # First Column: Input for Total Number of Columns
                        dbc.Col(
                            dbc.Button(
                                "+",  # Add button
                                id="add-metadata-table-button",
                                className="me-2",
                            ),
                            width="auto",  # Width of the column
                            className='pe-0'
                        ),
                        dbc.Col(
                            # Add an editable input box here
                            dbc.Input(
                                id="uneditable-input-box",  # ID for the input box, indeed it is editable
                                placeholder='Title',
                                value="",
                                disabled=False  # Enable the input box
                            ),
                            width="auto",
                            className='ps-0'
                        ),
                    ],
                    align="center"  # Align the input box to the center
                ),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                            dbc.Button(
                                'Select All',  # Select All button
                                id='select-all-metadata-tables',
                                className='me-2',
                                color='primary'
                            ),
                        ],
                        width=3),
                        dbc.Col([
                            dbc.Button(
                                'Deselect All',  # Deselect All button
                                id='deselect-all-metadata-tables',
                                className='me-2',
                                color='primary',
                            ),
                        ],
                        width=3
                        ),
                ]),
                ],
                width=3,
                ),
                html.Br(),
                dbc.Col([
                dbc.Container([
                    dcc.Tabs(
                        id='metadata-tabs',
                        value='batch-data-tab',
                        children=[]  # Empty children for the tabs to be filled in by the user, see function below
                    )
                ]
                ),
                ],
                        width=9),
            ]),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Finalize Tables",  # Finalize Tables button
                                id="finalize-metadata-table-button",
                                className="flex",
                                # Color of the button (wrmXpress) blue
                                color='primary'
                            ),
                            width="auto"  # Width of the column
                        ),
                    ],
                    justify="center"  # Justify the button to the center
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            "Save metadata",  # Save metadata button
                            id='save-meta-data-to-csv',
                            # Color of the button (wrmXpress) blue
                            color='primary',
                            n_clicks=0  # Number of clicks
                        ),
                        width='auto'
                    )
                ),
                html.Br(),
                dbc.Alert(
                    children=[
                        "Metadata tables saved!"  # Metadata tables saved alert
                    ],
                    id="metadata-saved-alert",
                    is_open=False,  # Alert is not open
                    color="success",  # Color of the alert (green)
                    style={"textAlign": "center"}
                )
            ]
        )
    ],

    # adjust white space between metadata tab and tabs of metadata content
    style={"paddingTop": "80px"}
)