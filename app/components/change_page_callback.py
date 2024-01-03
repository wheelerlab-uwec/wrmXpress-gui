########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
from dash.dependencies import Input, Output, State

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################
def get_callbacks(app):

    # Open and Close Info, Preview, and Save modals
    @app.callback(
        [Output("save-page-modal", "is_open"),
        Output("info-page-modal", "is_open"),
        Output("preview-page-modal", "is_open")],
        [Input("open-save-modal", "n_clicks"), Input("close-save-modal", "n_clicks"),
        Input("open-info-modal", "n_clicks"), Input("close-info-modal", "n_clicks"),
        Input("open-preview-modal", "n_clicks"), Input("close-preview-modal", "n_clicks")],
        [State("save-page-modal", "is_open"),
        State("info-page-modal", "is_open"),
        State("preview-page-modal", "is_open")],
    )
    def toggle_modals(open_save_clicks, close_save_clicks, open_info_clicks, close_info_clicks,
                    open_preview_clicks, close_preview_clicks, is_save_open, is_info_open, is_preview_open):
        ctx = dash.callback_context

        if ctx.triggered_id in ["open-save-modal", "close-save-modal"]:
            return not is_save_open, False, False
        elif ctx.triggered_id in ["open-info-modal", "close-info-modal"]:
            return False, not is_info_open, False
        elif ctx.triggered_id in ["open-preview-modal", "close-preview-modal"]:
            return False, False, not is_preview_open
        else:
            return is_save_open, is_info_open, is_preview_open
        