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
                dbc.Button("Metadata Selection",
                           id="metadata-tab-selection-offcanvas", n_clicks=0),
                dbc.Offcanvas(
                    [
                        metadata_checklist,
                        html.Br(),
                        dbc.Row(
                            [
                                # Label for Plate Format
                                dbc.Col(html.H6("Add New Metadata Table:")),
                            ],
                            align="center"
                        ),
                        dbc.Row(
                            [
                                # First Column: Image, Tooltip
                                dbc.Col(
                                    [
                                        html.Img(
                                            src=info_symbol,
                                            id="add-new-metadata-table-info-symbol"
                                        ),
                                        dbc.Tooltip(
                                            "Please click here which will open a modal that you can insert the name of the new metadata table which you wish to create.",
                                            placement="bottom",
                                            target="add-new-metadata-table-info-symbol"
                                        )
                                    ],
                                    width="auto"
                                ),
                                # Second Column: Input for Total Number of Columns
                                dbc.Col(
                                    dbc.Button(
                                        "Add Metadata Table",
                                        id="add-metadata-table-button",
                                        className="me-2",
                                    ),
                                    width="auto"
                                ),
                                dbc.Col(
                                    # Add an uneditable input box here
                                    dbc.Input(
                                        id="uneditable-input-box",
                                        value="",
                                        disabled=False
                                    ),
                                    width="auto"
                                ),
                            ],
                            align="center"
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(html.H6("Finalize Metadata Tables:")),
                            ],
                            align='center'
                        ),
                        dbc.Row(
                            [
                                # First Column: Image, Tooltip
                                dbc.Col(
                                    [
                                        html.Img(
                                            src=info_symbol,
                                            id="finalize-metadata-table-info-symbol"
                                        ),
                                        dbc.Tooltip(
                                            "Please click here which will open a modal that you can insert the name of the new metadata table which you wish to create.",
                                            placement="bottom",
                                            target="finalize-metadata-table-info-symbol"
                                        )
                                    ],
                                    width="auto"
                                ),
                                # Second Column: Input for Total Number of Columns
                                dbc.Col(
                                    dbc.Button(
                                        "Finalize Metadata Tables",
                                        id="finalize-metadata-table-button",
                                        className="me-2",
                                    ),
                                    width="auto"
                                ),
                            ],
                            align="center"
                        )
                    ],
                    id="offcanvas",
                    title="Select Metadata Tables",
                    is_open=True,
                ),
                html.Br(),
                html.Br(),
                meta_data_from_input,
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


def add_metadata_table_checklist(app):
    @app.callback(
        Output("checklist-input", "options"),
        [Input("add-metadata-table-button", "n_clicks")],
        [State("uneditable-input-box", 'value'),
         State("checklist-input", "options")]
    )
    def update_metadata_checklist(n_clicks, new_table_name, existing_options):
        if n_clicks and new_table_name:
            # Append the new table name to the existing options
            new_option = {"label": new_table_name, "value": new_table_name}
            updated_options = existing_options + [new_option]
            return updated_options
        else:
            return existing_options
