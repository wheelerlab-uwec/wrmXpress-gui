########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yaml
import os
import dash

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
save_page_content = dbc.ModalBody(
    [
        # Content for the Save Page Modal Body
        dcc.Markdown("Please input the name of the metadata table which you wish to add."),
        dbc.Input(id="name-of-new-metadata-table",
                  placeholder="Enter the name of the new metadata table", type="text"),
    ]
)

########################################################################
####                                                                ####
####                             Modal                              ####
####                                                                ####
########################################################################
add_metadata_table = dbc.Modal(
    [
        # Modal content header
        dbc.ModalHeader("Add New Metadata Table Page"),
        # Modal page content as defined above
        save_page_content,
        # Modal page footer
        dbc.ModalFooter([
            # Buttons for the Save Page Modal
            dbc.Button("Add", id="add-metadata-table-button-to-page", className="ml-auto"),
            dbc.Button("Close", id="close-metadata-table-add-modal", className="ml-auto"),
        ]),
        html.Div(id="add-metadata-table-page-status") 
    ],
    id="add-metadata-table-page-modal",
    size="s"
)

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################

def open_metadata_modal(app):
    # Callback to close the modal when the "Close" button is clicked
    # Callback to open and close the Add Metadata Table modal
    @app.callback(
        Output("add-metadata-table-page-modal", "is_open"),
        [Input("add-metadata-table-button", "n_clicks"), Input("close-metadata-table-add-modal", "n_clicks")],
        [State("add-metadata-table-page-modal", "is_open")],
    )
    def toggle_add_metadata_table_modal(open_clicks, close_clicks, is_open):
        ctx = dash.callback_context

        if ctx.triggered_id == "add-metadata-table-button":
            return True  # Set is_open to True to open the modal when the "Add Metadata Table" button is clicked
        elif ctx.triggered_id == "close-metadata-table-add-modal":
            return False  # Set is_open to False to close the modal when the "Close" button is clicked
        else:
            return is_open  # Return the current state if no relevant button was clicked
        
    # Callback to add a new tab to meta_data based on user input
    @app.callback(
        Output("metadata-tabs", "children"),
        [Input("add-metadata-table-button-to-page", "n_clicks")],
        [State("name-of-new-metadata-table", "value"),
        State("metadata-tabs", "children")]
    )
    def add_new_tab(n_clicks, new_tab_label, existing_tabs):
        if n_clicks and new_tab_label:
            # Create a new tab based on the user's input
            new_tab = dcc.Tab(
                label=new_tab_label,
                value=new_tab_label.lower() + "-data-tab",  # Use lowercase label for value
                children=[
                    html.Div(id=f"table-container-{new_tab_label.lower()}")
                ]
            )
            # Append the new tab to the existing tabs
            existing_tabs.append(new_tab)
        return existing_tabs
