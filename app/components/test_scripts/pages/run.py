########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash

dash.register_page(__name__)

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
                                    html.Br(),
                                    html.H6(
                                        "Imaging Mode:", className="card-subtitle"),
                                    html.Br(),
                                    html.H6(
                                        'File Structure:', className='card-subtitle'),
                                    html.Br(),
                                    html.H6('Plate Format:',
                                            className='card-subtitle'),
                                    html.Br(),
                                    html.H6('Image Masking:',
                                            className='card-subtitle'),
                                    html.Br(),
                                    html.H6('Module Selection:',
                                            className='card-subtitle'),
                                    html.Br(),
                                    html.H6(
                                        'Volume:', className='card-subtitle'),
                                    html.Br(),
                                    html.H6('Plate Name:',
                                            className='card-subtitle'),
                                    html.Br(),
                                    html.H6(
                                        'Wells:', className='card-subtitle'),
                                    html.Br(),
                                    dbc.Button('Begin Analysis',
                                               id='submit-analysis', className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
                                    dcc.Graph(
                                        id='image-analysis-preview',
                                    ),

                                ]
                                )
                            )
                        ),

                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4(
                                        "Run Diagnosis", className="text-center"),
                                    dcc.Graph(
                                        id='analysis-postview',
                                    ),
                                    html.Br(),
                                    dcc.Graph(
                                        id='analysis-postview-another',
                                    ),
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
