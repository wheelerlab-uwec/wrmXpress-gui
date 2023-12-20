########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
from app.components.selection_table import selection_table
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
run_time_settings = dbc.AccordionItem(
    [
        html.H4("Directories"),
        html.H6("Work"),
        dbc.Input(
            id="work-directory", placeholder="Please insert the work directory:", type="text"),
        html.H6("Input"),
        dbc.Input(
            id="input-directory", placeholder="Please insert the input directory:", type="text"),
        html.H6("Output"),
        dbc.Input(
            id="output-directory", placeholder="Please insert the output directory:", type="text"),
        html.Br(),

        html.H4("Wells"),
        html.P("Edit the following table such that well IDs are only present for wells to be analyzed.\
            Alternatively, edit the following field to include a list of comma-separated well IDs. \
                This list will override the contents of the table."),
        selection_table,
        html.Br(),
        html.P("List of wells to be analyzed:"),
        dbc.Card(
            dbc.CardBody(
                html.P(
                    id='well-selection-list'
                )
            )
        )
    ],
    id="run-time-settings",
    title="Run-Time Settings"
)