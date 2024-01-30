########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import docker
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
import os
import subprocess
import yaml
from dash.long_callback import DiskcacheLongCallbackManager
import pandas as pd

from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header

# importing utils
from app.utils.styling import layout

# Diskcache
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = Dash(__name__,
           long_callback_manager=long_callback_manager,
           use_pages=True,
           pages_folder='app/pages',
           external_stylesheets=[
               dbc.themes.FLATLY,
               dbc.icons.FONT_AWESOME],
           suppress_callback_exceptions=True)

########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

sidebar = html.Div(
    [
        html.A(
            html.Img(src='https://github.com/zamanianlab/wrmXpress/blob/main/img/logo/output.png?raw=true',  # wrmXpress image
                     height="200px"),
            # clicked takes user to wrmXpress github
            href="https://github.com/zamanianlab/wrmxpress",
            style={"textDecoration": "none"},
            className='ms-3'
        ),
        html.Hr(),
        html.Div([
            dbc.Nav(
                children=dbc.NavLink(f"{page['name']}",
                                     href=page["relative_path"],
                                     active='exact'
                                     ),
                pills=True,
                vertical=True
            ) for page in dash.page_registry.values()
        ])
    ],
    style=SIDEBAR_STYLE
)


app.layout = html.Div([
    dcc.Store(id='store', data={}),
    sidebar,
    html.Div(id="page-content",
             children=[header, dash.page_container],
             style=CONTENT_STYLE)])

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@app.long_callback(
    output=Output("image-analysis-preview", "children"),
    inputs=Input("submit-analysis", "n_clicks"),
    running=[
        (
            Output("submit-analysis", "disabled"), True, False
        ),
        (
            Output("cancel-analysis", "disabled"), False, True
        ),
        (
            Output("image-analysis-preview", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible"}
        ),
        (
            Output("progress-bar-run-page", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"}
        ),
    ],

    cancel=[Input("cancel-analysis", "n_clicks")],
    progress=[
        Output("progress-bar-run-page", "value"),
        Output("progress-bar-run-page", "max")
    ],
)
def callback(set_progress, n_clicks):
    if n_clicks:
        df = pd.read_csv("NYC_Pool_Inspections_20240124.csv")
        for i in range(df.shape[0]):
            text = str(df.iloc[i])
            time.sleep(0.1)
            set_progress((str(i + 1), str(df.shape[0]), text))
        return [f"Clicked {n_clicks} times"]

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)
