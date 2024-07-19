########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html

# importing utils
from app.utils.styling import layout, clear_alert_style

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

run_layout = dbc.ModalBody(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    "Configuration Summary",
                                                    style={"text-align": "center"},
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Begin analysis",
                                                        id="submit-analysis",
                                                        color="primary",
                                                        n_clicks=0,
                                                        style={
                                                            "margin-bottom": "10px",
                                                            "margin-top": "10px",
                                                            "text-align": "center",
                                                        },
                                                    ),
                                                    width={"offset": 2},
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Cancel analysis",
                                                        id="cancel-analysis",
                                                        color="danger",
                                                        n_clicks=0,
                                                        disabled=False,
                                                        style={
                                                            "margin-bottom": "10px",
                                                            "margin-top": "10px",
                                                            "margin-left": "-30px",
                                                            "text-align": "center",
                                                        },
                                                    ),
                                                    width={"offset": 0},
                                                ),
                                            ],
                                        ),
                                        dbc.Row(
                                            dbc.Progress(
                                                # Progress bar for run page
                                                id="progress-bar-run-page",
                                                striped=True,
                                                color="primary",
                                                value=0,
                                                animated=True,
                                            ),
                                        ),
                                        dbc.Row(
                                            [
                                                html.Div(
                                                    # Progress message for analysis
                                                    id="progress-message-run-page",
                                                    children=[
                                                        dcc.Markdown(  # Markdown for the progress message
                                                            children=[],
                                                            id="progress-message-run-page-markdown",
                                                            style={
                                                                "white-space": "pre-line",
                                                                "text-align": "left",
                                                            },
                                                        )
                                                    ],
                                                    className="div-with-scroll",
                                                    style={
                                                        "height": "490px",
                                                        "overflowY": "scroll",  # Always show vertical scrollbar
                                                        "margin-top": "10px",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                html.H4(
                                                    "Run Diagnosis",
                                                    style={"text-align": "center"},
                                                ),
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        # Dropdown for analysis
                                                        id="analysis-dropdown",
                                                        placeholder="Select diagnostic image to view...",
                                                    ),
                                                    width=8,
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        # Load Image button
                                                        id="load-analysis-img",
                                                        children="Load image",
                                                        disabled=True,
                                                    ),
                                                    width=4,
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H6(
                                                            # File
                                                            "File:",
                                                            className="card-subtitle",
                                                            style={"margin-top": "7px"},
                                                        )
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Alert(
                                                            # Alert for running file paths
                                                            id="run-page-file-paths-alert",
                                                            style=clear_alert_style,
                                                            is_open=True,
                                                            children=[
                                                                dcc.Markdown(
                                                                    # Progress message for progress file paths
                                                                    id="progress-message-run-page-for-analysis"
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Alert(
                                                            # Alert for file paths when updating dx image
                                                            id="run-page-file-paths-alert-update",
                                                            style=clear_alert_style,
                                                            is_open=False,
                                                            children=[
                                                                dcc.Markdown(
                                                                    # Message for analysis
                                                                    id="analysis-postview-message"
                                                                ),
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Alert(
                                                    id="first-view-of-analysis-alert",
                                                    color="light",
                                                    is_open=True,
                                                    children=[
                                                        html.Div(
                                                            [
                                                                dcc.Graph(
                                                                    # Image analysis preview
                                                                    id="image-analysis-preview",
                                                                    figure={
                                                                        "layout": layout
                                                                    },
                                                                    className="h-100 w-100",
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                ),
                                                dbc.Alert(
                                                    # Alert for additional view of analysis
                                                    id="additional-view-of-analysis-alert",
                                                    color="light",
                                                    is_open=True,
                                                    children=[
                                                        html.Div(
                                                            [
                                                                dcc.Graph(
                                                                    # Image analysis postview
                                                                    id="analysis-postview",
                                                                    figure={
                                                                        "layout": layout
                                                                    },
                                                                    className="h-100 w-100",
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ),
                            width=6,
                        ),
                    ],
                    className="h-90",
                ),
                dbc.Row(
                    [
                        dbc.Alert(
                            # Alert for no store
                            id="run-page-no-store-alert",
                            # Defines the color of the alert (red)
                            color="danger",
                            is_open=False,  # Defines if the alert is open or not
                            children=[
                                # Alert message
                                "No configuration found. Please go to the configuration page to set up the analysis."
                            ],
                        ),
                        dbc.Alert(
                            # Alert message
                            id="run-page-alert",
                            # Defines the color of the alert (red)
                            color="danger",
                            is_open=False,  # Defines if the alert is open or not
                            # Defines the duration of the alert in milliseconds (30 seconds)
                            duration=30000,
                        ),
                    ],
                    className="h-10",
                    style={"margin-top": "10px"},
                ),
            ],
            fluid=True,
        )
    ]
)
