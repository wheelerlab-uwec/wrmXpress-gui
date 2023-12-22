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


########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################
configure_analysis = dbc.Container([
            dbc.Accordion(
                [
                    # Order of the Accordian item in which they appear in the app
                    instrument_settings,
                    worm_information,
                    module_selection,
                    run_time_settings,
                ],
                start_collapsed=False,
                always_open=True,
            ),
        ],
        style={"paddingTop":"150px"})