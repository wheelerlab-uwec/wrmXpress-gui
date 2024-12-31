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
                    html.H5("Options:"),
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
                                                persistence=True,
                                            ),
                                            # Tooltip for static diagnostics
                                            dbc.Tooltip(
                                                "Run static diagnostics on the input data.",
                                                target="static-dx",
                                                placement="left",
                                            ),
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.P(
                                                        "Rescale multiplier:",
                                                        id="static-dx-rescale-label",
                                                    ),
                                                    dbc.Tooltip(
                                                        "Rescale multiplier is a number between 0 and 1 that determines the size of the output image.",
                                                        target="static-dx-rescale-label",
                                                        placement="left",
                                                    ),
                                                    dbc.Input(
                                                        placeholder="1",
                                                        type="number",
                                                        min=0,
                                                        max=1,
                                                        step=0.1,
                                                        persistence=True,
                                                        persistence_type="memory",
                                                        id="static-dx-rescale-input",
                                                    ),
                                                ],
                                                width=11,
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
                                                persistence=True,
                                            ),
                                            # Tooltip for video diagnostics
                                            dbc.Tooltip(
                                                "Run video diagnostics on the input data.",
                                                target="video-dx",
                                                placement="left",
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
                                                            },
                                                            # {
                                                            #     "label": "GIF",
                                                            #     "value": "gif",
                                                            # },
                                                            # {
                                                            #     "label": "NA",
                                                            #     "value": "NA",
                                                            # },
                                                        ],
                                                        value="avi",
                                                        persistence=True,
                                                        persistence_type="memory",
                                                    ),
                                                ],
                                                width=6,
                                                id="video-dx-format-column",
                                            ),
                                            dbc.Col(
                                                [
                                                    html.P(
                                                        "Rescale multiplier:",
                                                        id="video-rescale-multiplier-label",
                                                    ),
                                                    dbc.Tooltip(
                                                        "Rescale multiplier is a number between 0 and 1 that determines the size of the output video.",
                                                        target="video-rescale-multiplier-label",
                                                    ),
                                                    dbc.Input(
                                                        id="video-dx-rescale",
                                                        placeholder="0.5",
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
