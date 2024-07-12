########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html
from app.utils.styling import layout

# Assuming we have a fixed height for the headers and buttons in CSS
fixed_header_class = "fixed-header"
fixed_button_class = "fixed-button"

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

preview_layout = dbc.ModalBody(
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
                                                    "Input Preview",
                                                    style={"text-align": "center"},
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Preview analysis",  # Button to preview analysis
                                                        id="submit-val",
                                                        color="primary",  # Color of the button (wrmXpress) blue
                                                        n_clicks=0,  # Number of times the button has been clicked
                                                        style={
                                                            "margin-bottom": "10px",
                                                            "margin-top": "10px",
                                                            "text-align": "center",
                                                        },
                                                    ),
                                                )
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                html.P("Raw image:"),
                                                dcc.Markdown(id="input-path-output"),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Alert(
                                                    id="input-img-view-alert",  # Alert for input image view
                                                    color="light",  # Color of the alert (light)
                                                    is_open=True,  # Whether the alert is open
                                                    children=[
                                                        dcc.Loading(
                                                            id="loading-1",  # Loading element id
                                                            children=[
                                                                html.Div(
                                                                    [
                                                                        dcc.Graph(
                                                                            # Graph for input preview
                                                                            id="input-preview",
                                                                            figure={
                                                                                "layout": layout
                                                                            },
                                                                            className="h-100 w-100",
                                                                        )
                                                                    ]
                                                                ),
                                                            ],
                                                            type="cube",  # Type of loading element (cube)
                                                            color="#3b4d61",  # Color of the loading element (wrmXpress) blue
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ],
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
                                                    "Analysis Preview",
                                                    style={
                                                        "text-align": "center",
                                                        "margin-bottom": "20px",
                                                    },
                                                ),
                                            ],
                                            style={"height": "20%"},
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="preview-dropdown",  # Dropdown for preview
                                                        placeholder="Select diagnostic image to preview...",  # Placeholder for the dropdown
                                                        style={"textAlign": "left"},
                                                    ),
                                                    width=4,
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Load image",  # Button to load image
                                                        id="preview-change-img-button",
                                                        color="primary",  # Color of the button (wrmXpress) blue
                                                        disabled=True,  # Whether the button is disabled
                                                        n_clicks=0,  # Number of times the button has been clicked
                                                    ),
                                                    width={"offset": 4, "size": 4},
                                                ),
                                            ],
                                            style={
                                                "margin-bottom": "6px",
                                            },
                                        ),
                                        dbc.Row(
                                            [
                                                html.P("Path to diagnostic image:"),
                                                dcc.Markdown(
                                                    id="analysis-preview-message"
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Alert(
                                                    id="preview-img-view-alert",  # Alert for preview image view
                                                    color="light",
                                                    is_open=True,
                                                    children=[
                                                        dcc.Loading(
                                                            # Loading element for preview image
                                                            id="loading-2",
                                                            children=[
                                                                html.Div(
                                                                    [
                                                                        dcc.Graph(
                                                                            # Graph for analysis preview
                                                                            id="analysis-preview",
                                                                            figure={
                                                                                "layout": layout
                                                                            },
                                                                            className="h-100 w-100",
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            type="cube",  # Type of loading element (cube)
                                                            color="#3b4d61",  # Color of the loading element (wrmXpress) blue
                                                        ),
                                                    ],
                                                ),
                                                dbc.Alert(
                                                    # Alert for post analysis first well image view
                                                    id="post-analysis-first-well-img-view-alert",
                                                    color="light",  # Color of the alert (light)
                                                    is_open=False,  # Whether the alert is open
                                                    children=[
                                                        dcc.Loading(
                                                            # Loading element for post analysis first well image
                                                            id="loading-2",
                                                            children=[
                                                                html.Div(
                                                                    [
                                                                        dcc.Graph(
                                                                            # Graph for post analysis first well
                                                                            id="analysis-preview-other-img",
                                                                            figure={
                                                                                "layout": layout
                                                                            },
                                                                            className="h-100 w-100",
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            type="cube",  # Type of loading element (cube)
                                                            color="#3b4d61",  # Color of the loading element (wrmXpress) blue
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ),
                        ),
                    ],
                    className="h-90",
                ),
                dbc.Row(
                    [
                        dbc.Alert(
                            # Alert for resolving error issue preview
                            id="resolving-error-issue-preview",
                            is_open=False,
                            color="alert",
                            duration=6000,
                        ),
                        dbc.Alert(
                            # Alert for no store data
                            id="view-docker-logs",
                            is_open=False,
                            color="alert",
                            duration=30000,
                        ),
                        dbc.Alert(
                            id="no-store-data-alert",
                            color="danger",  # Color of the alert (red)
                            is_open=False,  # Whether the alert is open
                            children=[
                                # Default Alert message
                                "No configuration found. Please go to the configuration page to set up the analysis."
                            ],
                        ),
                    ],
                    className="h-10",
                ),
            ],
            style={"height": "100vh"},
        )
    ]
)

#                         dbc.Col(
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#                                         html.Div(
#                                             html.H4(
#                                                 "Analysis preview",  # Header of analysis preview
#                                                 className=f"text-center {fixed_header_class} mb-5",
#                                                 style={
#                                                     "margin-top": "10px",
#                                                 },
#                                             ),
#                                         ),
#                                         html.Div(
#                                             dbc.Row(
#                                                 [
#                                                     dbc.Col(
#                                                         dcc.Dropdown(
#                                                             id="preview-dropdown",  # Dropdown for preview
#                                                             placeholder="Select diagnostic image to preview...",  # Placeholder for the dropdown
#                                                             style={"textAlign": "left"},
#                                                         ),
#                                                     ),
#                                                     dbc.Col(
#                                                         dbc.Button(
#                                                             "Load image",  # Button to load image
#                                                             id="preview-change-img-button",
#                                                             color="primary",  # Color of the button (wrmXpress) blue
#                                                             disabled=True,  # Whether the button is disabled
#                                                             n_clicks=0,  # Number of times the button has been clicked
#                                                         ),
#                                                     ),
#                                                 ],
#                                                 style={
#                                                     "margin-bottom": "10px",
#                                                     "margin-top": "10px",
#                                                 },
#                                             ),
#                                             style={
#                                                 "text-align": "center",
#                                                 "height": "center",
#                                             },
#                                         ),
#                                         html.H6(
#                                             "Path to diagnostic image:",
#                                             className="card-subtitle",
#                                         ),
#                                         dcc.Markdown(
#                                             # Output of the command id displayed in markdown
#                                             id="analysis-preview-message"
#                                         ),
#                                         dbc.Alert(
#                                             id="preview-img-view-alert",  # Alert for preview image view
#                                             color="light",
#                                             is_open=True,
#                                             children=[
#                                                 dcc.Loading(
#                                                     # Loading element for preview image
#                                                     id="loading-2",
#                                                     children=[
#                                                         html.Div(
#                                                             [
#                                                                 dcc.Graph(
#                                                                     # Graph for analysis preview
#                                                                     id="analysis-preview",
#                                                                     figure={
#                                                                         "layout": layout
#                                                                     },
#                                                                     className="h-100 w-100",
#                                                                 ),
#                                                             ]
#                                                         )
#                                                     ],
#                                                     type="cube",  # Type of loading element (cube)
#                                                     color="#3b4d61",  # Color of the loading element (wrmXpress) blue
#                                                 ),
#                                             ],
#                                         ),
#                                         dbc.Alert(
#                                             # Alert for post analysis first well image view
#                                             id="post-analysis-first-well-img-view-alert",
#                                             color="light",  # Color of the alert (light)
#                                             is_open=False,  # Whether the alert is open
#                                             children=[
#                                                 dcc.Loading(
#                                                     # Loading element for post analysis first well image
#                                                     id="loading-2",
#                                                     children=[
#                                                         html.Div(
#                                                             [
#                                                                 dcc.Graph(
#                                                                     # Graph for post analysis first well
#                                                                     id="analysis-preview-other-img",
#                                                                     figure={
#                                                                         "layout": layout
#                                                                     },
#                                                                     className="h-100 w-100",
#                                                                 ),
#                                                             ]
#                                                         )
#                                                     ],
#                                                     type="cube",  # Type of loading element (cube)
#                                                     color="#3b4d61",  # Color of the loading element (wrmXpress) blue
#                                                 ),
#                                             ],
#                                         ),
#                                     ],
#                                     className="aligning-preview-page-content",
#                                 ),
#                                 style={"height": "100%", "width": "99%"},
#                             ),
#                             width={"size": 6},
#                         ),
#                     ]
#                 ),
#                 dbc.Alert(
#                     # Alert for resolving error issue preview
#                     id="resolving-error-issue-preview",
#                     is_open=False,
#                     color="alert",
#                     duration=6000,
#                 ),
#                 dbc.Alert(
#                     # Alert for no store data
#                     id="view-docker-logs",
#                     is_open=False,
#                     color="alert",
#                     duration=30000,
#                 ),
#                 dbc.Alert(
#                     id="no-store-data-alert",
#                     color="danger",  # Color of the alert (red)
#                     is_open=False,  # Whether the alert is open
#                     children=[
#                         # Default Alert message
#                         "No configuration found. Please go to the configuration page to set up the analysis."
#                     ],
#                 ),
#             ]
#         )
#     ]
# )
