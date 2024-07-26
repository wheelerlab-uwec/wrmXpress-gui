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
                        dbc.Col(
                            [
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
                                    target="volume-path-label",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.H6("Volume Path:", id="volume-path-label"),
                                dbc.Input(  # Input field for the mounted volume path
                                    id="mounted-volume",
                                    placeholder="Path",
                                    type="text",
                                    persistence=True,
                                    persistence_type="memory",
                                ),
                            ],
                            width="middle",
                        ),
                    ],
                    align="center",
                )
            ]
        ),
        html.Br(),  # Line break for spacing
        html.H6("Plate/Folder name:"),  # Label for the plate/folder name input field
        dbc.Input(  # Input field for the plate/folder name
            id="plate-name",
            placeholder="Name",
            type="text",
            persistence=True,
            persistence_type="memory",
        ),
        html.Br(),  # Line break for spacing
        html.Div(
            [
                dbc.Row(
                    [  # Row for wells input with info symbol and tooltip
                        dbc.Col(
                            [
                                dbc.Tooltip(
                                    html.P(
                                        "To multi select, hold down shift and use arrows, or copy paste from csv or from a document.",
                                        style={"text-align": "left"},
                                    ),
                                    placement="left",
                                    target="well-table-header",
                                ),
                                html.H4("Wells", id="well-table-header"),
                            ],
                            width="auto",  # Width of the column
                        ),  # Section header for wells
                    ],
                    align="center",  # Center align the row
                ),
                html.P(
                    "Edit the following table such that well IDs are only present for wells to be analyzed."
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
