########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
worm_information = dbc.AccordionItem(
    [
        html.H6("Species:"),
        dbc.RadioItems(
            id="species",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Brugia malayi", "value": "Bma"},
                {"label": "Caenorhabditis elegans", "value": "Cel"},
                {"label": "Schistosoma mansoni", "value": "Sma"}
            ],
            value="Bma",
        ),
        html.H6("Stages:"),
        dbc.RadioItems(
            id="stages",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Mf", "value": "Mf"},
                {"label": "Adult", "value": "Adult"},
                {"label": "Mixed", "value": "Mixed"},
            ],
            value="Mf",
        ),
    ],
    id="worm-information",
    title="Worm Information"
)