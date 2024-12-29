########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

module_selection = dbc.AccordionItem(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Row(
                            [
                                html.H5("wrmXpress pipeline:"),
                                dbc.RadioItems(
                                    id="pipeline-selection",
                                    options=[
                                        {"label": "Motility", "value": "motility"},
                                        {"label": "Fecundity", "value": "fecundity"},
                                        {"label": "Tracking", "value": "tracking"},
                                        {
                                            "label": [
                                                html.I("C. elegans"),
                                                " size and intensity (Cellpose)",
                                            ],
                                            "value": "wormsize_intensity_cellpose",
                                        },
                                        {
                                            "label": "Microfilariae viability",
                                            "value": "mf_celltox",
                                        },
                                        {
                                            "label": [html.I("C. elegans"), " feeding"],
                                            "value": "feeding",
                                        },
                                        {
                                            "label": [html.I("C. elegans"), " size"],
                                            "value": "wormsize",
                                        },
                                    ],
                                    value=None,
                                    persistence=True,
                                    persistence_type="memory",
                                ),
                            ]
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.Img(id="configure-input-preview"),
                                    html.P(id="configure-input-text"),
                                ],
                                style={"textAlign": "center"},
                            ),
                        ],
                        width=8,
                    ),
                ],
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.Br(),
                        html.H5(
                            "Pipeline Parameters:",
                            id="pipeline-params-header",
                            style={"display": "none"},
                        ),
                        # html.Div(
                        #     id="pipeline-params",
                        # ),
                        dbc.Row(  # Tracking parameters for motility pipeline
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("Wavelength:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="wavelengths",
                                                        placeholder="Wavelength",
                                                        type="text",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("pyrScale:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="pyrscale",
                                                        placeholder="0.5",
                                                        type="number",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("Levels:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="levels",
                                                        placeholder="5",
                                                        type="number",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("Window size:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="winsize",
                                                        placeholder="20",
                                                        type="number",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("Iterations:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="iterations",
                                                        placeholder="7",
                                                        type="number",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("Poly N:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="poly_n",
                                                        placeholder="5",
                                                        type="number",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("Poly Sigma:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="poly_sigma",
                                                        placeholder="1.1",
                                                        step=0.1,
                                                        type="number",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.P("Flags:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="flags",
                                                        placeholder="0",
                                                        type="number",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            id="motility_params",
                            style={"display": "none"},
                        ),
                        dbc.Row(  # Tracking parameters for fecundity pipeline
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                # cellpose model selection
                                                dbc.Col(html.P("Cellpose Model:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="cellpose-model-segmentation",
                                                        placeholder="cyto",
                                                        type="text",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                # cellpose model type
                                                dbc.Col(html.P("Cellpose Model Type:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="cellpose-model-type-segmentation",
                                                        placeholder="cytoplasm",
                                                        type="text",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                # cellpose wavelength selection
                                                dbc.Col(html.P("Wavelength:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="wavelengths-segmentation",
                                                        placeholder="Wavelength",
                                                        type="text",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ]
                                )
                            ],
                            id="fecundity_params",
                            style={"display": "none"},
                        ),
                        dbc.Row(  # Tracking parameters for wrmsize, mf_celltox, and feeding pipelines
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                # cellpose model selection
                                                dbc.Col(html.P("Cellpose Model:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="cellpose-model-cellprofile",
                                                        placeholder="cyto",
                                                        type="text",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                # cellpose model type
                                                # dbc.Col(html.P("Cellpose Model Type:")),
                                                # dbc.Col(
                                                #     dbc.Input(
                                                #         id="cellpose-model-type-cellprofile",
                                                #         placeholder="cytoplasm",
                                                #         type="text",
                                                #         persistence=True,
                                                #         persistence_type="memory",
                                                #         style={"display": "flex"},
                                                #     ),
                                                # ),
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                # cellpose wavelength selection
                                                dbc.Col(html.P("Wavelength:")),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="wavelengths-cellprofile",
                                                        placeholder="Wavelength",
                                                        type="text",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        style={"display": "flex"},
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                            id="cellprofile_params",
                            style={"display": "none"},
                        ),
                    ],
                    width=4,
                )
            ),
        ]
    ),
    id="module-selection",
    title="Pipeline Selection",
)
