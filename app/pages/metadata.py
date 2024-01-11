########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, callback, dash_table
import pandas as pd
from pathlib import Path

# components
from app.components.metadata_components import metadata_checklist

# utilities
from app.utils.callback_functions import create_empty_df_from_inputs

dash.register_page(__name__)

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

layout = dbc.Container(
    [
        html.Div(
            [
                metadata_checklist,
                html.Br(),
                dbc.Row(
                    [
                        # Label for Plate Format
                        dbc.Col(html.H6("Add new table:")),
                    ],
                    align="center"
                ),
                dbc.Row(
                    [
                        # First Column: Input for Total Number of Columns
                        dbc.Col(
                            dbc.Button(
                                "+",
                                id="add-metadata-table-button",
                                className="me-2",
                            ),
                            width="auto",
                            className='pe-0'
                        ),
                        dbc.Col(
                            # Add an editable input box here
                            dbc.Input(
                                id="uneditable-input-box",
                                placeholder='Title',
                                value="",
                                disabled=False
                            ),
                            width="auto",
                            className='ps-0'
                        ),
                    ],
                    align="center"
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Finalize Tables",
                                id="finalize-metadata-table-button",
                                className="flex",
                                color='success'
                            ),
                            width="auto"
                        ),
                    ],
                    justify="center"
                ),
                html.Br(),
                html.Br(),
                dbc.Container([
                    dcc.Tabs(id='metadata-tabs', value='batch-data-tab', children=[
                    ]
                    )
                ]
                ),
                html.Br(),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            "Save metadata",
                            id='save-meta-data-to-csv',
                            color='success',
                            n_clicks=0
                        ),
                        width='auto'
                    )
                )
            ]
        )
    ],
    # adjust white space between metadata tab and tabs of metadata content
    style={"paddingTop": "80px"}
)

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################


@callback(
    [Output('metadata-tabs', 'children'),
     Output('metadata-tabs', 'value')],
    [State('store', 'data'),
     Input("finalize-metadata-table-button", 'n_clicks')],
    [State("checklist-input", "value")],

)
def create_tabs_from_checklist(store, n_clicks, checklist_values):
    default_cols = 12
    default_rows = 8
    try:
        num_rows = store['rows']
    except:
        num_rows = default_rows
    try:
        num_cols = store['cols']
    except:
        num_cols = default_cols

    df_empty = create_empty_df_from_inputs(num_rows, num_cols)
    if n_clicks and checklist_values:
        # Create a list of dcc.Tab components from the checked items
        tabs = [
            dcc.Tab(label=value, value=f"{value}-tab", children=[
                html.Div(dash_table.DataTable(
                    data=df_empty.reset_index().to_dict('records'),
                    columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
                    [{'name': col, 'id': col} for col in df_empty.columns],
                    editable=True,
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'center'},
                    id=f'{value}-tab-table'
                )
                )
            ])  # Create a Tab for each checked item
            for value in checklist_values
        ]
        # Set the value of the first tab as the selected tab
        selected_tab = f'{checklist_values[0]}-tab'
        return tabs, selected_tab
    else:
        # If no checklist values are available, return an empty list and set 'batch-data-tab' as the selected tab
        return [], 'batch-data-tab'


@callback(
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


@callback(
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
