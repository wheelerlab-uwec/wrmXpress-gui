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
element_removed = dbc.Row([
dbc.Row(
        [
            
            # Label for Multi Site Imaging Mode
            dbc.Col(
                html.H6(
                    "Multi-site imaging:"
                )
            ),
            
        ],
        align="center"
    ),
    dbc.Row(
        [ 
            # First Column: Image, Tooltip
            dbc.Col(
                [
                    html.I(
                        className="fa-solid fa-circle-info",  # Information Symbol
                        id="multi-site-imaging-mode-info-symbol"
                    ),

                    dbc.Tooltip(
                        # Tooltip element for information symbol, displays message when cursor over the symbol
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
    ### IMG MASKING ###
    html.Div(
        
        dbc.Row([
                # Label for Circle or Square image Masking
                html.H6(
                    "Image masking:"  # Title for Image Masking
                ),
                dbc.Col([
                    html.I(
                        className="fa-solid fa-circle-info",  # Information Symbol
                        id="circ-or-square-img-mask"
                    ),
                    dbc.Tooltip(
                        # Tooltip element for information symbol, displays message when cursor over the symbol
                        "Select the shape of mask to be applied.",
                        placement="bottom",  # Placement of tooltip
                        target="circ-or-square-img-mask"  # Target of tooltip
                    ),
                    dbc.RadioItems(
                        id="circ-or-square-img-masking",  # Radio button selection for circle or square
                        className="btn-group",  # Class name for button group
                        inputClassName="btn-check",  # Class name for button check
                        # Class name for button outline primary
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",  # Class name for active label
                        options=[
                            {"label": "Circle", "value": "circle"},
                            {"label": "Square", "value": "square"},
                        ],
                        value="circle",  # Initial value of radio button
                        persistence=True,  # Persistence of radio button
                        persistence_type='memory'  # Persistence type of radio button
                    ),
                ],
                    width='auto'
                ),

                ],
                align="center"
                )
    )
])

    