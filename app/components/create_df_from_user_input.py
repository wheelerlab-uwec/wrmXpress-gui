import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html
from dash.dependencies import Input, Output, State

# Define the create_df_from_inputs function
def create_df_from_inputs(_rows, _cols):
    rows_total = list("ABCDEFGHIJKLMNOP")
    rows = rows_total[:int(_rows)]
    columns = [str(num).zfill(2) for num in range(1, int(_cols) + 1)]
    data = [[row + col for col in columns] for row in rows]
    df = pd.DataFrame(data, columns=columns, index=rows)
    return df