########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
preview_page_content = dbc.ModalBody(
    [
        # Preview page contents
        html.Div([
            html.Div([
                dbc.Row([
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("Input", className="text-center"),
                                    html.Br(),
                                    html.H6(
                                        "Path:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(id='input-path-output'),
                                    dcc.Graph(
                                        id='input-preview',
                                    ),
                                    dbc.Button('Load first input image',
                                               id='submit-val', className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
                                ]
                                )
                            )
                        ),

                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4(
                                        "Analysis", className="text-center"),
                                    html.Br(),
                                    html.H6(
                                        "Command:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(
                                        id='analysis-preview-message'),
                                    dcc.Graph(
                                        id='analysis-preview',
                                    ),
                                    dbc.Button(
                                        "Preview analysis", id="preview-button", className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
                                ]
                                )
                            ))
                        ])
            ]
            )
        ]
        )
    ],
)

########################################################################
####                                                                ####
####                             Modal                              ####
####                                                                ####
########################################################################
# Preview Page Modal
preview_page = dbc.Modal(
    [
        # Modal Header
        dbc.ModalHeader(
            "Preview Page"
        ),
        # Modal page contents from defined above
        preview_page_content,

        # Modal Footer
        dbc.ModalFooter([
            # Buttons for the Info Page Modal
            dbc.Button("Analyze all videos", id="run-button",
                       className="ml-auto", color="success"),
            dbc.Button("Close", id="close-preview-modal", className="ml-auto"),
        ]),
        html.Div(id="preview-page-status")
    ],
    id="preview-page-modal",
    size="xl"
)
