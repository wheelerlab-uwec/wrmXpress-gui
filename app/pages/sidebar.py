########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from app.pages.info_page_content import info_page_content
from app.pages.configure_analysis import configure_analysis
from app.pages.metadata_tab import meta_data
from app.pages.preview_page_content import preview_page_content
from app.pages.run_page_content import run_page_content
from app.components.header import header
from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE

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
        dbc.Nav(
            [
                dbc.NavLink("Info", href="/", active="exact"),
                dbc.NavLink("Configure", href="/configure", active="exact"),
                dbc.NavLink("Metadata", href="/metadata", active="exact"),
                dbc.NavLink('Preview', href='/preview', active='exact'),
                dbc.NavLink('Run', href='/run', active='exact')
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([
    header,
    html.Div(id="page-content", style=CONTENT_STYLE)
])

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################


def change_page_from_sidebar(app):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return info_page_content
        elif pathname == "/configure":
            return configure_analysis
        elif pathname == "/metadata":
            return meta_data
        elif pathname == '/preview':
            return preview_page_content
        elif pathname == '/run':
            return run_page_content
        # If the user tries to reach a different page, return the infomation page
        return info_page_content
