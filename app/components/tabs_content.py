########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

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

from app.components.configure_analysis import configure_analysis
from app.components.meta_data_ import meta_data
########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################
# Tabs Content
tabs_content = dbc.Container(
    [
        dcc.Tabs(id="tabs", value='tab-modules', children=[
            dcc.Tab(label="Configure Analysis", value="video_analysis-tab", children=[
                configure_analysis
            ]),
            dcc.Tab(label="Metadata", value='metadata-tab', children=[
                meta_data
            ])
        ])
    ],
    className="mt-5"
)
