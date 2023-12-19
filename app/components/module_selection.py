########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html

info_symbol = "data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwWiIgZGF0YS1uYW1lPSJQYXRoIDM2NzIiLz48cGF0aCBmaWxsPSIjNTI1ODYzIiBkPSJNNS4yMTEgMTguNzg3YTkuNiA5LjYgMCAxIDEgNi43ODggMi44MTQgOS42IDkuNiAwIDAgMS02Ljc4OC0yLjgxNFptMS4yNzQtMTIuM0E3LjgwNiA3LjgwNiAwIDEgMCAxMiA0LjIwNmE3LjgwOCA3LjgwOCAwIDAgMC01LjUxNSAyLjI3OFptNC4xNjMgOS44Nzl2LTQuOGExLjM1MiAxLjM1MiAwIDAgMSAyLjcgMHY0LjhhMS4zNTIgMS4zNTIgMCAwIDEtMi43IDBabS4wMTctOC43QTEuMzM1IDEuMzM1IDAgMSAxIDEyIDkuMDMzYTEuMzUgMS4zNSAwIDAgMS0xLjMzNS0xLjM2OVoiIGRhdGEtbmFtZT0iUGF0aCAyNjgzIi8+PC9zdmc+"

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
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