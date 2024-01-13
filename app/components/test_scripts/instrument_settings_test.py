########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header

########################################################################
####                                                                ####
####                           Testing                              ####
####                                                                ####
########################################################################
def test_001_instrument_settings(dash_duo):
    #defining the app
    app = Dash(__name__,
               use_pages=True,
               pages_folder='pages',
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

    #hosting the app
    dash_duo.start_server(app)

    #Wait for the presence of the configure link
    configure_link_xpath = '//a[@class="nav-link" and @href="/configure"]'
    WebDriverWait(dash_duo.driver, 10).until(EC.presence_of_element_located((By.XPATH, configure_link_xpath)))

    #clicking the link 
    dash_duo.driver.find_element(by=By.XPATH, value=configure_link_xpath).click()

    #id_list contains all known id's in the code
    id_list = [
        'imaging-mode-header', 'imaging-mode-symbol', 'imaging-mode', 'multi-well-rows', 'multi-well-cols', 'multi-well-options-row',
        'multi-site-imaging-mode-info-symbol', 'multi-site-well-cols', 'multi-site-num-rows', 'multi-site-foramt-options-row', 
        'file-structure-symbol', 'file-structure', 'crop-options', 'multi-well-detection', 'additional-options-row', 
        'tot-num-cols-and-rows-symbol', 'total-well-cols', 'total-num-rows', 'plate-foramt-options-row', 'circ-or-square-img-mask',
        'circ-or-square-img-masking', 'instrument-settings-file-structure', '_dbcprivate_radioitems_imaging-mode_input_multi-well',
        '_dbcprivate_radioitems_file-structure_input_imagexpress', '_dbcprivate_radioitems_file-structure_input_avi',
        '_dbcprivate_radioitems_multi-well-detection_input_auto', '_dbcprivate_radioitems_multi-well-detection_input_grid',
        '_dbcprivate_radioitems_circ-or-square-img-masking_input_circle', '_dbcprivate_radioitems_circ-or-square-img-masking_input_square',
        ]

    #testing for each id
    for element_id in id_list:
        css_selector = f'#{element_id}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id}' not found"

        

