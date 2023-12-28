########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import html

# Importing Components
from app.components.header import header, collapsing_navbar
from app.pages.save_page_content import save_page, save_page_yaml
from app.pages.info_page_content import info_page
from app.pages.preview_page_content import preview_page, save_yaml_from_preview, load_first_img
from app.components.tabs_content import tabs_content
from app.components.change_page_callback import get_callbacks
from app.components.meta_data_ import update_metadata_tables
from app.components.run_time_settings import update_well_selection_table, populate_list_of_wells
from app.components.instrument_settings import hidden_multi_row_col_feature

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
collapsing_navbar(app)
save_page_yaml(app)
save_yaml_from_preview(app)
update_metadata_tables(app)
update_well_selection_table(app)
hidden_multi_row_col_feature(app)
populate_list_of_wells(app)
load_first_img(app)

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)