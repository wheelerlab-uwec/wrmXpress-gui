import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html
from dash.dependencies import Input, Output, State
# import dash_ag_grid as dag

"""
I am not sure what elements we want in the table of the metadata, I am leaving this as the example shown in
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/table/
for now 
"""

# Example DataFrame
rows = list("ABCDEFGH")
columns = [str(num).zfill(2) for num in range(1, 13)]
data = [[row + col for col in columns] for row in rows]
df = pd.DataFrame(data, columns=columns, index=rows)

# Create a dbc.Table from the DataFrame
table = dbc.Table.from_dataframe(
    df, striped=True, bordered=True, hover=True, index=True
)