########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import base64
import os
import pathlib
import itertools
from collections import OrderedDict

import cv2
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import yaml
from dash import callback_context, dash_table, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from PIL import Image

# Importing Components
from app.components.selection_table import selection_table
from app.components.instrument_settings import instrument_settings
from app.components.header import header
from app.components.worm_information import worm_information
from app.components.module_selection import module_selection
from app.components.run_time_settings import run_time_settings
from app.components.save_page_content import save_page
from app.components.info_page_content import info_page
from app.components.preview_page_content import preview_page
from app.components.configure_analysis import configure_analysis
from app.components.meta_data_ import meta_data
from app.components.tabs_content import tabs_content
from app.components.create_df_from_user_input import create_df_from_inputs
from app.components.callbacks import get_callbacks

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SPACELAB], 
                suppress_callback_exceptions=True)


########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

app.layout = html.Div([header, 
                       # Adding vertical space so tabs content not hidden behind navbar
                       html.H4("",style={'padding-top': 80, 'display': 'inline-block'}),
                       tabs_content, 
                       # Modals (popup screens)
                        save_page,
                        info_page,
                        preview_page,
                       ])

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################
get_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9000)