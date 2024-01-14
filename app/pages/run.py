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
import plotly.graph_objs as go

# importing utils
from app.utils.styling import layout

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
                                        figure={'layout': layout},
                                        className='h-100 w-100'
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
                                        figure={'layout': layout},
                                        className='h-100 w-100'
                                    ),
                                    html.Br(),
                                    dcc.Graph(
                                        id='analysis-postview-another',
                                        figure={'layout': layout},
                                        className='h-100 w-100'
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

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@callback(
    Output('image-analysis-preview', 'figure'),
    Output('analysis-postview', 'figure'),
    Output('analysis-postview-another', 'figure'),
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def run_analysis(
    nclicks,
    store
):
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    
    if nclicks:
        client = docker.from_env()
        print(client)

        command = f"python wrmXpress/wrapper.py {platename}.yml {platename}"
        command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

        container = client.containers.run('zamanianlab/wrmxpress', command=f"{command}", detach=True,
                                          volumes={f'{volume}/input/': {'bind': '/input/', 'mode': 'rw'},
                                                   f'{volume}/output/': {'bind': '/output/', 'mode': 'rw'},
                                                   f'{volume}/work/': {'bind': '/work/', 'mode': 'rw'},
                                                   f'{volume}/{platename}.yml': {'bind': f'/{platename}.yml', 'mode': 'rw'}
                                                   })
        # assumes IX-like file structure
        img_path = Path(
            volume, 'output', 'thumbs', f'{platename}.png')
        
        # directory path to the thumbs
        file_path = Path(
            volume, 'output', 'thumbs'
        )

        # ensures that the images have been processed 
        while not os.path.exists(img_path):
            time.sleep(1)

        # empty list of filepaths which will be added to later
        files_with_png = []

        # Iterate through all files and subdirectories
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.lower().endswith('.png'):  # Check if the file is a PNG file
                    file_path = os.path.join(root, file)  # Get the full file path
                    files_with_png.append(file_path)  # append the file path to the list

        # empty list for the figures to be added to once they have been processed
        figs = []

        # iterating through each file path and getting the subsequent image
        for i, file_path in enumerate(files_with_png):
            img = np.array(Image.open(file_path))  # Open the image using PIL
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            figs.append(fig) # appending this image to the list

        # Return the figures as a tuple
        return tuple(figs)
