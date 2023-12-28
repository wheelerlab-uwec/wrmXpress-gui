########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
# Navbar
header = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                html.Img(src='https://github.com/zamanianlab/wrmXpress/blob/main/img/logo/output.png?raw=true', # wrmXpress image
                             height="100px"),
                href="https://github.com/zamanianlab/wrmxpress", # clicked takes user to wrmXpress github 
                style={"textDecoration": "none"},
                className='ms-5'
            ),

                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                # Buttons for the Navbar
                                dbc.NavItem(dbc.NavLink(
                                    "Info & Usage",
                                    id="open-info-modal",
                                    style={'cursor': 'pointer'})),
                                dbc.NavItem(dbc.NavLink(
                                    "Save YAML",
                                    id="open-save-modal",
                                    style={'cursor': 'pointer'})),
                                dbc.NavItem(dbc.NavLink(
                                    "Preview & Run",
                                    id="open-preview-modal",
                                    style={'cursor': 'pointer'}))
                            ],
                            className="w-100 justify-content-end"
                        ),
                        id="navbar-collapse",
                        is_open=False, # is open
                        navbar=True
                    )
        ]
    ),
    color='white',
    fixed='top' # fixed to the top of the screen
)

########################################################################
####                                                                ####
####                              Callbacks                         ####
####                                                                ####
########################################################################

def collapsing_navbar(app):
    # Collapsing navbar
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open