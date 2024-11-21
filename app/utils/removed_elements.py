########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
element_removed = dbc.Row(
    [
        dbc.Row(
            [
                # Label for Multi Site Imaging Mode
                dbc.Col(html.H6("Multi-site imaging:")),
            ],
            align="center",
        ),
        dbc.Row(
            [
                # First Column: Image, Tooltip
                dbc.Col(
                    [
                        html.I(
                            className="fa-solid fa-circle-info",  # Information Symbol
                            id="multi-site-imaging-mode-info-symbol",
                        ),
                        dbc.Tooltip(
                            # Tooltip element for information symbol, displays message when cursor over the symbol
                            "Use if each well had multiple sites imaged. Enter the number of x and y sites per well. If none provided, defaults to 1.",
                            placement="bottom",
                            target="multi-site-imaging-mode-info-symbol",
                        ),
                    ],
                    width="auto",
                ),
                # Second Column: Input for Total Number of Columns
                dbc.Col(
                    dbc.Input(
                        id="multi-site-well-cols",
                        placeholder="X-sites = 1",
                        type="number",
                        persistence=True,
                        persistence_type="memory",
                    ),
                    width="auto",
                ),
                # Third Column: Input for Total Number of Rows
                dbc.Col(
                    dbc.Input(
                        id="multi-site-num-rows",
                        placeholder="Y-sites = 1",
                        type="number",
                        persistence=True,
                        persistence_type="memory",
                    ),
                    width="auto",
                    id="multi-site-format-options-row",
                ),
            ],
            align="center",
        ),
        ### IMG MASKING ###
        html.Div(
            dbc.Row(
                [
                    # Label for Circle or Square image Masking
                    html.H6("Image masking:"),  # Title for Image Masking
                    dbc.Col(
                        [
                            html.I(
                                className="fa-solid fa-circle-info",  # Information Symbol
                                id="circ-or-square-img-mask",
                            ),
                            dbc.Tooltip(
                                # Tooltip element for information symbol, displays message when cursor over the symbol
                                "Select the shape of mask to be applied.",
                                placement="bottom",  # Placement of tooltip
                                target="circ-or-square-img-mask",  # Target of tooltip
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
                                persistence_type="memory",  # Persistence type of radio button
                            ),
                        ],
                        width="auto",
                    ),
                ],
                align="center",
            )
        ),
    ]
)


########################################################################
####                                                                ####
####                         From run.py                            ####
####                                                                ####
########################################################################


@callback(
    Output("img-mode-output", "children"),
    Output("file-structure-output", "children"),
    Output("plate-format-output", "children"),
    Output("img-masking-output", "children"),
    Output("mod-selection-output", "children"),
    Output("volume-name-output", "children"),
    Output("plate-name-output", "children"),
    Output("wells-content-output", "children"),
    Input("submit-analysis", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def update_results_message_for_run_page(nclicks, store):
    """
    This function updates the results message for the run page.
    =========================================================================================
    Arguments:
        - nclicks : int : The number of clicks
        - store : dict : The store data
    =========================================================================================
    Returns:
        - results : list : The results
    """
    # check to see if store exists
    if not store:
        return None, None, None, None, None, None, None, None

    # checking to see if the rows and cols are None
    if store["rows"] == None:
        rows = 8
    if store["cols"] == None:
        cols = 12

    # get the store from the data and create the results
    img_mode = f'Imaging Mode: {store["img_mode"]}'
    file_structure = f'File Structure: {store["file_structure"]}'
    plate_format = f"Plate Format: Rows = {rows}, Cols = {cols}"
    img_masking = f'Image Masking: {store["img_masking"]}'
    mod_selection = f'Module Selection: {store["pipeline_selection"]}'
    volume = f'Volume: {store["mount"]}'
    platename = f'Platename: {store["platename"]}'
    wells = f'Wells: {store["wells"]}'

    # create a list of the results
    results = [
        img_mode,
        file_structure,
        plate_format,
        img_masking,
        mod_selection,
        volume,
        platename,
        wells,
    ]
    if nclicks:  # check to see if the button has been clicked
        return results  # return the results
