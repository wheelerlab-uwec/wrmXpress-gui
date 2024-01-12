########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header
from app.pages.errormodal import error_modal
app = Dash(__name__,
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
             children=[header, dash.page_container, error_modal],
             style=CONTENT_STYLE)])

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)
