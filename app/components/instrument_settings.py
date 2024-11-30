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

instrument_settings = dbc.AccordionItem(
    [
        html.Div(
            dbc.Row(
                [
                    html.H6("File structure:"),  # Title for File Structure
                    dbc.Col(
                        [
                            html.I(
                                className="fa-solid fa-circle-info",  # Information symbol
                                id="file-structure-symbol",
                            ),
                            dbc.Tooltip(
                                # Tooltip element for information symbol, displays message when cursor over the symbol
                                html.P(
                                    "Select ImageXpress if the data is saved in an IX-like structure (see Info). Select AVI if the data is a single video saved as an AVI.",
                                    style={"text-align": "left"},
                                ),
                                placement="bottom",
                                target="file-structure-symbol",
                                style={"text-align": "left"},
                            ),
                            dbc.RadioItems(
                                # Radio selection items for ImageXpress or AVI
                                id="file-structure",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "ImageXpress", "value": "imagexpress"},
                                    {"label": "AVI", "value": "avi"},
                                ],
                                value="imagexpress",
                                persistence=True,
                                persistence_type="memory",
                            ),
                        ],
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                html.P(
                                    "Cropping options:",  # text of cropping items
                                    style={
                                        "textDecoration": "underline",
                                        "cursor": "pointer",
                                    },
                                    id="crop-options",
                                )
                            ),
                            dbc.Tooltip(
                                [
                                    # Tooltip element for text "cropping items", displays message when cursor over the text
                                    html.P(
                                        "Select the method of cropping wells.",
                                        style={"text-align": "left"},
                                    ),
                                    html.P(
                                        "Auto: in development.",
                                        style={"text-align": "left"},
                                    ),
                                    html.P(
                                        "Grid: Crops a grid based on the provided number of columns and rows.",
                                        style={"text-align": "left"},
                                    ),
                                ],
                                placement="bottom",
                                target="crop-options",
                                style={"text-align": "left"},
                            ),
                            dbc.RadioItems(
                                # Radio button selection of Auto or Grid
                                id="multi-well-detection",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    # {"label": "Auto", "value": "auto"},
                                    {"label": "Grid", "value": "grid"},
                                ],
                                value="grid",
                                persistence=True,
                                persistence_type="memory",
                            ),
                        ],
                        width="auto",
                        id="additional-options-row",
                        style={"display": "flex"},
                    ),
                ],
                align="center",
            )
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        # Title for Imaging mode
                        html.H6("Imaging mode:", id="imaging-mode-header"),
                        dbc.Col(
                            [
                                html.I(
                                    className="fa-solid fa-circle-info",  # Information Symbol
                                    id="imaging-mode-symbol",
                                ),
                                dbc.Tooltip(
                                    # Tooltip element for information symbol, displays message when cursor over the symbol
                                    html.P(
                                        "Select Single Well if each video/image only includes a single well. Select Multi Well if each video/image contains multiple wells that need to be split. Select Multi Site if there is >1 site for each well.",
                                        style={"text-align": "left"},
                                    ),
                                    placement="bottom",
                                    target="imaging-mode-symbol",
                                ),
                                dbc.RadioItems(
                                    # Radio button selection for single well or multi well
                                    id="imaging-mode",
                                    className="btn-group",
                                    inputClassName="btn-check",
                                    labelClassName="btn btn-outline-primary",
                                    labelCheckedClassName="active",
                                    options=[
                                        {
                                            "label": "Single Well",
                                            "value": "single-well",
                                        },
                                        {"label": "Multi Well", "value": "multi-well"},
                                        {"label": "Multi Site", "value": "multi-site"},
                                    ],
                                    value="single-well",
                                    persistence=True,
                                    persistence_type="memory",
                                ),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    id="multi-well-row",  # Input values for rows per image
                                    placeholder="Rows per image",
                                    type="number",
                                    persistence=True,
                                    persistence_type="memory",
                                ),
                                dbc.Input(
                                    id="multi-well-col",  # Input values for columns per image
                                    placeholder="Columns per image",
                                    type="number",
                                    persistence=True,
                                    persistence_type="memory",
                                ),
                            ],
                            width="auto",
                            id="multi-well-options-row",
                            style={"display": "flex"},  # Initially hidden
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    id="x-sites",  # Input values for rows per image
                                    placeholder="X-sites per image",
                                    type="number",
                                    persistence=True,
                                    persistence_type="memory",
                                ),
                                dbc.Input(
                                    id="y-sites",  # Input values for columns per image
                                    placeholder="Y-sites per image",
                                    type="number",
                                    persistence=True,
                                    persistence_type="memory",
                                ),
                                dbc.Checklist(
                                    options=[{"label": "Stitch", "value": False}],
                                    id="stitch-switch",
                                    switch=True,
                                    style={"margin-top": "10px", 
                                           "margin-left": "10px"}, # adjust the position of the switch based on personal preference
                                ),
                            ],
                            width="auto",
                            id="multi-site-options-row",
                            style={
                                "display": "flex",
                            },
                        ),
                    ],
                    align="center",
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                # Label for Plate Format
                dbc.Col(html.H6("Plate format:")),
            ],
            align="center",
        ),
        dbc.Row(
            [
                # First Column: Image, Tooltip
                dbc.Col(
                    [
                        html.I(
                            className="fa-solid fa-circle-info",  # Information Symbol
                            id="tot-num-cols-and-rows-symbol",
                        ),
                        dbc.Tooltip(
                            html.P(
                                "Input the total number of rows and columns in the plate. If none provided, defaults to 12 columns and 8 rows",
                                style={"text-align": "left"},
                            ),
                            placement="bottom",
                            target="tot-num-cols-and-rows-symbol",
                            style={"text-align": "left"},
                        ),
                    ],
                    width="auto",
                ),
                # Second Column: Input for Total Number of Columns
                dbc.Col(
                    dbc.Input(
                        id="well-col",
                        placeholder="Columns = 12",
                        type="number",
                        persistence=True,
                        persistence_type="memory",
                    ),
                    width="auto",
                ),
                # Third Column: Input for Total Number of Rows
                dbc.Col(
                    dbc.Input(
                        id="well-row",
                        placeholder="Rows = 8",
                        type="number",
                        persistence=True,
                        persistence_type="memory",
                    ),
                    width="auto",
                    id="plate-foramt-options-row",
                ),
            ],
            align="center",
        ),
        html.Br(),
    ],
    id="instrument-settings-file-structure",  # id of accordian item
    title="Instrument Settings",  # Title of accordian item
)
