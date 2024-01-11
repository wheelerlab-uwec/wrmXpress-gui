########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.components.header import header, collapsing_navbar
from app.pages.save_page_content import save_page, save_page_yaml
from app.pages.info_page_content import info_page
from app.pages.preview_page_content import preview_page, load_first_img, preview_analysis, populate_options
from app.components.tabs_content import tabs_content
from app.components.change_page_callback import get_callbacks
from app.components.metadata_tab import open_metadata_offcanvas
from app.components.run_time_settings import update_well_selection_table, populate_list_of_wells
from app.components.instrument_settings import hidden_multi_row_col_feature
from app.components.create_metadata_tabs_from_checklist import create_metadata_tables_from_checklist
from app.components.metadata_table_checklist import add_metadata_table_checklist
from app.components.save_metadata_tables import save_metadata_tables_to_csv

########################################################################
####                                                                ####
####                           Testing                              ####
####                                                                ####
########################################################################
def test_004_run_time_settings(dash_duo):
    #defining the app
    app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SPACELAB], 
                suppress_callback_exceptions=True)
    app.layout = html.Div([header, 
                       # Adding vertical space so tabs content not hidden behind navbar
                       html.H4("",style={'padding-top': 80, 'display': 'inline-block'}),
                       tabs_content, 
                       # Modals (popup screens)
                        save_page,
                        info_page,
                        preview_page,
                       ])

    # hosting the app
    dash_duo.start_server(app)

    #list containing known id's in the app
    id_list = ['mounted-volume', 'plate-name', 'well-selection-list', 'run-time-settings', 'well-selection-table']

    #testing for the existence of id's found in id_list
    for element_id in id_list:
        css_selector = f'#{element_id}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id}' not found"