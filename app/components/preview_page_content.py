########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
preview_page_content = dbc.ModalBody(
    [
        html.Div([
            dbc.Button('Load first input image',
                       id='submit-val', className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
            html.Br(),
            html.Br(),
            html.Div([
                dbc.Row([
                        dbc.Col([
                            html.P(id='input-path-output'),
                            "Input image: ",
                            dcc.Graph(
                                id='input-preview',
                                # style={'height':'30%', 'width':'30%'}
                            )
                        ]),
                        dbc.Col([
                            html.P(),
                            "Analysis preview: ",
                            dcc.Graph(
                                id='analysis-preview',
                                # style={'height':'30%', 'width':'30%'}
                            )
                        ])
                        ])
            ]
            )]),
        html.Br(),
        html.Div([
            dcc.Markdown("Write a YAML for running wrmXpress remotely. Include a full path and file name ending in `.yaml`."),
            dbc.Input(id="file-path-for-preview-yaml-file",
                      placeholder="Enter the full save path...", type="text"),
            html.Br(), 
            dcc.Markdown("Enter the path to the `wrapper.py` file provided by wrmXpress."),
            dbc.Input(id="file-path-to-wrapper-py",
                      placeholder="Enter the full path...", type="text"),
        ])
    ],
)

########################################################################
####                                                                ####
####                             Modal                              ####
####                                                                ####
########################################################################
# Create the Preview Page Modal
preview_page = dbc.Modal(
    [
        dbc.ModalHeader(
            "Preview Page"
        ),
        preview_page_content,

        dbc.ModalFooter([
            # Buttons for the Info Page Modal
            dbc.Button("Preview", id="preview-preview-button",
                       className="ml-auto", color="success"),
            dbc.Button("Close", id="close-preview-modal", className="ml-auto"),
        ]),
        html.Div(id="preview-page-status")  # Placeholder for saving status
    ],
    id="preview-page-modal",
    size="xl"
)