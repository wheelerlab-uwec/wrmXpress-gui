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
from app.components.metadata_table_checklist import metadata_checklist
from app.components.create_metadata_tabs_from_checklist import meta_data_from_input

info_symbol = "data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwWiIgZGF0YS1uYW1lPSJQYXRoIDM2NzIiLz48cGF0aCBmaWxsPSIjNTI1ODYzIiBkPSJNNS4yMTEgMTguNzg3YTkuNiA5LjYgMCAxIDEgNi43ODggMi44MTQgOS42IDkuNiAwIDAgMS02Ljc4OC0yLjgxNFptMS4yNzQtMTIuM0E3LjgwNiA3LjgwNiAwIDEgMCAxMiA0LjIwNmE3LjgwOCA3LjgwOCAwIDAgMC01LjUxNSAyLjI3OFptNC4xNjMgOS44Nzl2LTQuOGExLjM1MiAxLjM1MiAwIDAgMSAyLjcgMHY0LjhhMS4zNTIgMS4zNTIgMCAwIDEtMi43IDBabS4wMTctOC43QTEuMzM1IDEuMzM1IDAgMSAxIDEyIDkuMDMzYTEuMzUgMS4zNSAwIDAgMS0xLjMzNS0xLjM2OVoiIGRhdGEtbmFtZT0iUGF0aCAyNjgzIi8+PC9zdmc+"

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

meta_data = dbc.Container(
    [
        html.Div(
            [
                dbc.Button("Table selection",
                           id="metadata-tab-selection-offcanvas", n_clicks=0),
                dbc.Offcanvas(
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
                                # First Column: Input for Total Number of Columns
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
                        )
                    ],
                    id="offcanvas",
                    title="Select metadata tables:",
                    is_open=True,
                ),
                html.Br(),
                html.Br(),
                meta_data_from_input,
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


########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################
def open_metadata_offcanvas(app):
    @app.callback(
        Output("offcanvas", "is_open"),
        Input("metadata-tab-selection-offcanvas", "n_clicks"),
        [State("offcanvas", "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open
