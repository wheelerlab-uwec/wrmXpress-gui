########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
save_page_content = dbc.ModalBody(
    [
        # Content for the Save Page Modal
        dcc.Markdown("Write a YAML for running wrmXpress remotely. Include a full path and file name ending in `.yaml`."),
        dbc.Input(id="file-path-for-saved-yaml-file",
                  placeholder="Enter the full save path...", type="text"),
    ]
)

########################################################################
####                                                                ####
####                             Modal                              ####
####                                                                ####
########################################################################
save_page = dbc.Modal(
    [
        dbc.ModalHeader("Save Page"),
        save_page_content,
        dbc.ModalFooter([
            # Buttons for the Save Page Modal
            dbc.Button("Save", id="save-page-button", className="ml-auto"),
            dbc.Button("Close", id="close-save-modal", className="ml-auto"),
        ]),
        html.Div(id="save-page-status")  # Placeholder for saving status
    ],
    id="save-page-modal",
    size="l"
)