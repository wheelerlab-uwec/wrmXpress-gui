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
# Header
header = dbc.Row(
    [
        dbc.Col([
            html.A(
                    html.I(className="fa-solid fa-circle-info",
                           id='information-symbol'),
                    href ='', 
        )],
                    width="auto"),
        dbc.Col([
            html.A(
                    html.I(className="fa-solid fa-prescription",
                           id='rx-symbol'),
                    href='',
        )],
                    width="auto"),
        dbc.Col([
            html.A(
                    html.I(className="fa-brands fa-docker",
                           id='docker-symbol'),
                    href = "https://www.docker.com/products/docker-desktop/"
        )],
                    width="auto"),
        dbc.Col([
            html.A(
                    html.I(className="fa-brands fa-github",
                           id='github-symbol'),
                    href = "https://github.com/wheelerlab-uwec/wrmXpress-gui",
        )],
                    width="auto"),
        dbc.Col([
            html.A(
                    html.I(className="fa-brands fa-twitter",
                           id='twitter-symbol'),
                    href = 'https://twitter.com/wheeler_worm'
        )],
                    width="auto")
    ],
    className="w-100 justify-content-end"
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