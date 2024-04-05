########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
import dash_bootstrap_components as dbc
from dash import html

# Importing Components
from app.utils.styling import SIDEBAR_STYLE 

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
                children=dbc.NavLink(
                    # Page name
                    f"{page['name']}",
                    href=page["relative_path"],  # Page path
                    active='exact'
                ),
                pills=True,  # Style of the navigation
                vertical=True  # Style of the navigation
            ) for page in dash.page_registry.values()  # Iterate through each page
        ])
    ],
    style=SIDEBAR_STYLE  # Style of the sidebar, see styling.py
)