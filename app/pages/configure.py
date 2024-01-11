########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
import dash
from dash import callback
from dash.dependencies import Input, Output
from app.utils.callback_functions import create_df_from_inputs
from dash import dash_table
import itertools

# Importing Components
from app.components.instrument_settings import instrument_settings
from app.components.worm_information import worm_information
from app.components.module_selection import module_selection
from app.components.run_time_settings import run_time_settings

# Registering this page
dash.register_page(__name__)

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################
layout = dbc.Container([
    dbc.Accordion(
        [
            # Order of the Accordian item in which they appear in the app
            instrument_settings,
            worm_information,
            module_selection,
            run_time_settings,
        ],
        start_collapsed=False,
        always_open=True,
    ),
],
    style={"paddingTop": "80px"})  # Adjust the white space between tab and accordian elements


########################################################################
####                                                                ####
####                              Callback                          ####
####                                                                ####
########################################################################
@callback(
    [Output('multi-well-options-row', 'style'),
     Output('additional-options-row', 'style')],
    [Input('imaging-mode', 'value'),
     Input('file-structure', 'value')]
)
def update_options_visibility(imaging_mode, file_structure): # appearing selections upon meeting certain critera
    multi_well_options_style = {'display': 'none'}
    additional_options_style = {'display': 'none'}

    if imaging_mode == 'multi-well':
        multi_well_options_style = {'display': 'flex'}

        if file_structure == 'avi':
            additional_options_style = {'display': 'flex'}

    return multi_well_options_style, additional_options_style


@callback( # Storing values of inputs to be used in different pages
    Output("store", "data"),
    Input("total-well-cols", "value"),
    Input("total-num-rows", "value")
)
def rows_cols(cols, rows):
    return {'cols': cols, 'rows': rows}


@callback( 
    Output("well-selection-table", 'children'),
    [Input("total-num-rows", "value"),
     Input("total-well-cols", "value")]
)
def update_table(rows, cols): # creating a selection table based on the dimensions of rows and columns selected
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

# Populate list of wells to be analyzed
@callback(
    Output('well-selection-list', 'children'),
    Input('dynamic-table-container-well-selection-table', 'data')
)
def update_wells(table_contents): # list of cells from selection table
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
