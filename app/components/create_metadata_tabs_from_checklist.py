########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
from app.utils.create_df_from_user_input import create_empty_df_from_inputs


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

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################


def create_metadata_tables_from_checklist(app):
    @app.callback(
        [Output('metadata-tabs', 'children'),
         Output('metadata-tabs', 'value')],  # Added Output for setting the selected tab
        [Input('total-num-rows', 'value'),
         Input('total-well-cols', 'value'),
         Input("finalize-metadata-table-button", 'n_clicks')],
        [State("checklist-input", "value")]
    )
    def create_tabs_from_checklist(num_rows, num_cols, n_clicks, checklist_values):
        default_cols = 12
        default_rows = 8
        if num_rows is None:
            num_rows = default_rows
        if num_cols is None:
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
