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

meta_data_from_input = dbc.Container([
    dcc.Tabs(id='metadata-tabs', value='batch-data-tab', children=[

    ]
    )
]
)

metadata_checklist = dbc.Form([
    html.Div(
        [
            dbc.Checklist(
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
                    "Batch", 'Species', 'Strains', 'Stages', 'Treatments', "Concentrations", "Other"],
                persistence=True,
                persistence_type='session',
                id="checklist-input",
            ),
        ]
    )
])

selection_table = html.Div(
    id='well-selection-table'
)
