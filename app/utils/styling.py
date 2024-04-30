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

# Sidebar style
SIDEBAR_STYLE = {
    "position": "fixed",  # Fixed position
    "top": 0,  # Top of the page
    "left": 0,  # Left of the page
    "bottom": 0,  # Bottom of the page
    "width": "16rem",  # Width of the sidebar
    "padding": "2rem 1rem",  # Padding of the sidebar
    "background-color": "#f8f9fa",  # Background color of the sidebar
    "text-color": "#00205B",  # Text color of the sidebar
    "color": "#000000",  # Color of the sidebar
}

# Content style
CONTENT_STYLE = {
    "margin-left": "18rem",  # Margin left of the content
    "margin-right": "2rem",  # Margin right of the content
    "padding": "2rem 1rem",  # Padding of the content
    "text-color": "#00205B",  # Text color of the content
    "color": "#000000",  # Color of the content
}

# Graph style
layout = go.Layout(
    xaxis=dict(
        autorange=True,
        showgrid=False,
        ticks="",
        zeroline=False,
        showticklabels=False,
    ),
    yaxis=dict(
        autorange=True, showgrid=False, ticks="", zeroline=False, showticklabels=False
    ),
    width=600,
)
