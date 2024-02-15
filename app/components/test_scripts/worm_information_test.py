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
import os 

from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header

########################################################################
####                                                                ####
####                           Testing                              ####
####                                                                ####
########################################################################


def test_002_worm_information(dash_duo):
    #defining the app
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

    #hosting the app
    dash_duo.start_server(app)

    #Wait for the presence of the configure link
    configure_link_xpath = '//a[@class="nav-link" and @href="/configure"]'
    WebDriverWait(dash_duo.driver, 10).until(EC.presence_of_element_located((By.XPATH, configure_link_xpath)))

    #clicking the link 
    dash_duo.driver.find_element(by=By.XPATH, value=configure_link_xpath).click()

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
