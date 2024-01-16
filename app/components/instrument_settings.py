########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

instrument_settings = dbc.AccordionItem([
    html.Div([
        dbc.Row([
                # Title for Imaging mode
                html.H6("Imaging mode:", id='imaging-mode-header'),
                dbc.Col([
                    html.I(className="fa-solid fa-circle-info",  # Information Symbol
                           id='imaging-mode-symbol'),
                    dbc.Tooltip(
                        # Tooltip element for information symbol, displays message when cursor over the symbol
                        "Select Single Well if each video or image only includes a single well. Select Multi Well if each video/image contains multiple wells that need to be split.",
                        placement='bottom',
                        target="imaging-mode-symbol"
                    ),
                    dbc.RadioItems(  # Radio button selection for single well or multi well
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
                        persistence=True,
                        persistence_type='memory'
                    )
                ],
                    width="auto"),
                dbc.Col([
                    dbc.Input(id="multi-well-rows",  # Input values for rows per image
                        placeholder="Rows per image",
                        type="number",
                        persistence=True,
                        persistence_type='memory'),
                    dbc.Input(id="multi-well-cols",  # Input values for columns per image
                        placeholder="Columns per image",
                        type="number",
                        persistence=True,
                        persistence_type='memory'),
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
                    html.I(className="fa-solid fa-circle-info",  # Information Symbol
                           id="multi-site-imaging-mode-info-symbol"
                           ),

                    dbc.Tooltip(  # Tooltip element for information symbol, displays message when cursor over the symbol
                        "Use if each well had multiple sites imaged. Enter the number of x and y sites per well. If none provided, defaults to 1.",
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
                    placeholder="X-sites = 1",
                    type="number",
                    persistence=True,
                    persistence_type='memory'
                ),
                width="auto"
            ),
            # Third Column: Input for Total Number of Rows
            dbc.Col(
                dbc.Input(
                    id="multi-site-num-rows",
                    placeholder="Y-sites = 1",
                    type="number",
                    persistence=True,
                    persistence_type='memory'
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
                html.H6("File structure:"),  # Title for File Structure
                dbc.Col([
                    html.I(className="fa-solid fa-circle-info",  # Information symbol
                           id='file-structure-symbol'),
                    dbc.Tooltip(  # Tooltip element for information symbol, displays message when cursor over the symbol
                        "Select ImageXpress if the data is saved in an IX-like structure. Select AVI if the data is a single video saved as an AVI.",
                        placement='bottom',
                        target="file-structure-symbol"
                    ),
                    dbc.RadioItems(  # Radio selection items for ImageXpress or AVI
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
                        persistence=True,
                        persistence_type='memory'
                    )
                ],
                    width='auto'),
                dbc.Col([
                    html.Div(html.P("Cropping options:",  # text of cropping items
                             style={"textDecoration": "underline",
                                    "cursor": "pointer"},
                             id='crop-options')),
                    dbc.Tooltip(  # Tooltip element for text "cropping items", displays message when cursor over the text
                        "Select the method of cropping wells. \
                            Auto: incorporates a Hough transform in an attempt to automatically identify circular wells.\
                            Grid: Crops a grid based on the provided number of columns and rows.",
                        placement='bottom',
                        target="crop-options"
                    ),
                    dbc.RadioItems(  # Radio button selection of Auto or Grid
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
                        persistence=True,
                        persistence_type='memory'
                    ),
                ],
                    width='auto',
                    id='additional-options-row',
                    style={'display': 'flex'})
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
                    html.I(className="fa-solid fa-circle-info",
                           id="tot-num-cols-and-rows-symbol"
                           ),
                    dbc.Tooltip(
                        "Input the total number of rows and columns in the plate. If none provided, defaults to 12 columns and 8 rows",
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
                    placeholder="Columns = 12",
                    type="number",
                    persistence=True,
                    persistence_type='memory'
                ),
                width="auto"
            ),
            # Third Column: Input for Total Number of Rows
            dbc.Col(
                dbc.Input(
                    id="total-num-rows",
                    placeholder="Rows = 8",
                    type="number",
                    persistence=True,
                    persistence_type='memory'
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
                    html.I(className="fa-solid fa-circle-info",
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
                        persistence=True,
                        persistence_type='memory'
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
    id="instrument-settings-file-structure",  # id of accordian item
    title="Instrument Settings"  # Title of accordian item
)
