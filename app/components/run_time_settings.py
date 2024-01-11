########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
from app.components.metadata_components import selection_table
import dash_bootstrap_components as dbc
from dash import html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
# Run time accordian items for main page layout
run_time_settings = dbc.AccordionItem(
    [
        html.H4("Directories"),
        html.H6("Volume"),
        dbc.Input(
            id="mounted-volume", placeholder="Path to the mounted volume", type="text", persistence=True,
            persistence_type='session'),
        html.Br(),
        html.H6("Plate/Folder"),
        dbc.Input(
            id="plate-name", placeholder="Plate name", type="text", persistence=True,
            persistence_type='session'),
        html.Br(),
        html.H4("Wells"),
        html.P(
            "Edit the following table such that well IDs are only present for wells to be analyzed."),
        # Selection Table from selection_table.py acquired from imports
        selection_table,
        html.Br(),
        html.Div([
            html.P("List of wells to be analyzed:"),
            dbc.Card(
                dbc.CardBody(
                    html.P(
                        id='well-selection-list'
                    )
                )
            )],
            style={'display': 'none'})

    ],
    id="run-time-settings",
    title="Run-Time Settings"
)
