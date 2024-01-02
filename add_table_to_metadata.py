########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import html

# Information symbol for tooltip
info_symbol = "data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwWiIgZGF0YS1uYW1lPSJQYXRoIDM2NzIiLz48cGF0aCBmaWxsPSIjNTI1ODYzIiBkPSJNNS4yMTEgMTguNzg3YTkuNiA5LjYgMCAxIDEgNi43ODggMi44MTQgOS42IDkuNiAwIDAgMS02Ljc4OC0yLjgxNFptMS4yNzQtMTIuM0E3LjgwNiA3LjgwNiAwIDEgMCAxMiA0LjIwNmE3LjgwOCA3LjgwOCAwIDAgMC01LjUxNSAyLjI3OFptNC4xNjMgOS44Nzl2LTQuOGExLjM1MiAxLjM1MiAwIDAgMSAyLjcgMHY0LjhhMS4zNTIgMS4zNTIgMCAwIDEtMi43IDBabS4wMTctOC43QTEuMzM1IDEuMzM1IDAgMSAxIDEyIDkuMDMzYTEuMzUgMS4zNSAwIDAgMS0xLjMzNS0xLjM2OVoiIGRhdGEtbmFtZT0iUGF0aCAyNjgzIi8+PC9zdmc+"

# Importing Components
from app.components.metadata_tab import meta_data, update_metadata_tables 
from app.components.metadata_table_checklist import metadata_checklist, add_metadata_table_checklist
from app.components.create_metadata_tabs_from_checklist import meta_data_from_input, create_metadata_tables_from_checklist

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SPACELAB], 
                suppress_callback_exceptions=True)

########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

app.layout = html.Div([
                html.Br(),
                        dbc.Row(
                            [
                                # Label for Plate Format
                                dbc.Col(html.H6("Plate Format:")),
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
                                            id="tot-num-cols-and-rows-symbol"
                                        ),
                                        dbc.Tooltip(
                                            "Input the total number of rows and columns in the plate.",
                                            placement="bottom",
                                            target="tot-num-cols-and-rows-symbol"
                                        )
                                    ],
                                    width="auto"
                                ),
                                # Second Column: Input for Total Number of Columns
                                dbc.Col(
                                    dbc.Input(
                                        id="total-well-cols",
                                        placeholder="Number of columns.",
                                        type="number"
                                    ),
                                    width="auto"
                                ),
                                # Third Column: Input for Total Number of Rows
                                dbc.Col(
                                    dbc.Input(
                                        id="total-num-rows",
                                        placeholder="Number of rows.",
                                        type="number"
                                    ),
                                    width="auto",
                                    id="plate-foramt-options-row"
                                )
                            ],
                            align="center"
                        ),
                        html.Br(),
                        dbc.Row(
                            metadata_checklist
                        ),
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
                            align = 'center'
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
                        ),
                        html.Br(),
                        meta_data_from_input
                       
                       ])

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################

update_metadata_tables(app)
add_metadata_table_checklist(app)
create_metadata_tables_from_checklist(app)

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9000)