########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os 

from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header

########################################################################
####                                                                ####
####                           Testing                              ####
####                                                                ####
########################################################################


def test_003_module_selection(dash_duo):
    # defining the app
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    #defining the app
    app = Dash(__name__,
               use_pages=True,
               pages_folder = os.path.join(script_dir, "..", "..", "..", "app", "pages"),
               external_stylesheets=[
                   dbc.themes.FLATLY,
                   dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True)
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
                children=[header, dash.page_container],
                style=CONTENT_STYLE)])

    # hosting the app
    dash_duo.start_server(app)

    #Wait for the presence of the configure link
    configure_link_xpath = '//a[@class="nav-link" and @href="/configure"]'
    WebDriverWait(dash_duo.driver, 10).until(EC.presence_of_element_located((By.XPATH, configure_link_xpath)))

    #clicking the link 
    dash_duo.driver.find_element(by=By.XPATH, value=configure_link_xpath).click()

    # using selenium to find and click the module selection dropdown
    module_selection_dropdown = dash_duo.driver.find_element(
        by=By.XPATH, value='//*[@id="module-selection"]/h2/button')
    dash_duo.driver.execute_script("arguments[0].click()", module_selection_dropdown)

    # using selenium to find and click the "Video Analysis" tab
    video_analysis_option = dash_duo.driver.find_element(
        by=By.XPATH, value='//*[@id="module-tabs"]/div[1]')
    dash_duo.driver.execute_script("arguments[0].click()", video_analysis_option)

    # id_list_1 contains all known id's in the video analysis tab
    id_list_1 = [
        'motility-run', 'motility-symbol', 'conversion-symbol', 'conversion-run', 'rescale-symbol', 'conversion-scale-video',
        'conversion-rescale-multiplier', 'segment-run', 'segmentation-wavelength', 'module-tabs-parent', 'dx-symbol',
        '_dbcprivate_radioitems_motility-run_input_True', '_dbcprivate_radioitems_motility-run_input_False',
        '_dbcprivate_radioitems_conversion-run_input_True', '_dbcprivate_radioitems_conversion-run_input_False',
        '_dbcprivate_radioitems_conversion-scale-video_input_True', '_dbcprivate_radioitems_conversion-scale-video_input_False',
        '_dbcprivate_radioitems_segment-run_input_True', '_dbcprivate_radioitems_segment-run_input_False',
        '_dbcprivate_radioitems_diagnostics-dx_input_True', '_dbcprivate_radioitems_diagnostics-dx_input_False'
    ]

    # tests for the existence id's found in id_list_1
    for element_id_1 in id_list_1:
        css_selector = f'#{element_id_1}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id_1}' not found"

    # using selenium to find and click the "Image Analysis (CellProfiler)" tab
    image_analysis_option = dash_duo.driver.find_element(
        by=By.XPATH, value='//*[@id="module-tabs"]/div[2]')
    dash_duo.driver.execute_script("arguments[0].click()", image_analysis_option)

    # id_list_2 contains all known id's in the video analysis tab
    id_list_2 = [
        'cell-profiler-run', 'cell-profiler-pipeline', 'dx-symbol', 'diagnostics-dx', '_dbcprivate_radioitems_cell-profiler-pipeline_input_wormsize_intensity_cellpose',
        '_dbcprivate_radioitems_cell-profiler-pipeline_input_mf_celltox', '_dbcprivate_radioitems_cell-profiler-pipeline_input_wormsize',
        '_dbcprivate_radioitems_cell-profiler-pipeline_input_wormsize_trans'
    ]

    # tests for the existence id's found in id_list_2
    for element_id_2 in id_list_2:
        css_selector = f'#{element_id_2}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id_2}' not found"
