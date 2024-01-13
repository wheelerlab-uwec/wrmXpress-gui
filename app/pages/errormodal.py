########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

error_content = dbc.ModalBody(
    [
        dbc.Alert(id='error-modal-content', color='danger'),
        dbc.Alert(id='resolving-error-issue', color='success'),
    ]
)


########################################################################
####                                                                ####
####                              Modal                             ####
####                                                                ####
########################################################################

error_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle('ERROR')),
        error_content,
    ],
    id='error-modal',
    is_open=False
)
