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

diagnostics = dbc.AccordionItem(
    dbc.Container(
        # Wrap the Row in a list
        children=[
            dbc.Row(
                [
                    html.H5("Diagnostic Options:"),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Checklist(
                                                options=[
                                                    {
                                                        "label": "Static diagnostics",
                                                        "value": "True",
                                                    },
                                                ],
                                                id="static-dx",
                                            ),
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.P("Rescale multiplier:")
                                                    ],
                                                    width=3
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Input(
                                                        placeholder="1",
                                                        type="number",
                                                        min=0,
                                                        max=1,
                                                        step=0.1,
                                                        persistence=True,
                                                        persistence_type="memory",
                                                    ),
                                                ],
                                                width=9,
                                            ),
                                        ],
                                        id="static-dx-rescale",
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Checklist(
                                                options=[
                                                    {
                                                        "label": "Video diagnostics",
                                                        "value": "True",
                                                    },
                                                ],
                                                id="video-dx",
                                            ),
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.P("Output format:"),
                                                    dbc.Select(
                                                        id="video-dx-format",
                                                        options=[
                                                            {
                                                                "label": "AVI",
                                                                "value": "avi",
                                                            }
                                                        ],
                                                        value="NA",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                    ),
                                                ],
                                                width=6,
                                                id="video-dx-format",
                                            ),
                                            dbc.Col(
                                                [
                                                    html.P("Rescale multiplier:"),
                                                    dbc.Input(
                                                        id="video-dx-rescale",
                                                        placeholder="1",
                                                        type="number",
                                                        min=0,
                                                        max=1,
                                                        step=0.1,
                                                        persistence=True,
                                                        persistence_type="memory",
                                                    ),
                                                ],
                                                width=6,
                                            ),
                                        ],
                                        id="video-dx-options",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ],  # This is where the issue was, now it's wrapped in a list
    ),
    id="dx",
    title="Run Diagnostics",
)
