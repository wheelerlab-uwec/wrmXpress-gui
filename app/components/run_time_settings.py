########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

from app.components.metadata_layout import selection_table
import dash_bootstrap_components as dbc
from dash import html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

# Define the accordion item for run-time settings
run_time_settings = dbc.AccordionItem(
    [  # Accordion content starts here
        html.Div(
            [
                dbc.Row(
                    [
                        # Title for Imaging mode
                        html.H5("Directories", id="directories-mode-header"),
                        dbc.Tooltip(
                            [
                                # Tooltip element for information symbol, displays message when cursor over the symbol
                                html.P(
                                    "Running in Docker: use `/home/`.",
                                    style={"text-align": "left"},
                                ),
                                html.P(
                                    "Running natively: use the path to the parent directory that contains a directory of images.",
                                    style={"text-align": "left"},
                                ),
                            ],
                            placement="left",
                            target="mounted-info-icon",
                        ),
                        html.H6("Volume path:", id="volume-path-label"),
                        html.Div(
                            [
                                html.I(
                                    className="fa-solid fa-circle-info",  # Information symbol
                                    id="mounted-info-icon",
                                    style={
                                        "margin-right": "20px"
                                    },  # Add some space between icon and input
                                ),
                                dbc.Input(  # Input field for the mounted volume path
                                    id="mounted-volume",
                                    placeholder="Path",
                                    type="text",
                                    persistence=True,
                                    persistence_type="memory",
                                    style={
                                        "flex": "2"
                                    },  # Make the input take remaining space
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                            },
                        ),
                    ],
                    align="center",
                )
            ]
        ),
        html.Br(),  # Line break for spacing
        html.Div(
            [
                dbc.Row(
                    [
                        html.H6(
                            "Plate name:"
                        ),  # Label for the plate/folder name input field
                        html.Div(
                            [
                                dbc.Tooltip(
                                    html.P(
                                        "Name of the folder that contains imaging data structured as shown in Info.",
                                        style={"text-align": "left"},
                                    ),
                                    placement="left",
                                    target="plate-info-icon",
                                ),
                                html.I(
                                    className="fa-solid fa-circle-info",
                                    id="plate-info-icon",
                                    style={"margin-right": "20px"},
                                ),
                                dbc.Input(  # Input field for the plate/folder name
                                    id="plate-name",
                                    placeholder="Name",
                                    type="text",
                                    persistence=True,
                                    persistence_type="memory",
                                    style={"flex": "2"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                            },
                        ),
                    ]
                ),
            ]
        ),
        html.Br(),  # Line break for spacing
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Wells", id="well-table-header"),
                            ],
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
                html.Div(
                    [
                        dbc.Tooltip(
                            html.P(
                                "To select a range of wells, hold down Shift + ←↑→↓, or copy/paste from a spreadsheet.",
                                style={"text-align": "left"},
                            ),
                            placement="left",
                            target="well-info-icon",
                        ),
                        html.I(
                            className="fa-solid fa-circle-info",
                            id="well-info-icon",
                            style={"margin-right": "20px"},
                        ),
                        html.H6(
                            "Edit the following table such that well IDs are only present for wells to be analyzed.",
                            style={
                                "text-align": "left",
                                "flex": "2",
                                "display": "flex",
                                "align-items": "center",
                                "margin-top": "5px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "align-items": "center",  # Align items vertically centered
                    },
                ),
            ]
        ),
        # Placeholder for selection_table, assuming imported from another module
        selection_table,
        html.Br(),  # Line break for spacing
        html.Div(
            [  # Div for displaying the list of wells to be analyzed
                html.P("List of wells to be analyzed:"),
                dbc.Card(
                    dbc.CardBody(
                        html.P(
                            id="well-selection-list"
                        )  # Placeholder for the dynamic list of selected wells
                    )
                ),
            ],
            style={
                "display": "none"
            },  # Initially hidden, can be shown based on certain conditions
        ),
    ],
    id="run-time-settings",  # ID for the accordion item
    title="Run-Time Settings",  # Title of the accordion item
)
