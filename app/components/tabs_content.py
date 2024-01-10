########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc

from app.pages.configure_analysis import configure_analysis
from app.pages.metadata_tab import meta_data
########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################
# Tabs Content
tabs_content = dbc.Container(
    [
        dcc.Tabs(id="tabs", value='video_analysis-tab', children=[
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
