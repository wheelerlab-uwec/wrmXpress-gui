########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

meta_data_from_input = dbc.Container([  # creating empty tabs for the metadata tables which will be populated in later
    dcc.Tabs(id='metadata-tabs', value='batch-data-tab', children=[

    ]
    )
]
)

metadata_checklist = dbc.Form([
    html.Div(
        [
            dbc.Checklist(  # Initial checklist for metadata tables
                options=[
                    {"label": "Batch",
                     "value": "Batch"},
                    {"label": "Species",
                     "value": "Species"},
                    {"label": "Strains",
                     "value": 'Strains'},
                    {"label": "Stages",
                     "value": "Stages"},
                    {"label": "Treatments",
                     "value": "Treatments"},
                    {'label': 'Concentrations',
                     'value': 'Concentrations'},
                    {'label': "Other",
                     'value': 'Other'},
                ],
                value=[
                    "Batch",
                    'Species',
                    'Strains',
                    'Stages',
                    'Treatments',
                    "Concentrations",
                    "Other"
                ],
                persistence=True,
                persistence_type='memory',
                id="checklist-input",
            ),
        ]
    )
])

selection_table = html.Div(
    # initializing selection table id which will be populated in later
    id='well-selection-table'
)
