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

module_selection = dbc.AccordionItem(
    [
        # Create separate tabs for video/image analysis
        dcc.Tabs(
            id="module-tabs",
            value="video-analysis-tab",
            persistence=True,
            persistence_type='memory',

            children=[

                # Video analysis tab
                dcc.Tab(
                    label="Video Analysis",
                    value='video-analysis-tab',
                    children=[

                        # Motility module
                        html.H4(
                            "Motility",
                            style={'display': 'inline-block'}
                        ),
                        # Using the info button image
                        html.I(
                            className="fa-solid fa-circle-info",
                            id='motility-symbol',
                            style={
                                'display': 'inline-block',
                                'width': '1.5%',
                                'height': '1.5%',
                                'padding-bottom': 10,
                                'padding-left': 5
                            }
                        ),
                        # Tooltip item for the info button which displays message when cursor over info button
                        dbc.Tooltip(
                            "Uses an optical flow algorithm to measure total motility of the well.",
                            target="motility-symbol"
                        ),
                        html.H6(
                            "Motility Run"
                        ),
                        # Radio buttons for motility run
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
                            value="True",
                            persistence=True,
                            persistence_type='memory'
                        ),
                        html.Br(),

                        # Conversion module
                        html.H4(
                            "Conversion",
                            style={
                                'padding-top': 30,
                                'display': 'inline-block'
                            }
                        ),
                        # Using info button image
                        html.I(
                            className="fa-solid fa-circle-info",
                            id='conversion-symbol',
                            style={
                                'display': 'inline-block',
                                'width': '1.5%',
                                'height': '1.5%',
                                'padding-bottom': 10,
                                'padding-left': 5
                            }
                        ),
                        # Utalizing tooltip item for info button image
                        dbc.Tooltip(
                            "Convert an IX-like video file-structure (directories of time points) to a structure that contains directories of wells. This new structure will be saved to Output",
                            target="conversion-symbol"
                        ),
                        html.H6(
                            "Conversion Run"
                        ),
                        # Radio buttons for conversion run
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
                            value="False",
                            persistence=True,
                            persistence_type='memory'
                        ),
                        html.Br(),
                        html.H6(
                            "Conversion Scale Video",
                            style={'display': 'inline-block'}
                        ),

                        html.I(
                            className="fa-solid fa-circle-info",
                            id='rescale-symbol',
                            style={
                                'display': 'inline-block',
                                'width': '1.5%',
                                'height': '1.5%',
                                'padding-bottom': 10,
                                'padding-left': 5
                            }
                        ),
                        # Using tooltip item for info button image
                        dbc.Tooltip(
                            "Rescale the video to be smaller or larger than the original. Useful for reducing the file size of a video to be included in a presentation. Use a float as the multiplier (smaller than 1 will make a smaller video).",
                            target="rescale-symbol"
                        ),
                        # Radio button items for conversion scale video
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
                            persistence=True,
                            persistence_type='memory'
                        ),
                        html.H6(
                            "Conversion Rescale Multiplier"
                        ),
                        # Input of text for rescale multiplier
                        dbc.Input(
                            id="conversion-rescale-multiplier",
                            placeholder="Please insert the rescale multiplier:",
                            type="text"
                        ),

                        # Segementation module
                        html.H4(
                            "Segmentation",
                            style={'padding-top': 30}
                        ),
                        html.H6(
                            "Segment Run"
                        ),
                        # Radio button items for segment run
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
                            persistence=True,
                            persistence_type='memory'
                        ),
                        html.H6(
                            "Wavelength"
                        ),
                        # Input of text for wavelength
                        dbc.Input(
                            id="segmentation-wavelength",
                            placeholder="Please insert the segmentation wavelength (please seperate multiple values by a comma):",
                            type="text",
                            persistence=True,
                            persistence_type='memory'
                        )
                    ]),

                # Image analysis tab
                dcc.Tab(
                    label="Image Analysis (CellProfiler)",
                    value='still-analysis-tab',
                    children=[

                        # Cell Profiler module
                        html.H4(
                            "Cell Profiler",
                            style={'padding-top': 30}
                        ),
                        html.H6(
                            "Cell Profiler Run"
                        ),
                        # Radio button items for cell profiler run
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
                            persistence=True,
                            persistence_type='memory'
                        ),
                        html.H6(
                            "Cell Profiler Pipeline"
                        ),
                        # Radio buttons for cell profiler pipeline
                        dbc.RadioItems(
                            id="cell-profiler-pipeline",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {
                                    "label": "Worm Size, Intensity, Cell Pose",
                                    "value": "wormsize_intensity_cellpose"
                                },
                                {
                                    "label": "Mf Celltox",
                                    "value": "mf_celltox"
                                },
                                {
                                    "label": "Wormsize",
                                    "value": "wormsize"
                                },
                                {
                                    "label": "Wormsize Trans",
                                    "value": "wormsize_trans"
                                }
                            ],
                            value="wormsize_intensity_cellpose",
                            persistence=True,
                            persistence_type='memory'
                        )
                    ]
                )
            ]
        ),

        html.Hr(),

        # Diagnostic Module
        html.H4(
            "Diagnostics",
            style={'display': 'inline-block'}
        ),
        # Using info button image
        html.I(
            className="fa-solid fa-circle-info",
            id='dx-symbol',
            style={
                'display': 'inline-block',
                      'width': '1.5%',
                      'height': '1.5%',
                      'padding-bottom': 10,
                      'padding-left': 5
            }
        ),

        dbc.Tooltip(
            # Tooltip element for information symbol, displays message when cursor over the symbol
            "Generate and export diagnostic images (recommended).",
            target="dx-symbol"
        ),
        html.H6(
            "dx"
        ),
        # Radio buttons for dx
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
            persistence=True,
            persistence_type='memory'
        )
    ],
    id="module-selection",
    title="Module Selection"
)
