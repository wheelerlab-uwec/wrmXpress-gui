########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output, State

# Importing Components
from app.utils.create_df_from_user_input import create_empty_df_from_inputs

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

meta_data = dbc.Container([
    dcc.Tabs(id='metadata-tabs', value='batch-data-tab', children=[
        dcc.Tab(label='Batch', value="batch-data-tab", children=[
                html.Div(id="table-container-batch"),
        ]),
        dcc.Tab(label="Species", value = "species-data-tab", children=[
            html.Div(id = "table-container-species")
        ]),
       dcc.Tab(label="Strains", value = "strains-data-tab", children=[
            html.Div(id = "table-container-strains")
        ]),
        dcc.Tab(label="Stages", value = "stages-data-tab", children=[
            html.Div(id = "table-container-stages")
        ]),
        dcc.Tab(label="Treatments", value = "treatment-data-tab", children=[
            html.Div(id = "table-container-treatments")
        ]),
        dcc.Tab(label="Concentrations", value = "concentration-data-tab", children=[
            html.Div(id = "table-container-conc")
        ]),
        dcc.Tab(label="Other", value = "other-data-tab", children=[
            html.Div(id = "table-container-other")
        ]),
    ]),
],
    style={"paddingTop": "80px"}) # adjust white space between metadata tab and tabs of metadata content


########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################
def update_metadata_tables(app):
     # Create a callback to update the table based on user inputs
    @app.callback(
        [Output("table-container-batch", "children"),
        Output("table-container-species", "children"),
        Output("table-container-strains", "children"),
        Output("table-container-stages", "children"),
        Output("table-container-treatments", "children"),
        Output("table-container-conc", "children"),
        Output("table-container-other", "children")
        ],
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

        df_empty = create_empty_df_from_inputs(rows, cols)
        table_batch = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df_empty.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-batch'
        )
        table_species = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df_empty.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-species'
        )
        table_stages = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df_empty.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-stages'
        )
        table_strains = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df_empty.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-strains'
        )
        table_treatment = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df_empty.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-species'
        )
        table_conc = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df_empty.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-conc'
        )
        table_other = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df_empty.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-other'
        )
        return table_batch, table_species, table_strains, table_stages, table_treatment, table_conc, table_other