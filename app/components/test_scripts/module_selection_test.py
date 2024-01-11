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
def test_003_worm_information(dash_duo):
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

    #hosting the app
    dash_duo.start_server(app)

    #using selenium to find and click the module selection dropdown
    module_selection_dropdown = dash_duo.driver.find_element(by=By.ID, value = "module-selection")
    module_selection_dropdown.click()

    #using selenium to find and click the "Video Analysis" tab
    video_analysis_option = dash_duo.driver.find_element(by=By.XPATH, value= '//*[@id="module-tabs"]/div[1]')
    video_analysis_option.click()

    #id_list_1 contains all known id's in the video analysis tab
    id_list_1 = [
        'motility-run', 'motility-symbol', 'conversion-symbol', 'conversion-run', 'rescale-symbol', 'conversion-scale-video',
        'conversion-rescale-multiplier', 'segment-run', 'segmentation-wavelength', 'module-tabs-parent', 'dx-symbol', 
        '_dbcprivate_radioitems_motility-run_input_True', '_dbcprivate_radioitems_motility-run_input_False',
        '_dbcprivate_radioitems_conversion-run_input_True', '_dbcprivate_radioitems_conversion-run_input_False', 
        '_dbcprivate_radioitems_conversion-scale-video_input_True', '_dbcprivate_radioitems_conversion-scale-video_input_False',
        '_dbcprivate_radioitems_segment-run_input_True', '_dbcprivate_radioitems_segment-run_input_False', 
        '_dbcprivate_radioitems_diagnostics-dx_input_True', '_dbcprivate_radioitems_diagnostics-dx_input_False'
        ]

    #tests for the existence id's found in id_list_1
    for element_id_1 in id_list_1:
        css_selector = f'#{element_id_1}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id_1}' not found"

    #using selenium to find and click the "Image Analysis (CellProfiler)" tab
    image_analysis_option = dash_duo.driver.find_element(by=By.XPATH, value = '//*[@id="module-tabs"]/div[2]')
    image_analysis_option.click()

    # id_list_2 contains all known id's in the video analysis tab
    id_list_2 = [
        'cell-profiler-run', 'cell-profiler-pipeline', 'dx-symbol', 'diagnostics-dx', '_dbcprivate_radioitems_cell-profiler-pipeline_input_wormsize_intensity_cellpose',
        '_dbcprivate_radioitems_cell-profiler-pipeline_input_mf_celltox', '_dbcprivate_radioitems_cell-profiler-pipeline_input_wormsize',
        '_dbcprivate_radioitems_cell-profiler-pipeline_input_wormsize_trans'
        ]
    
    #tests for the existence id's found in id_list_2
    for element_id_2 in id_list_2:
        css_selector = f'#{element_id_2}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id_2}' not found"


