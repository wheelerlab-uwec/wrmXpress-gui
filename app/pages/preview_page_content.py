########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
import yaml
from dash.dependencies import Input, Output, State
import os
import pathlib
import numpy as np
import plotly.express as px
from PIL import Image


########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
preview_page_content = dbc.ModalBody(
    [
        # Preview page contents
        html.Div([
            # button for loadining image
            dbc.Button('Load first input image',
                       id='submit-val', className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
            html.Br(),
            html.Br(),
            html.Div([
                dbc.Row([
                        dbc.Col([
                            html.P(id='input-path-output'),
                            "Input image: ",
                            # First image for selected well
                            dcc.Graph(
                                id='input-preview',
                                # style={'height':'30%', 'width':'30%'}
                            )
                        ]),
                        dbc.Col([
                            html.P(),
                            "Analysis preview: ",
                            # Second image of wrmXpress product after analysis of same well
                            dcc.Graph(
                                id='analysis-preview',
                                # style={'height':'30%', 'width':'30%'}
                            )
                        ])
                        ])
            ]
            )])
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
            dbc.Button("Preview", id="preview-preview-button",
                       className="ml-auto", color="success"),
            dbc.Button("Close", id="close-preview-modal", className="ml-auto"),
        ]),
        html.Div(id="preview-page-status")  
    ],
    id="preview-page-modal",
    size="xl"
)

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################

    
def load_first_img(app):
    # Load first image in Preview page
    @app.callback(
        Output('input-path-output', 'children'),
        Output('input-preview', 'figure'),
        Input('submit-val', 'n_clicks'),
        State("input-directory", "value"),
        prevent_initial_call=True
    )
    def update_preview_image(n_clicks, input_dir_state):

        path_split = pathlib.PurePath(str(input_dir_state))
        dir_path = str(path_split.parts[-1])
        plate_base = dir_path.split("_", 1)[0]

        if n_clicks >= 1:
            # assumes IX-like file structure
            img_path = input_dir_state + f'/TimePoint_1/{plate_base}_A01.TIF'
            img = np.array(Image.open(img_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            return f'Input path: {input_dir_state}', fig
        n_clicks = 0