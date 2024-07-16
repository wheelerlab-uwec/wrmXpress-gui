########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html

# importing utils
from app.utils.styling import layout

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

run_layout = dbc.ModalBody(
    [
        # Preview page contents
        html.Div(
            [
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            # Header of Configuration Summary
                                                            "Configuration Summary",
                                                            className="text-center",
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dbc.Button(
                                                                        # Begin Analysis
                                                                        "Begin analysis",
                                                                        id="submit-analysis",
                                                                        className="d-grid gap-2 col-8 mx-auto",
                                                                        # Defines the color of the button (wrmxpress) blue
                                                                        color="primary",
                                                                        n_clicks=0,  # Defines the number of clicks
                                                                        disabled=False,  # Defines if the button is disabled or not
                                                                    ),
                                                                ),
                                                                dbc.Col(
                                                                    dbc.Button(
                                                                        # Cancel Analysis
                                                                        "Cancel analysis",
                                                                        id="cancel-analysis",
                                                                        className="d-grid gap-2 col-8 mx-auto",
                                                                        # Defines the color of the button (wrmxpress) red
                                                                        color="danger",
                                                                        n_clicks=0,
                                                                        disabled=True,  # Defines if the button is disabled or not
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        dbc.Progress(
                                                            # Progress bar for run page
                                                            id="progress-bar-run-page",
                                                            striped=True,  # Defines if the progress bar is striped or not
                                                            # Defines the color of the progress bar (wrmxpress) blue
                                                            color="primary",
                                                            value=0,  # Defines the default value of the progress bar
                                                            animated=True,  # Defines if the progress bar is animated or not
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
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
                                                        dbc.Row(
                                                            [
                                                                dbc.Alert(
                                                                    # Alert message
                                                                    id="run-page-alert",
                                                                    # Defines the color of the alert (red)
                                                                    color="danger",
                                                                    is_open=False,  # Defines if the alert is open or not
                                                                    # Defines the duration of the alert in milliseconds (30 seconds)
                                                                    duration=30000,
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
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
                                                        "height": "470px",
                                                        "overflowY": "scroll",  # Always show vertical scrollbar
                                                        "margin-top": "10px",
                                                    },
                                                ),
                                            ],
                                            className="aligning-run-page-content",
                                        ),
                                        style={"height": "100%", "width": "99%"},
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            # Header for Run Diagnosis
                                                            "Run Diagnosis",
                                                            className="text-center",
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
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
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        html.H6(
                                                            # File
                                                            "File:",
                                                            className="card-subtitle",
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.Markdown(
                                                            # Progress message for progress file paths
                                                            id="progress-message-run-page-for-analysis"
                                                        ),
                                                        dcc.Markdown(
                                                            # Message for analysis
                                                            id="analysis-postview-message"
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        dbc.Alert(
                                                            # Alert for first view of analysis
                                                            id="first-view-of-analysis-alert",
                                                            color="light",
                                                            is_open=True,
                                                            children=[
                                                                dcc.Graph(
                                                                    # Image analysis preview
                                                                    id="image-analysis-preview",
                                                                    figure={
                                                                        "layout": layout
                                                                    },
                                                                    className="h-100 w-100",
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Alert(
                                                            # Alert for additional view of analysis
                                                            id="additional-view-of-analysis-alert",
                                                            color="light",
                                                            is_open=False,
                                                            children=[
                                                                dcc.Loading(
                                                                    # Loading for analysis
                                                                    id="loading-2",
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
                                                                    type="cube",
                                                                    color="#3b4d61",
                                                                ),
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            className="aligning-run-page-content",
                                        ),
                                        style={"height": "100%", "width": "99%"},
                                    ),
                                    width=6,
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)
