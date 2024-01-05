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
            for tab in metadata_tabs:
                tab_data = tab['props']['children'][0]['props']['children']['props']['data']
                df = pd.DataFrame(tab_data)
                tab_id = tab['props']['label']

                # Save the DataFrame to a CSV file
                file_path = f"/Users/zach/avacado_analytics/wrmXpress_github/wrmXpress-gui/practice_output_folder/{tab_id}.csv"
                df.to_csv(file_path, index=False)

            # Re-enable the button after saving
            return "danger"

        # Enable the button if not clicked
        return "success"

