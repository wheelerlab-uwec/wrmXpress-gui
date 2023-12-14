import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html
from dash.dependencies import Input, Output, State
# import dash_ag_grid as dag

# Create row names
rows = list('ABCDEFGH')

# Create column names
columns = [str(num).zfill(2) for num in range(1, 13)]

# Step 3: Create cell values
data = [[row + col for col in columns] for row in rows]

# Step 4: Create DataFrame
df = pd.DataFrame(data, columns=columns, index=rows)

selection_table = html.Div(
    dash_table.DataTable(
        data=df.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col, "selectable": True} for col in df.columns],
        editable=True,
        # column_selectable="multi",
        # row_selectable="multi",
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_cell_conditional=[{'if': {'column_id': 'index'},
                                 'width': '40px'}],
        id='well-selection-table'
    )
)

# selection_table_ag = html.Div([
#     dbc.Button('Select all wells',
#                color='primary',
#                className='me-1 mb-4',
#                id='row-selection-button'),
#     html.Br(),
#     dag.AgGrid(
#         columnDefs=[{"field": col} for col in df.columns],
#         rowData=df.to_dict("records"),
#         columnSize='sizeToFit',
#         dashGridOptions={
#             "rowSelection": "multiple",
#             "rowMultiSelectWithClick": True
#         },
#         id='well-selection-table'
#     )]
# )