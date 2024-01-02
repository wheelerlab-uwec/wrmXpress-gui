########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
from app.components.selection_table import selection_table
import dash_bootstrap_components as dbc
from dash import html
from app.utils.create_df_from_user_input import create_df_from_inputs
from dash.dependencies import Input, Output, State
from dash import dash_table
import itertools

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
# Run time accordian items for main page layout
run_time_settings = dbc.AccordionItem(
    [
        html.H4("Directories"),
        html.H6("Volume"),
        dbc.Input(
            id="mounted-volume", placeholder="Please insert the path to the local mounted volume:", type="text"),
        html.Br(),
        html.H6("Plate/Folder"),
        dbc.Input(
            id="plate-name", placeholder="Please insert the plate name:", type="text"),
        html.Br(),
        html.H4("Wells"),
        html.P("Edit the following table such that well IDs are only present for wells to be analyzed.\
            Alternatively, edit the following field to include a list of comma-separated well IDs. \
                This list will override the contents of the table."),
        # Selection Table from selection_table.py acquired from imports
        selection_table,
        html.Br(),
        html.Div([
            html.P("List of wells to be analyzed:"),
            dbc.Card(
                dbc.CardBody(
                    html.P(
                        id='well-selection-list'
                    )
                )
            )],
            style={'display':'none'})
        
    ],
    id="run-time-settings",
    title="Run-Time Settings"
)

########################################################################
####                                                                ####
####                              Callbacks                         ####
####                                                                ####
########################################################################
def update_well_selection_table(app):
    @app.callback(
        Output("well-selection-table", 'children'),
        [Input("total-num-rows", "value"),
        Input("total-well-cols", "value")]
    )
    def update_table(rows, cols):
        default_cols = 12
        default_rows = 8
        if rows is None:
            rows = default_rows
        if cols is None:
            cols = default_cols
        
        df = create_df_from_inputs(rows, cols)
        well_selection = dash_table.DataTable(
            data=df.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-well-selection-table'
        )
        return well_selection
    
def populate_list_of_wells(app):
    # Populate list of wells to be analyzed
    @app.callback(
        Output('well-selection-list', 'children'),
        Input('dynamic-table-container-well-selection-table', 'data')
    )
    def update_wells(table_contents):
        values_list = [list(d.values()) for d in table_contents]
        flattened_list = list(itertools.chain.from_iterable(values_list))
        filtered_list = []
        for item in flattened_list:
            if item is None:
                continue
            elif len(item) == 1:
                continue
            else:
                filtered_list.append(item)
        # filtered_list = [item for item in flattened_list if item is None or len(item) > 1]
        sorted_list = sorted(filtered_list)

        return sorted_list