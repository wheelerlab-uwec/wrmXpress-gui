########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
instrument_settings = dbc.AccordionItem([
    html.Div([
        dbc.Row([
                html.H6("Imaging mode:", id='imaging-mode-header'),
                dbc.Col([
                    html.I(className="fa-solid fa-info",
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
    dbc.Row(
        [
            # Label for Multi Site Imaging Mode
            dbc.Col(html.H6("Multi-site imaging:")),
        ],
        align="center"
    ),
    dbc.Row(
        [
            # First Column: Image, Tooltip
            dbc.Col(
                [
                    html.I(className="fa-solid fa-info",
                           id="multi-site-imaging-mode-info-symbol"
                           ),
                    dbc.Tooltip(
                        "Use if each well had multiple sites imaged. Enter the number of x and y sites per well",
                        placement="bottom",
                        target="multi-site-imaging-mode-info-symbol"
                    )
                ],
                width="auto"
            ),
            # Second Column: Input for Total Number of Columns
            dbc.Col(
                dbc.Input(
                    id="multi-site-well-cols",
                    placeholder="X-sites",
                    type="number"
                ),
                width="auto"
            ),
            # Third Column: Input for Total Number of Rows
            dbc.Col(
                dbc.Input(
                    id="multi-site-num-rows",
                    placeholder="Y-sites",
                    type="number"
                ),
                width="auto",
                id="multi-site-foramt-options-row"
            )
        ],
        align="center"
    ),
    html.Br(),
    html.Div(
        dbc.Row([
                html.H6("File structure:"),
                dbc.Col([
                    html.I(className="fa-solid fa-info",
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
    html.Br(),
    dbc.Row(
        [
            # Label for Plate Format
            dbc.Col(html.H6("Plate format:")),
        ],
        align="center"
    ),
    dbc.Row(
        [
            # First Column: Image, Tooltip
            dbc.Col(
                [
                    html.I(className="fa-solid fa-info",
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
    html.Div(
        dbc.Row([
                # Label for Circle or Square image Masking
                html.H6("Image masking:"),
                dbc.Col([
                    html.I(className="fa-solid fa-info",
                           id="circ-or-square-img-mask"),
                    dbc.Tooltip(
                        "Select the shape of mask to be applied.",
                        placement="bottom",
                        target="circ-or-square-img-mask"
                    ),
                    dbc.RadioItems(
                        id="circ-or-square-img-masking",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Circle", "value": "circle"},
                            {"label": "Square", "value": "square"},
                        ],
                        value="circle",
                    ),
                ],
                    width='auto'),
                dbc.Col([
                ],
                )
                ],
                align="center")
    )
],
    id="instrument-settings-file-structure",
    title="Instrument Settings"
)

########################################################################
####                                                                ####
####                              Callback                          ####
####                                                                ####
########################################################################


def hidden_multi_row_col_feature(app):
    # Appearing multi-well options
    @app.callback(
        [Output('multi-well-options-row', 'style'),
         Output('additional-options-row', 'style')],
        [Input('imaging-mode', 'value'),
         Input('file-structure', 'value')]
    )
    def update_options_visibility(imaging_mode, file_structure):
        multi_well_options_style = {'display': 'none'}
        additional_options_style = {'display': 'none'}

        if imaging_mode == 'multi-well':
            multi_well_options_style = {'display': 'flex'}

            if file_structure == 'avi':
                additional_options_style = {'display': 'flex'}

        return multi_well_options_style, additional_options_style
