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
####                           Callbacks                            ####
####                                                                ####
########################################################################


@callback(
    Output('input-path-output', 'children'),
    Output('input-preview', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    State('plate-name', 'value'),
    State('well-selection-list', 'children'),
    prevent_initial_call=True
)
def update_preview_image(n_clicks, store, platename, wells):

    first_well = wells[0].replace(', ', '')

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
    Input('open-preview-modal', 'n_clicks'),
    State('motility-run', 'value'),
    State('segment-run', 'value')
)
def get_options(nclicks, motility, segment):

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
    State('imaging-mode', 'value'),
    State('file-structure', 'value'),
    State('multi-well-rows', 'value'),
    State('multi-well-cols', 'value'),
    State('multi-well-detection', 'value'),
    State('species', 'value'),
    State('stages', 'value'),
    State('motility-run', 'value'),
    State('conversion-run', 'value'),
    State('conversion-scale-video', 'value'),
    State('conversion-rescale-multiplier', 'value'),
    State('segment-run', 'value'),
    State('segmentation-wavelength', 'value'),
    State('cell-profiler-run', 'value'),
    State('cell-profiler-pipeline', 'value'),
    State('diagnostics-dx', 'value'),
    State('plate-name', 'value'),
    State('store', 'value'),
    State('well-selection-list', 'children'),
    State('preview-dropdown', 'value'),
    prevent_initial_call=True
)
def run_analysis(
    nclicks,
    imagingmode,
    filestructure,
    multiwellrows,
    multiwellcols,
    multiwelldetection,
    species,
    stages,
    motilityrun,
    conversionrun,
    conversionscalevideo,
    conversionrescalemultiplier,
    segmentrun,
    wavelength,
    cellprofilerrun,
    cellprofilerpipeline,
    diagnosticdx,
    platename,
    store,
    wells,
    selection
):
    volume = store['mount']
    if nclicks:

        if wells == 'All':
            first_well = 'A01'
        else:
            first_well = wells[0]

        config = prep_yaml(
            imagingmode,
            filestructure,
            multiwellrows,
            multiwellcols,
            multiwelldetection,
            species,
            stages,
            motilityrun,
            conversionrun,
            conversionscalevideo,
            conversionrescalemultiplier,
            segmentrun,
            wavelength,
            cellprofilerrun,
            cellprofilerpipeline,
            diagnosticdx,
            wells
        )

        output_file = Path(volume, platename + '.yml')

        # Dump preview data to YAML file
        with open(output_file, 'w') as yaml_file:
            yaml.dump(config, yaml_file,
                      default_flow_style=False)

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
            volume, 'work', f'{platename}/{first_well}/img/{platename}_{first_well}_{selection}.png')

        while not os.path.exists(img_path):
            time.sleep(1)

        img = np.array(Image.open(img_path))
        fig = px.imshow(img, color_continuous_scale="gray")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return command_message, fig
