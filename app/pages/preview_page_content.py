########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import docker
from pathlib import Path
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

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################

def load_first_img(app):
    @app.callback(
        Output('input-path-output', 'children'),
        Output('input-preview', 'figure'),
        Input('submit-val', 'n_clicks'),
        State("input-directory", "value"),
        State('mounted-volume', 'value'),
        State('plate-name', 'value'),
        State('well-selection-list', 'children'),
        prevent_initial_call=True
    )
    def update_preview_image(n_clicks, input, volume, platename, wells):

        first_well = wells[0].replace(', ', '')

        plate_base = platename.split("_", 1)[0]

        if n_clicks >= 1:
            # assumes IX-like file structure
            img_path = Path(volume, input, f'{platename}/TimePoint_1/{plate_base}_{first_well}.TIF')
            img = np.array(Image.open(img_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            return f'```{img_path}```', fig
        n_clicks = 0

def preview_analysis(app):
    @app.callback(
            Output('analysis-preview-message', 'children'),
            Output('analysis-preview', 'figure'),
            Input('preview-button', 'n_clicks'),
            State('plate-name', 'value'),
            State('mounted-volume', 'value'),
            State("work-directory", "value"),
            State('well-selection-list', 'children'),
        prevent_initial_call=True
    )
    def run_analysis(nclicks, platename, volume, work, wells):
        if nclicks:
            # 20210819-p01-NJW_753
            client = docker.from_env()
            print(client)

            first_well = wells[0].replace(', ', '')

            command = f"python wrmXpress/wrapper.py {platename}.yml {platename}"
            command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"
            
            container = client.containers.run('zamanianlab/wrmxpress', command=f"{command}", detach=True, 
                                  volumes={f'{volume}/input/': {'bind': '/input/', 'mode': 'rw'},
                                            f'{volume}/output/': {'bind': '/output/', 'mode': 'rw'},
                                            f'{volume}/work/': {'bind': '/work/', 'mode': 'rw'},
                                            f'{volume}/{platename}.yml': {'bind': f'/{platename}.yml', 'mode': 'rw'}
                                            })
            
            # assumes IX-like file structure
            img_path = Path(volume, work, f'{platename}/{first_well}/img/{platename}_{first_well}_motility.png')
            img = np.array(Image.open(img_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)

            return command_message, fig