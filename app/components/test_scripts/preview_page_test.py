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
def test_006_preview_page(dash_duo):
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
    preview_link_xpath = '//a[@class="nav-link" and @href="/preview"]'
    WebDriverWait(dash_duo.driver, 10).until(EC.presence_of_element_located((By.XPATH, preview_link_xpath)))

    #clicking the link 
    dash_duo.driver.find_element(by=By.XPATH, value=preview_link_xpath).click()

    id_list = [
        'input-path-output', 'input-preview', 'submit-val', 'preview-dropdown', 'analysis-preview-message',
        'analysis-preview', 'preview-button', '_pages_dummy', 
        ]
    
    #testing for each id
    for element_id in id_list:
        css_selector = f'#{element_id}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id}' not found"