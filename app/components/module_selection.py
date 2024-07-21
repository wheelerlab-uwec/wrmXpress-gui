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
                        [
                            html.H5("wrmXpress Pipeline:"),
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
                                value="False",
                                persistence=True,
                                persistence_type="memory",
                            ),
                        ],
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
        ]
    ),
    id="module-selection",
    title="Pipeline Selection",
)
