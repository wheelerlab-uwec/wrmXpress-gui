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

image_transformations = dbc.AccordionItem(
    [
        html.Div(
            dbc.Row(
                [
                    html.H6("Mask:"),  # Title for File Structure
                    dbc.Col(
                        [
                            html.I(
                                className="fa-solid fa-circle-info",  # Information symbol
                                id="mask-symbol",
                            ),
                            dbc.Tooltip(
                                # Tooltip element for information symbol, displays message when cursor over the symbol
                                html.P(
                                    "Implement a circular or square mask. If no masking is needed, choose NA.",
                                    style={"text-align": "left"},
                                ),
                                placement="bottom",
                                target="mask-symbol",
                                style={"text-align": "left"},
                            )
                        ],
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Select(
                                id="mask",
                                options=[
                                    {"label": "Circular", "value": "circular"},
                                    {"label": "Square", "value": "square"},
                                    {"label": "NA", "value": "NA"},
                                ],
                                value="NA",
                                persistence=True,
                                persistence_type="memory",
                            ),
                        ],
                        width="auto"
                    ),
                    dbc.Col(
                        [
                            html.H6("Diameter (portion of image height)"),
                            dbc.Input(
                                id="mask-diameter", 
                                placeholder="0",
                                type="number",
                                min=0,
                                max=1,
                                # step=0.1,
                                persistence=True,
                                persistence_type="memory",
                            ),
                        ],
                        width="auto",
                        id="mask-options-row",
                        style={
                            "display": "flex",
                        },
                    ),
                ],
                align="center",
            )
        )
    ],
    id="image-transformations",
    title="Image Transformations",  # Title of accordian item
)
