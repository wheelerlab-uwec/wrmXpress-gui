########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import html

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
                href='',
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
                href="https://www.docker.com/products/docker-desktop/"
            )],
            width="auto"),
        dbc.Col([
            html.A(
                html.I(className="fa-brands fa-github",
                       id='github-symbol'),
                href="https://github.com/wheelerlab-uwec/wrmXpress-gui",
            )],
            width="auto"),
        dbc.Col([
            html.A(
                html.I(className="fa-brands fa-twitter",
                       id='twitter-symbol'),
                href='https://twitter.com/wheeler_worm'
            )],
            width="auto")
    ],
    className="w-100 justify-content-end"
)
