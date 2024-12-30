########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
from dash import dcc, html, callback, dash_table, Input, Output, State
import pandas as pd
from pathlib import Path
import os

# functions
from app.utils.callback_functions import create_na_df_from_inputs
from app.components.metadata_layout import metadata_layout

# registering dash page
dash.register_page(__name__)

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

layout = metadata_layout

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################


@callback(
    [
        Output("metadata-tabs", "children"),
        Output("metadata-tabs", "value"),
        Output("finalize-metadata-table-button", "color"),
    ],
    [State("store", "data"), Input("finalize-metadata-table-button", "n_clicks")],
    [State("checklist-input", "value")],
    prevent_initial_call=True,
)
# creating empty dash tables from metadata checklist with proper dimensions from rows and columns
def create_tabs_from_checklist(store, n_clicks, checklist_values):
    """
    This function creates a list of dcc.Tab components from the checklist values
    """
    default_cols = 12
    default_rows = 8

    # attempting to catch any errors that may occur
    # if the rows are not available, set them to the default values
    try:
        if store["rows"] is not None:
            num_rows = store["rows"]
        else:
            num_rows = default_rows
    except KeyError:
        num_rows = default_rows

    # if the columns are not available, set them to the default values
    try:
        if store["cols"] is not None:
            num_cols = store["cols"]
        else:
            num_cols = default_cols
    except KeyError:
        num_cols = default_cols

    # Create an empty DataFrame with the specified dimensions, see callback_functions.py
    df_na = create_na_df_from_inputs(num_rows, num_cols)
    if (
        n_clicks and checklist_values
    ):  # If the checklist values are available and the button has been clicked

        # Create a list of dcc.Tab components from the checked items
        tabs = [
            dcc.Tab(
                label=value,
                value=f"{value}-tab",
                children=[
                    html.Div(
                        dash_table.DataTable(
                            data=df_na.reset_index().to_dict("records"),
                            columns=[{"name": "Row", "id": "index", "editable": False}]
                            + [{"name": col, "id": col} for col in df_na.columns],
                            editable=True,
                            style_table={"overflowX": "auto"},
                            style_cell={"textAlign": "center"},
                            id=f"{value}-tab-table",
                        )
                    )
                ],
            )  # Create a Tab for each checked item
            for value in checklist_values  # Iterate over the checklist values
        ]

        # Set the value of the first tab as the selected tab
        selected_tab = f"{checklist_values[0]}-tab"
        return tabs, selected_tab, "success"
    else:
        # If no checklist values are available, return an empty list and set 'batch-data-tab' as the selected tab
        return [], "batch-data-tab", "primary"


@callback(
    Output("checklist-input", "options"),
    [Input("add-metadata-table-button", "n_clicks")],
    [State("uneditable-input-box", "value"), State("checklist-input", "options")],
)
# creating additional checklist items from user input
def update_metadata_checklist(n_clicks, new_table_name, existing_options):
    """
    This function updates the checklist options with the new table name
    """
    if (
        n_clicks and new_table_name
    ):  # If the button has been clicked and the new table name is available

        # Append the new table name to the existing options
        new_option = {"label": new_table_name, "value": new_table_name}
        updated_options = existing_options + [
            new_option
        ]  # Append the new table name to the existing options
        return updated_options  # Return the updated options
    else:
        return existing_options  # Return the existing options


@callback(
    [
        Output("save-meta-data-to-csv", "color"),
        Output("metadata-saved-alert", "is_open"),
        Output("metadata-saved-alert", "children"),
        Output("metadata-saved-alert", "color"),
        Output("save-meta-data-to-csv", "disabled"),
    ],
    Input("save-meta-data-to-csv", "n_clicks"),
    State("metadata-tabs", "children"),
    State("store", "data"),
)
# saving metadata tables
def save_the_metadata_tables_to_csv(n_clicks, metadata_tabs, store):
    """
    This function saves the metadata tables to a CSV file
    """
    # If no store is available, return an error message and disable the button
    if not store:
        return (
            "primary",
            True,
            "No configuration found. Please go to the configuration page to set up the analysis.",
            "danger",
            True,
        )

    # check if the store values are none
    if store["mount"] is None or store["platename"] is None:
        return (
            "primary",
            True,
            "No configuration found. Please go to the configuration page to set up the analysis.",
            "danger",
            True,
        )

    if (
        n_clicks
    ):  # If the button has been clicked and store values from the configuration page are available

        # Iterate over the metadata tabs
        for tab in metadata_tabs:
            tab_data = tab["props"]["children"][0]["props"]["children"]["props"][
                "data"
            ]  # Get the data from the tab
            tab_id = tab["props"]["label"]  # Get the label of the tab
            tab_id = tab_id.lower()  # Convert the label to lowercase

            df = pd.DataFrame(tab_data)
            current_columns_order = df.columns.tolist()  # Get the current columns order

            # Define a mapping of column names to integer values (except for 'index')
            column_order_mapping = {"index": -1}
            for i, col in enumerate(
                current_columns_order
            ):  # Iterate over the current columns order
                if col != "index":  # All of the columns that are not 'index'
                    column_order_mapping[col] = int(
                        col
                    )  # Add the column to the column order mapping

            # Sort the columns based on their values in the mapping
            sorted_columns = sorted(
                current_columns_order, key=lambda col: column_order_mapping[col]
            )
            sorted_columns = list(
                sorted_columns
            )  # Convert the sorted columns to a list
            sorted_columns = sorted_columns[1:]

            # Reorder the DataFrame columns
            df = df[sorted_columns]

            volume = store["mount"]  # Get the volume from the store
            plate = store["platename"]

            # Save the DataFrame to a CSV file
            metadata_dir = Path(volume).joinpath(
                "metadata"
            )  # Join the volume and the metadata directory

            # If the metadata directory does not exist, create it
            if not metadata_dir.exists():
                metadata_dir.mkdir(parents=True, exist_ok=True)

            # Save the DataFrame to a CSV file
            file_path = metadata_dir.joinpath(plate, f"{tab_id}.csv")

            # Get the directory path and make if not there
            directory_path = os.path.dirname(file_path)

            if os.path.exists(metadata_dir.joinpath(plate)) == False:
                os.mkdir(metadata_dir.joinpath(plate))

            df.to_csv(file_path, index=False, header=False)

        # Enable the button if not clicked
        return (
            "success",
            True,
            f"Metadata tables saved to destination: {directory_path}",
            "success",
            False,
        )
    else:
        return "primary", False, "", "success", False


@callback(
    Output("checklist-input", "value"),  # Update the values of the checklist
    [
        Input(
            "select-all-metadata-tables", "n_clicks"
        ),  # Button for selecting all items
        Input(
            "deselect-all-metadata-tables", "n_clicks"
        ),  # Button for deselecting all items
    ],
    [State("checklist-input", "options")],  # Existing options of the checklist
    prevent_initial_call=True,
)
# Callback for the 'Select All' and 'Deselect All' buttons
def select_deselect_all(select_all_clicks, deselect_all_clicks, checklist_options):
    ctx = dash.callback_context  # Getting context to find which button was clicked
    if not ctx.triggered:  # If no button was clicked, return no update
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[
            0
        ]  # Get the ID of the button that was clicked

    if button_id == "select-all-metadata-tables" and select_all_clicks:
        # If 'Select All' was clicked, return all the values to be selected
        return [option["value"] for option in checklist_options]
    elif button_id == "deselect-all-metadata-tables" and deselect_all_clicks:
        # If 'Deselect All' was clicked, return an empty list to deselect all
        return []

    return dash.no_update  # In case of any other condition, don't update
