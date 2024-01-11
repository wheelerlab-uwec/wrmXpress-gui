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
                html.I(className="fa-solid fa-circle-info", # Information Symbol
                       id='information-symbol'),
                href='',
            )],
            width="auto"),
        dbc.Col([
            html.A(
                html.I(className="fa-solid fa-prescription", # Prescription Symbol
                       id='rx-symbol'),
            )],
            width="auto"),
        dbc.Col([
            html.A(
                html.I(className="fa-brands fa-docker", # Docker Symbol
                       id='docker-symbol'),
                href="https://hub.docker.com/r/wheelern/wrmxpress_gui" # Link to docker install
            )],
            width="auto"),
        dbc.Col([
            html.A(
                html.I(className="fa-brands fa-github", # Github Symbol
                       id='github-symbol'),
                href="https://github.com/wheelerlab-uwec/wrmXpress-gui", # Link to wrmXpress-gui github
            )],
            width="auto"),
        dbc.Col([
            html.A(
                html.I(className="fa-brands fa-twitter", # Twitter Symbol
                       id='twitter-symbol'),
                href='https://twitter.com/wheeler_worm' # Link to wheeler worm twitter page
            )],
            width="auto")
    ],
    className="w-100 justify-content-end"
)
