########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import callback, html, dcc
from dash.dependencies import Input, Output

from app.utils.callback_functions import zenodo_get_id

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

fetch_data_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Please select the data to fetch:")),
        dbc.ModalBody(
            [
                dbc.Row(
                    [
                        # Display an alert message above the checklist with the Zenodo link
                        dbc.Alert(
                            [
                                "Please select your plates below or visit the ",
                                html.A(
                                    "Zenodo link",
                                    href="https://zenodo.org/records/12760651",
                                    target="_blank",  # Opens the link in a new tab
                                    style={
                                        "color": "#007bff"
                                    },  # Customize the link color
                                ),
                                " for more information.",
                            ],
                            color="light",  # You can change the color to 'warning', 'danger', 'success', etc.
                            dismissable=True,  # Allow the alert to be dismissed
                        ),
                        dbc.Checklist(
                            options=[
                                {
                                    "label": html.Span(
                                        [
                                            "Motility (96-well plate, individual wells) - ",
                                            html.I("Brugia malayi "),
                                            "microfilaria",
                                        ]
                                    ),
                                    "value": "20210819-p01-NJW_753",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Motility (96-well plate, whole plate) - ",
                                            html.I("Brugia pahangi "),
                                            "adults",
                                        ]
                                    ),
                                    "value": "20220622-p02-KTR",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Motility (24-well plate, whole plate) - ",
                                            html.I("Brugia pahangi "),
                                            "adults",
                                        ]
                                    ),
                                    "value": "20220527-p02-KTR",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Feeding - ",
                                            html.I("Caenorhabditis elegans "),
                                            "adults",
                                        ]
                                    ),
                                    "value": "20210823-p01-KJG_795",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Worm size - ",
                                            html.I("Caenorhabditis elegans "),
                                        ]
                                    ),
                                    "value": "20220408-p01-MGC_1351",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Viability - ",
                                            html.I("Brugia malayi "),
                                            "microfilaria",
                                        ]
                                    ),
                                    "value": "20210917-p15-NJW_913",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Fecundity (with adults) - ",
                                            html.I("Schistosoma mansoni "),
                                        ]
                                    ),
                                    "value": "20220722-p04-JDC_1606",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Fecundity (without adults) - ",
                                            html.I("Schistosoma mansoni "),
                                        ]
                                    ),
                                    "value": "20220722-p06-JDC_1608",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Fecundity - ",
                                            html.I("Brugia pahangi "),
                                        ]
                                    ),
                                    "value": "20210906-p01-NJW_857",
                                },
                                {
                                    "label": html.Span(
                                        [
                                            "Tracking - ",
                                            html.I("Schistosoma mansoni "),
                                            "miracidia",
                                        ]
                                    ),
                                    "value": "20240307-p01-RVH",
                                },
                            ],
                            id="overwrite-checklist",
                            inline=False,
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [dbc.Col(dcc.Markdown("Data will be saved to `/home/downloads/`"))],
                ),
                dbc.Row(
                    [
                        dbc.Alert(
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                "Zenodo File Size (GB):",  # Text displaying the file size label
                                            ],
                                            width=3,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Input(
                                                    type="number",  # Text input
                                                    id="zenodo-file-size-input",  # Input ID
                                                    disabled=True,  # Make input field read-only
                                                ),
                                            ],
                                            width=4,
                                        ),
                                    ]
                                ),
                            ],
                            color="light",
                            dismissable=True,
                        ),
                    ]
                ),
            ]
        ),
        dbc.ModalFooter(
            [
                html.H6("Are you sure you want to fetch the example data?"),
                dbc.Button(
                    "Yes", id="confirm-fetch", color="success", className="me-2"
                ),
                dbc.Button("No", id="cancel-fetch", color="danger", className="me-2"),
            ]
        ),
    ],
    id="fetch-data-modal",
    is_open=False,  # Modal is initially closed
    size="lg",
)


@callback(
    Output("zenodo-file-size-input", "value"),
    Input("overwrite-checklist", "value"),
    prevent_initial_call=True,
)
def update_file_size_alert(value):
    file_size = {
        "20210819-p01-NJW_753": 5.8,
        "20210823-p01-KJG_795": 1.5,
        "20210906-p01-NJW_857": 1.9,
        "20210917-p15-NJW_913": 1.9,
        "20220408-p01-MGC_1351": 0.5338,
        "20220527-p02-KTR": 0.2661,
        "20220622-p02-KTR": 0.0382,
        "20220722-p04-JDC_1606": 0.1256,
        "20220722-p06-JDC_1608": 0.1461,
        "20240307-p01-RVH": 7.2,
    }

    if len(value) == 0:
        return 0
    else:
        for plate in value:
            if plate in file_size:
                total_size = sum([file_size[plate] for plate in value])
        
        return round(total_size, 2)


@callback(
    Output(
        "fetch-data-link", "children"
    ),  # Optionally update the link text or other outputs
    Input("confirm-fetch", "n_clicks"),  # Listen for Yes button click
    Input("overwrite-checklist", "value"),  # Listen for checklist value
    prevent_initial_call=True,
)
def fetch_data(confirm_click, value):
    if confirm_click:
        # Only download files that are selected
        try:
            result = zenodo_get_id(value)
            return result
                
        except Exception as e:
            return f"Error: {str(e)}"
    return "Fetch Example Data"
