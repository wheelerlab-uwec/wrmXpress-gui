########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import html

# Importing Components
from app.components.header import header
from app.components.save_page_content import save_page
from app.components.info_page_content import info_page
from app.components.preview_page_content import preview_page
from app.components.tabs_content import tabs_content
from app.components.callbacks import get_callbacks

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SPACELAB], 
                suppress_callback_exceptions=True)


########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

app.layout = html.Div([header, 
                       # Adding vertical space so tabs content not hidden behind navbar
                       html.H4("",style={'padding-top': 80, 'display': 'inline-block'}),
                       tabs_content, 
                       # Modals (popup screens)
                        save_page,
                        info_page,
                        preview_page,
                       ])

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################

get_callbacks(app)


########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9000)