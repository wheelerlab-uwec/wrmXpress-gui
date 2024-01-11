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


def test_002_worm_information(dash_duo):
    # defining the app
    app = dash.Dash(__name__, external_stylesheets=[
        dbc.themes.SPACELAB],
        suppress_callback_exceptions=True)
    app.layout = html.Div([header,
                           # Adding vertical space so tabs content not hidden behind navbar
                           html.H4(
                               "", style={'padding-top': 80, 'display': 'inline-block'}),
                           tabs_content,
                           # Modals (popup screens)
                           save_page,
                           info_page,
                           preview_page,
                           ])

    # hosting the app
    dash_duo.start_server(app)

    # testing for imaging-mode
    # id_list contains all known id's in the code
    id_list = ['species', 'stages', 'worm-information', '_dbcprivate_radioitems_species_input_Bma', '_dbcprivate_radioitems_species_input_Cel',
               '_dbcprivate_radioitems_species_input_Sma', '_dbcprivate_radioitems_stages_input_Mf', '_dbcprivate_radioitems_stages_input_Adult',
               '_dbcprivate_radioitems_stages_input_Mixed']

    # tests for the existacne of specfic elements within the html
    for i in id_list:
        s1 = '#'
        new_string = s1+i
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, new_string)))
        assert element is not None, f"Element with id of '{i}' not found"
