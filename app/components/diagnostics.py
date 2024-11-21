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
        dbc.Row(
            [
                html.H5("Diagnostic Options:"),
                dbc.Col(
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
                        html.Div(
                            [
                                html.P("Rescale multiplier:"),
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
                            id="static-dx-rescale",
                        ),
                    ]
                ),
                dbc.Col(
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
                        html.Div(
                            [
                                html.P("Output format:"),
                                dbc.Select(
                                    id="video-dx-format",
                                    options=[
                                        {"label": "AVI", "value": "avi"},
                                    ],
                                    value="NA",
                                    persistence=True,
                                    persistence_type="memory",
                                ),
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
                            id="video-dx-options",
                        ),
                    ],
                ),
            ],
        ),
    ),
    id="dx",
    title="Run Diagnostics",
)
