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
        dbc.Alert(id='resolving-error-issue-configure', color='success'),
    ]
)

error_content_preview = dbc.ModalBody(
    [
        dbc.Alert(id='resolving-error-issue-preview', color='success'),
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
        dbc.ModalFooter(
            dbc.Button("close", id = 'close-error-modal-button-configure', color = 'success')
        )
    ],
    id='error-modal-configure',
    is_open=False
)

error_modal_preview = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle('ERROR')),
        error_content_preview,
        dbc.ModalFooter(
            dbc.Button("close", id = 'close-error-modal-button-preview', color = 'success')
        )
    ],
    id='error-modal-preview',
    is_open=False
)