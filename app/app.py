import base64
import os
import pathlib
import itertools
from collections import OrderedDict

import cv2
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import yaml
from dash import callback_context, dash_table, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from PIL import Image

# Importing Components
from components.selection_table import selection_table
from components.instrument_settings import instrument_settings
from components.header import header

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SPACELAB], 
                suppress_callback_exceptions=True)


# Initialize images
info_symbol = "data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwWiIgZGF0YS1uYW1lPSJQYXRoIDM2NzIiLz48cGF0aCBmaWxsPSIjNTI1ODYzIiBkPSJNNS4yMTEgMTguNzg3YTkuNiA5LjYgMCAxIDEgNi43ODggMi44MTQgOS42IDkuNiAwIDAgMS02Ljc4OC0yLjgxNFptMS4yNzQtMTIuM0E3LjgwNiA3LjgwNiAwIDEgMCAxMiA0LjIwNmE3LjgwOCA3LjgwOCAwIDAgMC01LjUxNSAyLjI3OFptNC4xNjMgOS44Nzl2LTQuOGExLjM1MiAxLjM1MiAwIDAgMSAyLjcgMHY0LjhhMS4zNTIgMS4zNTIgMCAwIDEtMi43IDBabS4wMTctOC43QTEuMzM1IDEuMzM1IDAgMSAxIDEyIDkuMDMzYTEuMzUgMS4zNSAwIDAgMS0xLjMzNS0xLjM2OVoiIGRhdGEtbmFtZT0iUGF0aCAyNjgzIi8+PC9zdmc+"

########################################################################
####                                                                ####
####                             NAVBAR                             ####
####                                                                ####
########################################################################


########################################################################
####                                                                ####
####                    MAIN ACCORDION STRUCTURE                    ####
####                                                                ####
########################################################################


worm_information = dbc.AccordionItem(
    [
        html.H6("Species:"),
        dbc.RadioItems(
            id="species",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Brugia malayi", "value": "Bma"},
                {"label": "Caenorhabditis elegans", "value": "Cel"},
                {"label": "Schistosoma mansoni", "value": "Sma"}
            ],
            value="Bma",
        ),
        html.H6("Stages:"),
        dbc.RadioItems(
            id="stages",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Mf", "value": "Mf"},
                {"label": "Adult", "value": "Adult"},
                {"label": "Mixed", "value": "Mixed"},
            ],
            value="Mf",
        ),
    ],
    id="worm-information",
    title="Worm Information"
)


module_selection = dbc.AccordionItem(
        [
            # Create separate tabs for video/image analysis
            dcc.Tabs(id="module-tabs", value="tab-modules", children=[

                # Video analysis tab
                dcc.Tab(label="Video Analysis", value='video-analysis-tab', children=[

                    # Motility module
                    html.H4("Motility", style={'display': 'inline-block'}),
                    html.Img(src=info_symbol,
                             id='motility-symbol',
                             style={'display': 'inline-block', 'width': '1.5%', 'height': '1.5%', 'padding-bottom': 10}),
                    dbc.Tooltip(
                        "Uses an optical flow algorithm to measure total motility of the well.",
                        target="motility-symbol"),
                    html.H6("Motility Run"),
                    dbc.RadioItems(
                        id="motility-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="True"
                    ),
                    html.Br(),

                    # Conversion module
                    html.H4("Conversion",
                            style={'padding-top': 30, 'display': 'inline-block'}),
                    html.Img(src=info_symbol,
                             id='conversion-symbol',
                             style={'display': 'inline-block', 'width': '1.5%', 'height': '1.5%', 'padding-bottom': 10}),
                    dbc.Tooltip(
                        "Convert an IX-like video file-structure (directories of time points) to a structure that contains directories of wells. This new structure will be saved to Output",
                        target="conversion-symbol"),
                    html.H6("Conversion Run"),
                    dbc.RadioItems(
                        id="conversion-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="False"
                    ),
                    html.Br(),
                    html.H6("Conversion Scale Video",
                            style={'display': 'inline-block'}),
                    html.Img(src=info_symbol,
                             id='rescale-symbol',
                             style={'display': 'inline-block', 'width': '1.5%', 'height': '1.5%', 'padding-bottom': 10}),
                    dbc.Tooltip(
                        "Rescale the video to be smaller or larger than the original. Useful for reducing the file size of a video to be included in a presentation. Use a float as the multiplier (smaller than 1 will make a smaller video).",
                        target="rescale-symbol"),
                    dbc.RadioItems(
                        id="conversion-scale-video",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="False",
                    ),
                    html.H6("Conversion Rescale Multiplier"),
                    dbc.Input(id="conversion-rescale-multiplier",
                              placeholder="Please insert the rescale multiplier:",
                              type="text"),

                    # Segementation module
                    html.H4("Segmentation",
                            style={'padding-top': 30}),
                    html.H6("Segment Run"),
                    dbc.RadioItems(
                        id="segment-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="True",
                    ),
                    html.H6("Wavelength"),
                    dbc.Input(id="segmentation-wavelength",
                              placeholder="Please insert the segmentation wavelength (please seperate multiple values by a comma):", type="text")
                ]),

                # Image analysis tab
                dcc.Tab(label="Image Analysis (CellProfiler)", value='still-analysis-tab', children=[

                    # Cell Profiler module
                    html.H4("Cell Profiler",
                            style={'padding-top': 30}),
                    html.H6("Cell Profiler Run"),
                    dbc.RadioItems(
                        id="cell-profiler-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="False",
                    ),
                    html.H6("Cell Profiler Pipeline"),
                    dbc.RadioItems(
                        id="cell-profiler-pipeline",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Worm Size, Intensity, Cell Pose",
                             "value": "wormsize_intensity_cellpose"},
                            {"label": "Mf Celltox", "value": "mf_celltox"},
                            {"label": "Wormsize", "value": "wormsize"},
                            {"label": "Wormsize Trans", "value": "wormsize_trans"}
                        ],
                        value="wormsize_intensity_cellpose",
                    )
                ])]),

            html.Hr(),

            # Diagnostic Module
            html.H4("Diagnostics",
                    style={'display': 'inline-block'}),
            html.Img(src=info_symbol,
                     id='dx-symbol',
                     style={'display': 'inline-block', 'width': '1.5%', 'height': '1.5%', 'padding-bottom': 10}),
            dbc.Tooltip(
                "Generate and export diagnostic images (recommended).",
                target="dx-symbol"),
            html.H6("dx"),
            dbc.RadioItems(
                id="diagnostics-dx",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "True", "value": "True"},
                    {"label": "False", "value": "False"}
                ],
                value="True",
            )
        ],
        id="module-selection",
        title="Module Selection"
    )


run_time_settings = dbc.AccordionItem(
    [
        html.H4("Directories"),
        html.H6("Work"),
        dbc.Input(
            id="work-directory", placeholder="Please insert the work directory:", type="text"),
        html.H6("Input"),
        dbc.Input(
            id="input-directory", placeholder="Please insert the input directory:", type="text"),
        html.H6("Output"),
        dbc.Input(
            id="output-directory", placeholder="Please insert the output directory:", type="text"),
        html.Br(),

        html.H4("Wells"),
        html.P("Edit the following table such that well IDs are only present for wells to be analyzed.\
            Alternatively, edit the following field to include a list of comma-separated well IDs. \
                This list will override the contents of the table."),
        selection_table,
        html.Br(),
        html.P("List of wells to be analyzed:"),
        dbc.Card(
            dbc.CardBody(
                html.P(
                    id='well-selection-list'
                )
            )
        )
    ],
    id="run-time-settings",
    title="Run-Time Settings"
)


########################################################################
####                                                                ####
####                             MODALS                             ####
####                                                                ####
########################################################################

save_page_content = dbc.ModalBody(
    [
        # Content for the Save Page Modal
        dcc.Markdown("Write a YAML for running wrmXpress remotely. Include a full path and file name ending in `.yaml`."),
        dbc.Input(id="file-path-for-saved-yaml-file",
                  placeholder="Enter the full save path...", type="text"),
    ]
)


info_page_content = dbc.ModalBody(
    [
        html.P("wrmXpress is a unified framework for the analysis of diverse phenotypic imaging data in high-throughput and high-content experiments involving free-living and parasitic nematodes and flatworms. wrmXpress is a versatile solution capable of handling large datasets and generating relevant phenotypic measurements across various worm species and experimental assays. This software, designed to analyze a spectrum of phenotypes such as motility, development/size, fecundity, and feeding, not only addresses current research needs but also establishes itself as a platform for future extensibility, enabling the development of custom phenotypic modules."),

        html.H3("Usage"),
        html.P("There are two options for running wrmXpress:"),


        dbc.Row(
            [
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(
                            [
                                html.H5("Remotely", className="card-title"),
                                dcc.Markdown(
                                    "wrmXpress was originally designed to be invoked remotely, using a high-performance or high-throughput computer. There are many ways to go about this, but we recommend encapsulating the entire process in a Docker container. The container should include the Python libraries required by wrmXpress (see the [Zamanian Lab's Dockerfile/conda environment](https://github.com/zamanianlab/Docker/tree/main/chtc-wrmxpress) for an example), the cloned [wrmXpress repository](https://github.com/zamanianlab/wrmXpress), the input data in a directory called `input/`, and a YAML file that configures the analysis. A user can use this graphical user interface (GUI) to produce the YAML by selecting the options and modules and clicking Save YAML.",
                                    className="card-text")
                            ]
                        )
                    ],
                        color='light')
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(
                             [
                                 html.H5("Locally", className="card-title"),
                                 dcc.Markdown("Many analyses, such as those that include a few dozen separate videos or images, can be performed on a desktop computer without the need for high-performance or high-throughput computing. For these, a user can use this GUI to select the options and modules and run the analysis by clicking the Preview and Run button.",
                                              className="card-text")
                             ]
                             )
                    ],
                        color='light')
                ])
            ]),
        html.Br(),
        html.H3("The Developers"),
        dcc.Markdown(
            "wrmXpress is entirely open-source. The code for the back-end is maintained by the [Zamanian Lab](https://www.zamanianlab.org/) at the University of Wisconsin-Madison and can be found [here](https://github.com/zamanianlab/wrmXpress). The code for the front-end is maintained by the [Wheeler Lab](wheelerlab.bio) at the University of Wisconsin-Eau Claire and can be found [here](https://github.com/wheelerlab-uwec/wrmXpress-gui)."),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [html.Img(
                        src='https://assets.super.so/6d48c8d3-6e72-45c3-a5b9-04514883421e/images/9da71b53-e8f2-4234-9e55-e50d302f5c46/Lab_logo.svg',
                        style={'width':'30%'}
                    ),
                    html.Img(
                        src='https://lib02.uwec.edu/Omeka/files/original/37b67b60cca3c3ad308515aab27a66afe6c75b2f.gif',
                        style={'width':'30%'}
                    )],
                    style={'textAlign':'center'}
                ),
                dbc.Col(
                    [html.Img(
                        src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/University_of_Wisconsin_seal.svg/512px-University_of_Wisconsin_seal.svg.png',
                        style={'width':'30%'}
                    )],
                    style={'textAlign':'center'}
                )
            ])
    ]
)


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

# Create the Save Page Modal
info_page = dbc.Modal(
    [
        dbc.ModalHeader(
            "Information & Usage"
        ),
        info_page_content,
        dbc.ModalFooter([
            # Buttons for the Info Page Modal
            dbc.Button("Close", id="close-info-modal", className="ml-auto"),
        ]),
        html.Div(id="info-page-status")  # Placeholder for saving status
    ],
    id="info-page-modal",
    size="xl"
)

# Create the Save Page Modal
save_page = dbc.Modal(
    [
        dbc.ModalHeader("Save Page"),
        save_page_content,
        dbc.ModalFooter([
            # Buttons for the Save Page Modal
            dbc.Button("Save", id="save-page-button", className="ml-auto"),
            dbc.Button("Close", id="close-save-modal", className="ml-auto"),
        ]),
        html.Div(id="save-page-status")  # Placeholder for saving status
    ],
    id="save-page-modal",
    size="l"
)


########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

app.layout = html.Div([
    # Navbar
    header,

    # Accordion
    dbc.Container([
        dbc.Accordion(
            [
                instrument_settings,
                worm_information,
                module_selection,
                run_time_settings,
            ],
            start_collapsed=False,
            always_open=True,
        ),
    ],
    style={"paddingTop":"150px"}),

    # Modals (popup screens)
    save_page,
    info_page,
    preview_page,
])

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################

# Collapsing navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Appearing multi-well options
@app.callback(
    [Output('multi-well-options-row', 'style'),
     Output('additional-options-row', 'style')],
    [Input('imaging-mode', 'value'),
     Input('file-structure', 'value')]
)
def update_options_visibility(imaging_mode, file_structure):
    multi_well_options_style = {'display': 'none'}
    additional_options_style = {'display': 'none'}

    if imaging_mode == 'multi-well':
        multi_well_options_style = {'display': 'flex'}

        if file_structure == 'avi':
            additional_options_style = {'display': 'flex'}

    return multi_well_options_style, additional_options_style


# Populate list of wells to be analyzed
@app.callback(
    Output('well-selection-list', 'children'),
    Input('well-selection-table', 'data')
)
def update_wells(table_contents):
    values_list = [list(d.values()) for d in table_contents]
    flattened_list = list(itertools.chain.from_iterable(values_list))
    filtered_list = []
    for item in flattened_list:
        if item is None:
            continue
        elif len(item) == 1:
            continue
        else:
            filtered_list.append(item + ", ")
    # filtered_list = [item for item in flattened_list if item is None or len(item) > 1]
    sorted_list = sorted(filtered_list)

    return sorted_list

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


# Write YAML from preview page
@app.callback(
    Output("preview-page-status", "children"),
    [Input("preview-preview-button", "n_clicks")],
    [
        State("imaging-mode", "value"),
        State("file-structure", "value"),
        State("multi-well-rows", "value"),
        State("multi-well-cols", "value"),
        State("multi-well-detection", "value"),
        State("species", "value"),
        State("stages", 'value'),
        State("motility-run", "value"),
        State("conversion-run", "value"),
        State("conversion-scale-video", "value"),
        State("conversion-rescale-multiplier", "value"),
        State("segment-run", "value"),
        State("segmentation-wavelength", 'value'),
        State("cell-profiler-run", "value"),
        State("cell-profiler-pipeline", "value"),
        State("diagnostics-dx", "value"),
        State("well-selection-list", "children"),
        State("work-directory", "value"),
        State("input-directory", "value"),
        State("output-directory", "value"),
        State("file-path-for-preview-yaml-file", "value"),
        State("file-path-to-wrapper-py", "value"),
    ]
)
def save_page_to_yaml(
    n_clicks,
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
    wellselection,
    workdirectory,
    inputdirectory,
    outputdirectory,
    filepathforyamlfile,
    wrapper_py_file_path,
):
    if n_clicks:
        well_list = [s.replace(", ", '') for s in wellselection]

        preview_input_yaml_file = {
            "imaging_mode": [imagingmode],
            "file_structure": [filestructure],
            "multi-well-rows": multiwellrows,
            "multi-well-cols": multiwellcols,
            "multi-well-detection": [multiwelldetection],
            "species": [species],
            "stages": [stages],
            "modules": {
                "motility": {"run": bool(motilityrun)},
                "convert": {
                    "run": bool(conversionrun),
                    "save_video": bool(conversionscalevideo),
                    "rescale_multiplier": conversionrescalemultiplier
                },
                "segment": {
                    "run": bool(segmentrun),
                    "wavelength": [wavelength]
                },
                "cellprofiler": {
                    "run": bool(cellprofilerrun),
                    "pipeline": [cellprofilerpipeline]
                },
                "dx": {
                    "run": bool(diagnosticdx)
                }
            },
            "wells": well_list,
            "directories": {
                "work": [workdirectory],
                "input": [inputdirectory],
                "output": [outputdirectory]
            }
        }
        # Create the full filepath using os.path.join
        output_file = os.path.join(filepathforyamlfile)

        # Dump preview data to YAML file
        with open(output_file, 'w') as yaml_file:
            yaml.dump(preview_input_yaml_file, yaml_file,
                      default_flow_style=False)
        return f"Data Saved to {filepathforyamlfile}"
    return ""

# Write YAML from save page
@app.callback(
    Output("save-page-status", "children"),
    [Input("save-page-button", "n_clicks")],
    [
        State("imaging-mode", "value"),
        State("file-structure", "value"),
        State("multi-well-rows", "value"),
        State("multi-well-cols", "value"),
        State("multi-well-detection", "value"),
        State("species", "value"),
        State("stages", 'value'),
        State("motility-run", "value"),
        State("conversion-run", "value"),
        State("conversion-scale-video", "value"),
        State("conversion-rescale-multiplier", "value"),
        State("segment-run", "value"),
        State("segmentation-wavelength", 'value'),
        State("cell-profiler-run", "value"),
        State("cell-profiler-pipeline", "value"),
        State("diagnostics-dx", "value"),
        State("well-selection-list", "children"),
        State("work-directory", "value"),
        State("input-directory", "value"),
        State("output-directory", "value"),
        State("file-path-for-saved-yaml-file", "value")
    ]
)
def save_page_to_yaml(
    n_clicks,
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
    wellselection,
    workdirectory,
    inputdirectory,
    outputdirectory,
    filepathforyamlfile
):
    if n_clicks:
        well_list = [s.replace(", ", '') for s in wellselection]
        
        user_input_yaml_file = {
            "imaging_mode": [imagingmode],
            "file_structure": [filestructure],
            "multi-well-rows": multiwellrows,
            "multi-well-cols": multiwellcols,
            "multi-well-detection": [multiwelldetection],
            "species": [species],
            "stages": [stages],
            "modules": {
                "motility": {"run": bool(motilityrun)},
                "convert": {
                    "run": bool(conversionrun),
                    "save_video": bool(conversionscalevideo),
                    "rescale_multiplier": conversionrescalemultiplier
                },
                "segment": {
                    "run": bool(segmentrun),
                    "wavelength": [wavelength]
                },
                "cellprofiler": {
                    "run": bool(cellprofilerrun),
                    "pipeline": [cellprofilerpipeline]
                },
                "dx": {
                    "run": bool(diagnosticdx)
                }
            },
            "wells": well_list,
            "directories": {
                "work": [workdirectory],
                "input": [inputdirectory],
                "output": [outputdirectory]
            }
        }
        # Create the full filepath using os.path.join
        output_file = os.path.join(filepathforyamlfile)

        # Dump preview data to YAML file
        with open(output_file, 'w') as yaml_file:
            yaml.dump(user_input_yaml_file, yaml_file,
                      default_flow_style=False)
        return f"Data Saved to {filepathforyamlfile}"
    return ""

# Open Info, Preview, and Save modals
@app.callback(
    [Output("save-page-modal", "is_open"),
     Output("info-page-modal", "is_open"),
     Output("preview-page-modal", "is_open")],
    [Input("open-save-modal", "n_clicks"), Input("close-save-modal", "n_clicks"),
     Input("open-info-modal", "n_clicks"), Input("close-info-modal", "n_clicks"),
     Input("open-preview-modal", "n_clicks"), Input("close-preview-modal", "n_clicks")],
    [State("save-page-modal", "is_open"),
     State("info-page-modal", "is_open"),
     State("preview-page-modal", "is_open")],
)
def toggle_modals(open_save_clicks, close_save_clicks, open_info_clicks, close_info_clicks,
                  open_preview_clicks, close_preview_clicks, is_save_open, is_info_open, is_preview_open):
    ctx = dash.callback_context

    if ctx.triggered_id in ["open-save-modal", "close-save-modal"]:
        return not is_save_open, False, False
    elif ctx.triggered_id in ["open-info-modal", "close-info-modal"]:
        return False, not is_info_open, False
    elif ctx.triggered_id in ["open-preview-modal", "close-preview-modal"]:
        # Toggle the preview modal based on the button click
        return False, False, not is_preview_open
    else:
        return is_save_open, is_info_open, is_preview_open


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9000)