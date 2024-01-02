########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash
from app.utils.create_df_from_user_input import create_empty_df_from_inputs


########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

metadata_checklist = dbc.Form([
                                html.Div(
                                    [
                                        dbc.Label("Choose the Metadata Tables"),
                                        dbc.Checklist(
                                            options=[
                                                {"label": "Batch", "value": "batch"},
                                                {"label": "Species", "value": "species"},
                                                {"label": "Strains", "value": 'strains'},
                                                {"label": "Stages", "value": "stages"},
                                                {"label": "Treatements", "value": "treatments"},
                                                {'label':'Concentrations', 'value':'concentration'},
                                                {'label': "Other", 'value': 'other'},
                                            ],
                                            value=["batch", 'species', 'strains', 'stages', 'treatments', "concentration", "other"],
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
