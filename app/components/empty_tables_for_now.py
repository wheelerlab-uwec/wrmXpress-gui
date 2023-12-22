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
table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

table_body = [html.Tbody([row1, row2, row3, row4])]

table = dbc.Table(table_header + table_body,
                    bordered=True,
                    dark=True,
                    hover=True,
                    responsive=True,
                    striped=True,)
