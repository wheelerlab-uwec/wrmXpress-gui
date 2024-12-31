########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import callback
from dash.dependencies import Input, Output

from app.utils.callback_functions import zenodo_get_id

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

fetch_data_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Confirmation")),
        dbc.ModalBody("Are you sure you want to fetch the example data?"),
        dbc.ModalFooter(
            [
                dbc.Button(
                    "Yes", id="confirm-fetch", color="success", className="me-2"
                ),
                dbc.Button("No", id="cancel-fetch", color="danger", className="me-2"),
            ]
        ),
    ],
    id="fetch-data-modal",
    is_open=False,  # Modal is initially closed
)


@callback(
    Output(
        "fetch-data-link", "children"
    ),  # Optionally update the link text or other outputs
    Input("confirm-fetch", "n_clicks"),  # Listen for Yes button click
    prevent_initial_call=True,
)
def fetch_data(confirm_click):
    if confirm_click:
        # Perform the fetch operation
        try:
            result = zenodo_get_id()
            return result  # Optionally update the UI with the result
        except Exception as e:
            return f"Error: {str(e)}"
    return "Fetch Example Data"
