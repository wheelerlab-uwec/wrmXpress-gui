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

from app.components.header import header
from app.components.save_page_content import save_page
from app.components.info_page_content import info_page
from app.components.preview_page_content import preview_page
from app.components.create_df_from_user_input import create_df_from_inputs 

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

meta_data = dbc.Container([
    dcc.Tabs(id='metadata-tabs', value='tab-modules', children=[
        dcc.Tab(label='Batch', value="batch-data-tab", children=[
                html.Div(id="table-container-batch"),
        ]),
        dcc.Tab(label="Species", value = "species-data-tab", children=[
            html.Div(id = "table-container-species")
        ]),
       dcc.Tab(label="Strains", value = "strains-data-tab", children=[
            html.Div(id = "table-container-strains")
        ]),
        dcc.Tab(label="Stages", value = "stages-data-tab", children=[
            html.Div(id = "table-container-stages")
        ]),
        dcc.Tab(label="Treatments", value = "treatment-data-tab", children=[
            html.Div(id = "table-container-treatments")
        ]),
        dcc.Tab(label="Concentrations", value = "concentration-data-tab", children=[
            html.Div(id = "table-container-conc")
        ]),
        dcc.Tab(label="Other", value = "other-data-tab", children=[
            html.Div(id = "table-container-other")
        ]),
    ]),
],
    style={"paddingTop": "150px"})
