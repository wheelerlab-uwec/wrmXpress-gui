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
                tab_id = tab['props']['value']  # Get the tab ID
                table_id = f'{tab_id}-table'  # Construct the table ID

                # Find the correct table object inside the tab
                table_obj = None

                if table_obj:
                    # Get the data from the table
                    table_data = table_obj['props']['children']['props']['data']

                    # Convert the table data to a DataFrame
                    df = pd.DataFrame(table_data)

                    # Replace empty cells with "None"
                    df = df.where(pd.notnull(df), "None")

                    # Save the DataFrame to a CSV file
                    file_path = f"/Users/zach/avacado_analytics/wrmXpress_github/wrmXpress-gui/practice_output_folder/{tab_id}.csv"
                    df.to_csv(file_path, index=False)

            # Re-enable the button after saving
            return "danger"

        # Enable the button if not clicked
        return "success"
