########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################
def save_metadata_tables_to_csv(app):
    @app.callback(
        Output("save-meta-data-to-csv", 'color'),
        Input("save-meta-data-to-csv", "n_clicks"),
        State('metadata-tabs', 'children')
    )
    def save_the_metadata_tables_to_csv(n_clicks, metadata_tabs):
        if n_clicks:
            # Iterate over the metadata tabs
            

            # Re-enable the button after saving
            return "danger"

        # Enable the button if not clicked
        return "success"
