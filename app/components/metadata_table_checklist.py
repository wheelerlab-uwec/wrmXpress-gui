########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State


########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

metadata_checklist = dbc.Form([
    html.Div(
        [
            dbc.Label(
                "Choose the metadata tables"),
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
                id="checklist-input",
            ),
        ]
    )
])


########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################

def add_metadata_table_checklist(app):
    @app.callback(
        Output("checklist-input", "options"),
        [Input("add-metadata-table-button", "n_clicks")],
        [State("uneditable-input-box", 'value'),
         State("checklist-input", "options")]
    )
    def update_metadata_checklist(n_clicks, new_table_name, existing_options):
        if n_clicks and new_table_name:
            # Append the new table name to the existing options
            new_option = {"label": new_table_name, "value": new_table_name}
            updated_options = existing_options + [new_option]
            return updated_options
        else:
            return existing_options
