########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import plotly.graph_objs as go

########################################################################
####                                                                ####
####                             Styling                            ####
####                                                                ####
########################################################################

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "text-color": "#00205B",  
    'color':'#000000',
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "text-color": "#00205B", 
    'color':'#000000',
}

layout = go.Layout(
    xaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        zeroline=False,
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        ticks='',
        zeroline=False,
        showticklabels=False
    )
)