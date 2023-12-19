########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

info_symbol = "data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZmlsbD0ibm9uZSIgZD0iTTAgMGgyNHYyNEgwWiIgZGF0YS1uYW1lPSJQYXRoIDM2NzIiLz48cGF0aCBmaWxsPSIjNTI1ODYzIiBkPSJNNS4yMTEgMTguNzg3YTkuNiA5LjYgMCAxIDEgNi43ODggMi44MTQgOS42IDkuNiAwIDAgMS02Ljc4OC0yLjgxNFptMS4yNzQtMTIuM0E3LjgwNiA3LjgwNiAwIDEgMCAxMiA0LjIwNmE3LjgwOCA3LjgwOCAwIDAgMC01LjUxNSAyLjI3OFptNC4xNjMgOS44Nzl2LTQuOGExLjM1MiAxLjM1MiAwIDAgMSAyLjcgMHY0LjhhMS4zNTIgMS4zNTIgMCAwIDEtMi43IDBabS4wMTctOC43QTEuMzM1IDEuMzM1IDAgMSAxIDEyIDkuMDMzYTEuMzUgMS4zNSAwIDAgMS0xLjMzNS0xLjM2OVoiIGRhdGEtbmFtZT0iUGF0aCAyNjgzIi8+PC9zdmc+"

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
instrument_settings = dbc.AccordionItem([
    html.Div([
        dbc.Row([
                html.H6("Imaging Mode:", id='imaging-mode-header'),
                dbc.Col([
                    html.Img(src=info_symbol,
                             id='imaging-mode-symbol'),
                    dbc.Tooltip(
                        "Select Single Well if each video or image only includes a single well. Select Multi Well if each video/image contains multiple wells that need to be split.",
                        placement='bottom',
                        target="imaging-mode-symbol"
                    ),
                    dbc.RadioItems(
                        id="imaging-mode",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Single Well", "value": "single-well"},
                            {"label": "Multi Well", "value": "multi-well"},
                        ],
                        value="single-well",
                    )
                ],
                    width="auto"),
                dbc.Col([
                    html.Div("Settings for multiple wells per image:"),
                    dbc.Input(id="multi-well-rows",
                        placeholder="Number of rows per image.",
                        type="number"),
                    dbc.Input(id="multi-well-cols",
                        placeholder="Number of columns per image.",
                        type="number"),
                ],
                    width='auto',
                    id='multi-well-options-row',
                    style={'display': 'flex'}  # Initially hidden
                )
                ],
                align="center")
    ]),
    html.Br(),
    html.Div(
        dbc.Row([
                html.H6("File Structure:"),
                dbc.Col([
                    html.Img(src=info_symbol,
                             id='file-structure-symbol'),
                    dbc.Tooltip(
                        "Select ImageXpress if the data is saved in an IX-like structure. Select AVI if the data is a single video saved as an AVI.",
                        placement='bottom',
                        target="file-structure-symbol"
                    ),
                    dbc.RadioItems(
                        id="file-structure",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "ImageXpress", "value": "imagexpress"},
                            {"label": "AVI", "value": "avi"},
                        ],
                        value="imagexpress",
                    )
                ],
                    width='auto'),
                dbc.Col([
                    html.Div(html.P("Cropping options:",
                             style={"textDecoration": "underline",
                                    "cursor": "pointer"},
                             id='crop-options')),
                    dbc.Tooltip(
                        "Select the method of cropping wells. \
                            Auto: incorporates a Hough transform in an attempt to automatically identify circular wells.\
                            Grid: Crops a grid based on the provided number of columns and rows.",
                        placement='bottom',
                        target="crop-options"
                    ),
                    dbc.RadioItems(
                        id="multi-well-detection",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Auto", "value": "auto"},
                            {"label": "Grid", "value": "grid"},
                        ],
                        value="auto",
                    ),
                ],
                    width='auto',
                    id='additional-options-row',
                    style={'display': 'flex'})  # Initially hidden
                ],
                align="center")
    ),
],
    id="instrument-settings-file-structure",
    title="Instrument Settings"
)