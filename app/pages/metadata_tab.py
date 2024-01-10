########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, callback, dash_table

# components
from app.components.metadata_table_checklist import metadata_checklist
from app.components.create_metadata_tabs_from_checklist import meta_data_from_input

# utilities
from app.utils.create_df_from_user_input import create_df_from_inputs, create_empty_df_from_inputs

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


@callback(
    [Output("table-container-batch", "children"),
     Output("table-container-species", "children"),
     Output("table-container-strains", "children"),
     Output("table-container-stages", "children"),
     Output("table-container-treatments", "children"),
     Output("table-container-conc", "children"),
     Output("table-container-other", "children"),
     Output("well-selection-table", 'children')
     ],
    State('store', 'data'),
    [Input("total-num-rows", "value"),
     Input("total-well-cols", "value")]
)
def update_table(store, rows, cols):
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

    df = create_df_from_inputs(rows, cols)
    df_empty = create_empty_df_from_inputs(rows, cols)
    table_batch = dash_table.DataTable(
        data=df_empty.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-batch'
    )
    table_species = dash_table.DataTable(
        data=df_empty.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-species'
    )
    table_stages = dash_table.DataTable(
        data=df_empty.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-stages'
    )
    table_strains = dash_table.DataTable(
        data=df_empty.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-strains'
    )
    table_treatment = dash_table.DataTable(
        data=df_empty.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-species'
    )
    table_conc = dash_table.DataTable(
        data=df_empty.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-conc'
    )
    table_other = dash_table.DataTable(
        data=df_empty.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-other'
    )
    well_selection = dash_table.DataTable(
        data=df.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-well-selection-table'
    )
    return table_batch, table_species, table_strains, table_stages, table_treatment, table_conc, table_other, well_selection


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
