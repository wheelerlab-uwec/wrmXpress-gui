########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import time

########################################################################
####                                                                ####
####                              Content                           ####
####                                                                ####
########################################################################

error_content_configure = dbc.ModalBody(
    [
        dbc.Alert(id='resolving-error-issue-configure', color='success', duration = 6000),
    ]
)

error_content_preview = dbc.ModalBody(
    [
        dbc.Alert(id='resolving-error-issue-preview', color='success', duration=6000),
    ]
)

########################################################################
####                                                                ####
####                              Modal                             ####
####                                                                ####
########################################################################

error_modal_configure = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle('ERROR')),
        error_content_configure,
    ],
    id='error-modal-configure',
    is_open=False
)

error_modal_preview = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle('ERROR')),
        error_content_preview,
    ],
    id='error-modal-preview',
    is_open=False
)