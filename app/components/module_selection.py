# In[1]: Imports

import dash_bootstrap_components as dbc
from dash import html

# In[2]: Module Selection

module_selection = dbc.AccordionItem(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    html.H5("wrmXpress pipeline:"),
                                    dbc.Checklist(
                                        id="pipeline-selection",
                                        options=[
                                            {
                                                "label": "Optical Flow (motility)",
                                                "value": "motility",
                                            },
                                            {
                                                "label": "Segmentation",
                                                "value": "segmentation",
                                            },
                                            {
                                                "label": "CellProfiler",
                                                "value": "cellprofiler",
                                            },
                                            {"label": "Tracking", "value": "tracking"},
                                            # {"label": "Fecundity", "value": "fecundity"},
                                            # {
                                            #     "label": [
                                            #         html.I("C. elegans"),
                                            #         " size and intensity (Cellpose)",
                                            #     ],
                                            #     "value": "wormsize_intensity_cellpose",
                                            # },
                                            # {
                                            #     "label": "Microfilariae viability",
                                            #     "value": "mf_celltox",
                                            # },
                                            # {
                                            #     "label": [html.I("C. elegans"), " feeding"],
                                            #     "value": "feeding",
                                            # },
                                            # {
                                            #     "label": [html.I("C. elegans"), " size"],
                                            #     "value": "wormsize",
                                            # },
                                        ],
                                        value=[],
                                        switch=True,
                                        persistence=True,
                                        persistence_type="memory",
                                    ),
                                ]
                            ),
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.Br(),
                                        html.H5(
                                            "Parameters:",
                                            id="pipeline-params-header",
                                            style={"display": "none"},
                                        ),
                                        dbc.Row(  # Parameters for motility pipeline
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H5(
                                                            "Motility Parameters:",
                                                        ),
                                                        html.Div(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Wavelength:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Select(
                                                                                    id="wavelengths",
                                                                                    options=[
                                                                                        # {
                                                                                        #     "label": "All",
                                                                                        #     "value": "All",
                                                                                        # },
                                                                                        {
                                                                                            "label": "w1",
                                                                                            "value": "w1",
                                                                                        },
                                                                                        {
                                                                                            "label": "w2",
                                                                                            "value": "w2",
                                                                                        },
                                                                                        {
                                                                                            "label": "w3",
                                                                                            "value": "w3",
                                                                                        },
                                                                                        {
                                                                                            "label": "w4",
                                                                                            "value": "w4",
                                                                                        },
                                                                                    ],
                                                                                    value="w1",
                                                                                    persistence=True,
                                                                                    persistence_type="memory",
                                                                                ),
                                                                                # dbc.Input(
                                                                                #     id="wavelengths",
                                                                                #     placeholder="Wavelength",
                                                                                #     type="text",
                                                                                #     persistence=True,
                                                                                #     persistence_type="memory",
                                                                                #     style={"display": "flex"},
                                                                                # ),
                                                                            ],
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "pyrScale:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="pyrscale",
                                                                                placeholder="0.5",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Levels:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="levels",
                                                                                placeholder="5",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Window size:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="winsize",
                                                                                placeholder="20",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Iterations:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="iterations",
                                                                                placeholder="7",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Poly N:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="poly_n",
                                                                                placeholder="5",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Poly Sigma:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="poly_sigma",
                                                                                placeholder="1.1",
                                                                                step=0.1,
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Flags:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="flags",
                                                                                placeholder="0",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                        html.Br(),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Img(
                                                            src="assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01_motility.png",
                                                            style={"width": "40%"},
                                                            id="motility-input-preview",
                                                        ),
                                                        html.P(
                                                            "The motility pipeline exports a 'flow cloud' as a diagnostic and saves a single value as output.",
                                                            id="motility-input-text",
                                                        ),
                                                    ],
                                                    style={"textAlign": "center"},
                                                ),
                                                html.Hr(id = "motility-hr",
                                                        style = {"display": "none"}),
                                            ],
                                            id="motility_params",
                                            style={"display": "none"},
                                        ),
                                        dbc.Row(  # Tracking parameters for Segmentation pipeline
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H5(
                                                            "Segmentation Parameters:",
                                                        ),
                                                        html.Div(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        # cellpose model selection
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Cellpose Model:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Select(
                                                                                id="cellpose-model-segmentation",
                                                                                options=[
                                                                                    {
                                                                                        "label": "celegans_20220830",
                                                                                        "value": "celegans_20220830",
                                                                                    },
                                                                                    {
                                                                                        "label": "celegans_pharynx_20230203",
                                                                                        "value": "celegans_pharynx_20230203",
                                                                                    },
                                                                                    {
                                                                                        "label": "mf_20241112",
                                                                                        "value": "mf_20241112",
                                                                                    },
                                                                                    {
                                                                                        "label": "strongyle_eggs_20241226",
                                                                                        "value": "strongyle_eggs_20241226",
                                                                                    },
                                                                                ],
                                                                                value="20220830_all",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        # cellpose model type
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Cellpose Model Type:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Select(
                                                                                id="cellpose-model-type-segmentation",
                                                                                options=[
                                                                                    {
                                                                                        "label": "cellpose",
                                                                                        "value": "cellpose",
                                                                                    },
                                                                                    {
                                                                                        "label": "python",
                                                                                        "value": "python",
                                                                                    },
                                                                                ],
                                                                                value="cellpose",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        # cellpose model type
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Python Model Sigma:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="python-model-sigma",
                                                                                placeholder="0.2",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ],
                                                                    id="python-model-sigma-row",
                                                                    style={
                                                                        "display": "none"
                                                                    },
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        # cellpose wavelength selection
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Wavelength:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Select(
                                                                                id="wavelengths-segmentation",
                                                                                options=[
                                                                                    # {
                                                                                    #     "label": "All",
                                                                                    #     "value": "All",
                                                                                    # },
                                                                                    {
                                                                                        "label": "w1",
                                                                                        "value": "w1",
                                                                                    },
                                                                                    {
                                                                                        "label": "w2",
                                                                                        "value": "w2",
                                                                                    },
                                                                                    {
                                                                                        "label": "w3",
                                                                                        "value": "w3",
                                                                                    },
                                                                                    {
                                                                                        "label": "w4",
                                                                                        "value": "w4",
                                                                                    },
                                                                                ],
                                                                                value="w1",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                            ]
                                                        ),
                                                        html.Br(),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Img(
                                                            src="assets/configure_assets/fecundity/A01/img/20210906-p01-NJW_857_A01_binary.png",
                                                            style={"width": "40%"},
                                                            id="segmentation-input-preview",
                                                        ),
                                                        html.P(
                                                            "The fecundity pipeline exports a segmented image as a diagnostic and saves a single value as output.",
                                                            id="segmentation-input-text",
                                                        ),
                                                    ],
                                                    style={"textAlign": "center"},
                                                ),
                                                html.Hr(id = "segmentation-hr", style={"display": "none"}),
                                            ],
                                            id="segmentation_params",
                                            style={"display": "none"},
                                        ),
                                        dbc.Row(  # Tracking parameters for Cellprofiler pipeline
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H5(
                                                            "Cellprofiler Parameters:",
                                                        ),
                                                        html.Div(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.P(
                                                                                    "Cellprofiler pipeline:"
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Select(
                                                                                    id="cellprofiler-pipeline-selection",
                                                                                    options=[
                                                                                        {
                                                                                            "label": "Worm size and intensity",
                                                                                            "value": "wormsize_intensity_cellpose",
                                                                                        },
                                                                                        {
                                                                                            "label": "Microfilariae viability",
                                                                                            "value": "mf_celltox",
                                                                                        },
                                                                                        {
                                                                                            "label": "C. elegans feeding",
                                                                                            "value": "feeding",
                                                                                        },
                                                                                        {
                                                                                            "label": "C. elegans size",
                                                                                            "value": "wormsize",
                                                                                        },
                                                                                    ],
                                                                                    value="wormsize_intensity_cellpose",
                                                                                    persistence=True,
                                                                                    persistence_type="memory",
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        # cellpose model selection
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Cellpose Model:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Select(
                                                                                id="cellpose-model-cellprofiler",
                                                                                options=[
                                                                                    {
                                                                                        "label": "20220830_all",
                                                                                        "value": "20220830_all",
                                                                                    },
                                                                                    {
                                                                                        "label": "CP_20220801_scratch",
                                                                                        "value": "CP_20220801_scratch",
                                                                                    },
                                                                                    {
                                                                                        "label": "CP_20220803_LC4",
                                                                                        "value": "CP_20220803_LC4",
                                                                                    },
                                                                                    {
                                                                                        "label": "CP_20230203_155226_pharynx3",
                                                                                        "value": "CP_20230203_155226_pharynx3",
                                                                                    },
                                                                                ],
                                                                                value="20220830_all",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        # cellpose wavelength selection
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Wavelength:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Select(
                                                                                id="wavelengths-cellprofiler",
                                                                                options=[
                                                                                    # {
                                                                                    #     "label": "All",
                                                                                    #     "value": "All",
                                                                                    # },
                                                                                    {
                                                                                        "label": "w1",
                                                                                        "value": "w1",
                                                                                    },
                                                                                    {
                                                                                        "label": "w2",
                                                                                        "value": "w2",
                                                                                    },
                                                                                    {
                                                                                        "label": "w3",
                                                                                        "value": "w3",
                                                                                    },
                                                                                    {
                                                                                        "label": "w4",
                                                                                        "value": "w4",
                                                                                    },
                                                                                ],
                                                                                value="w1",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                            ]
                                                        ),
                                                        html.Br(),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Img(
                                                            id="cellprofiler-input-preview"
                                                        ),
                                                        html.P(
                                                            id="cellprofiler-input-text"
                                                        ),
                                                    ],
                                                    style={"textAlign": "center"},
                                                ),
                                            ],
                                            id="cellprofiler_params",
                                            style={"display": "none"},
                                        ),
                                        dbc.Row(  # Tracking parameters for Tracking pipeline
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H5(
                                                            "Tracking Parameters:",
                                                        ),
                                                        html.Div(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Diameter:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="tracking-diameter",
                                                                                placeholder="35",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Minimum Mass:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="tracking-minmass",
                                                                                placeholder="1200",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Noise Size:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="tracking-noisesize",
                                                                                placeholder="2",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Search Range:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="tracking-searchrange",
                                                                                placeholder="45",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Memory:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="tracking-memory",
                                                                                placeholder="25",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            html.P(
                                                                                "Adaptive Stop:"
                                                                            )
                                                                        ),
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                id="tracking-adaptivestop",
                                                                                placeholder="30",
                                                                                type="number",
                                                                                persistence=True,
                                                                                persistence_type="memory",
                                                                                style={
                                                                                    "display": "flex"
                                                                                },
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                        html.Br(),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Img(
                                                            src="assets/configure_assets/tracking/20240307-p01-RVH_A05_tracks.png",
                                                            style={"width": "40%"},
                                                            id="tracking-input-preview",
                                                        ),
                                                        html.P(
                                                            "The tracking pipeline exports tracks as a diagnostic and saves a single value per track as output.",
                                                            id="tracking-input-text",
                                                        ),
                                                    ],
                                                    style={"textAlign": "center"},
                                                ),
                                            ],
                                            id="tracking_params",
                                            style={"display": "none"},
                                        ),
                                    ],
                                )
                            ),
                        ],
                        # width=4,
                    ),
                    # dbc.Col(
                    #     [
                    #         html.Div(
                    #             [
                    #                 dbc.Row(
                    #                     [
                    #                         html.Img(id="configure-input-preview"),
                    #                         html.P(id="configure-input-text"),
                    #                     ],
                    #                     id="configure-input",
                    #                 ),
                    #             ],
                    #             style={"textAlign": "center"},
                    #         ),
                    #     ],
                    #     width=8,
                    # ),
                ],
            ),
        ]
    ),
    id="module-selection",
    title="Pipeline Selection",
)
