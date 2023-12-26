########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html

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
