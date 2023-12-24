########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc

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
