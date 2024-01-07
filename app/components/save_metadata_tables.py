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
from pathlib import Path
import os

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################


def save_metadata_tables_to_csv(app):
    @app.callback(
        Output("save-meta-data-to-csv", 'color'),
        Input("save-meta-data-to-csv", "n_clicks"),
        State('metadata-tabs', 'children'),
        State('mounted-volume', 'value')
    )
    def save_the_metadata_tables_to_csv(n_clicks, metadata_tabs, volume):
        if n_clicks:

            # Iterate over the metadata tabs
            for tab in metadata_tabs:
                tab_data = tab['props']['children'][0]['props']['children']['props']['data']
                tab_id = tab['props']['label']
                tab_id = tab_id.lower()

                df = pd.DataFrame(tab_data)
                current_columns_order = df.columns.tolist()
                # Define a mapping of column names to integer values (except for 'index')
                column_order_mapping = {'index': -1}
                for i, col in enumerate(current_columns_order):
                    if col != 'index':
                        column_order_mapping[col] = int(col)

                # Sort the columns based on their values in the mapping
                sorted_columns = sorted(
                    current_columns_order, key=lambda col: column_order_mapping[col])
                sorted_columns = list(sorted_columns)
                sorted_columns = sorted_columns[1:]

                # Reorder the DataFrame columns
                df = df[sorted_columns]

                # Save the DataFrame to a CSV file
                metadata_dir = Path(volume).joinpath('metadata')
                if not metadata_dir.exists():
                    metadata_dir.mkdir(parents=True, exist_ok=True)
                file_path = metadata_dir.joinpath(f"{tab_id}.csv")
                df.to_csv(file_path, index=False, header=False)

        # Enable the button if not clicked
        return "success"
