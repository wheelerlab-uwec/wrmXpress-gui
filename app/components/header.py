########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import callback_context, dash_table, dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
header = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                html.Img(src='https://github.com/zamanianlab/wrmXpress/blob/main/img/logo/output.png?raw=true',
                             height="100px"),
                href="https://github.com/zamanianlab/wrmxpress",
                style={"textDecoration": "none"},
                className='ms-5'
            ),

                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [
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
                        is_open=False,
                        navbar=True
                    )
        ]
    ),
    color='white',
    fixed='top'
)