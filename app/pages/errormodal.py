########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import yaml
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
from app.utils.callback_functions import prep_yaml
import os
import plotly.graph_objs as go

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

error_content = dbc.ModalBody(
    id='error-modal-content'
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
        dbc.ModalFooter(
            dbc.Button(
                "Close", id='close-error-modal', className='ms-auto', color='success', n_clicks=0
            )
        )
    ],
    id='error-modal',
    is_open=False
)
