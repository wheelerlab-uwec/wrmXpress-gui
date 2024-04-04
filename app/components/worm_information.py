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

# Worm Information accordion items
worm_information = dbc.AccordionItem(
    [
        html.H6("Species:"),
        # Radio button items for species with italicized labels
        dbc.RadioItems(
            id="species",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": html.I("Brugia malayi"), "value": "Bma"},
                {"label": html.I("Caenorhabditis elegans"), "value": "Cel"},
                {"label": html.I("Schistosoma mansoni"), "value": "Sma"}
            ],
            value="Bma",
            persistence=True,
            persistence_type='memory'
        ),
        html.H6("Stages:"),
        # Radio button items for stage information
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
            persistence=True,
            persistence_type='memory'
        ),
    ],
    id="worm-information",
    title="Worm Information"
)
