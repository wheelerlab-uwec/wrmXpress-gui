########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import docker
import yaml
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
from app.utils.callback_functions import prep_yaml
import os
import plotly.graph_objs as go

dash.register_page(__name__)

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
layout = go.Layout(
    xaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        zeroline=False,
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        zeroline=False,
        showticklabels=False
    )
)

layout = dbc.ModalBody(
    [
        # Preview page contents
        html.Div([
            html.Div([
                dbc.Row([
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("Input",
                                            className="text-center mb-5"),
                                    html.Br(),
                                    html.H6(
                                        "Path:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(id='input-path-output'),
                                    html.Div(
                                        dcc.Graph(
                                            id='input-preview',
                                            figure={'layout': layout},
                                            className='h-100 w-100'
                                        )),
                                    dbc.Button('Load first input image',
                                               id='submit-val',
                                               className="d-grid gap-2 col-6 mx-auto",
                                               color="primary",
                                               n_clicks=0),
                                ]
                                )
                            ),
                            width={'size': 6}
                        ),

                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4(
                                        "Analysis", className="text-center"),
                                    dcc.Dropdown(
                                        id='preview-dropdown',
                                        placeholder='Select image to preview...'),
                                    html.Br(),
                                    html.H6(
                                        "Command:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(
                                        id='analysis-preview-message'),
                                    dcc.Graph(
                                        id='analysis-preview',
                                        figure={'layout': layout},
                                        className='h-100 w-100'
                                    ),
                                    dbc.Button(
                                        "Preview analysis", id="preview-button", className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
                                ]
                                )
                            ),
                            width={'size': 6})
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
    Output('input-path-output', 'children'),
    Output('input-preview', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def update_preview_image(n_clicks, store):

    wells = store['wells']
    first_well = wells[0].replace(', ', '')

    platename = store['platename']
    plate_base = platename.split("_", 1)[0]

    volume = store['mount']
    if n_clicks >= 1:
        # assumes IX-like file structure
        img_path = Path(
            volume, 'input', f'{platename}/TimePoint_1/{plate_base}_{first_well}.TIF')
        img = np.array(Image.open(img_path))
        fig = px.imshow(img, color_continuous_scale="gray")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return f'```{img_path}```', fig
    n_clicks = 0


@callback(
    Output('preview-dropdown', 'options'),
    # update the option dropdown when the previous load is clicked
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def get_options(nclicks, store):

    motility = store['motility']
    segment = store['segment']
    selection_dict = {'motility': 'motility', 'segment': 'binary'}
    option_dict = {}

    if nclicks is not None:
        for selection in selection_dict.keys():
            if eval(selection) == 'True':
                option_dict[selection] = selection_dict[selection]

    dict_option = {v: k for k, v in option_dict.items()}
    return dict_option


@callback(
    Output('analysis-preview-message', 'children'),
    Output('analysis-preview', 'figure'),
    Input('preview-button', 'n_clicks'),
    State('store', 'data'),
    State('preview-dropdown', 'value'),
    prevent_initial_call=True
)
def run_analysis(
    nclicks,
    store,
    selection
):
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]

    if nclicks:
        if wells == 'All':
            first_well = 'A01'
        else:
            first_well = wells[0]

        full_yaml = Path(volume, platename + '.yml')
        # reading in yaml file
        with open(full_yaml, 'r') as file:
            data = yaml.safe_load(file)

        # creating temp yaml file name
        temp_platename = f'{platename}_temp'
        # creating temp yaml file path
        temp_plate_path = Path(volume, temp_platename + '.yml')

        # assigning first well to the well value
        data['wells'] = [first_well]

        # Dump preview data to temp YAML file
        with open(temp_plate_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file,
                    default_flow_style=False)
            
        client = docker.from_env()
        print(client)

        command = f"python wrmXpress/wrapper.py {temp_platename}.yml {platename}"
        command_message = f"```python wrmXpress/wrapper.py {temp_platename}.yml {platename}```"

        container = client.containers.run('zamanianlab/wrmxpress', command=f"{command}", detach=True,
                                          volumes={f'{volume}/input/': {'bind': '/input/', 'mode': 'rw'},
                                                   f'{volume}/output/': {'bind': '/output/', 'mode': 'rw'},
                                                   f'{volume}/work/': {'bind': '/work/', 'mode': 'rw'},
                                                   f'{volume}/{temp_platename}.yml': {'bind': f'/{temp_platename}.yml', 'mode': 'rw'}
                                                   })

        # assumes IX-like file structure
        img_path = Path(
            volume, 'work', f'{platename}/{first_well}/img/{platename}_{first_well}_{selection}.png')

        while not os.path.exists(img_path):
            time.sleep(1)

        img = np.array(Image.open(img_path))
        fig = px.imshow(img, color_continuous_scale="gray")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        # remove temporary yaml file
        os.remove(temp_plate_path)

        print('finished')
        return command_message, fig
