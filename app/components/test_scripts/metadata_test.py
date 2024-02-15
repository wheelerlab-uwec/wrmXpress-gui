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
def test_005_metadata_checklist(dash_duo):
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

    # hosting the app
    dash_duo.start_server(app)

    #Wait for the presence of the configure link
    metadata_link_xpath = '//a[@class="nav-link" and @href="/metadata"]'
    WebDriverWait(dash_duo.driver, 10).until(EC.presence_of_element_located((By.XPATH, metadata_link_xpath)))

    #clicking the link 
    dash_duo.driver.find_element(by=By.XPATH, value=metadata_link_xpath).click()

    #list containing all known id's on the initial metadata page 
    id_list_1 = [
        'checklist-input', '_dbcprivate_checklist_checklist-input_input_Species', '_dbcprivate_checklist_checklist-input_input_Species',
        '_dbcprivate_checklist_checklist-input_input_Strains', '_dbcprivate_checklist_checklist-input_input_Stages',
        '_dbcprivate_checklist_checklist-input_input_Treatments', '_dbcprivate_checklist_checklist-input_input_Concentrations',
        '_dbcprivate_checklist_checklist-input_input_Other', 'uneditable-input-box', 'finalize-metadata-table-button'
        ]
    
    #testing for id's found in id_list_1
    for element_id_1 in id_list_1:
        css_selector = f'#{element_id_1}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id_1}' not found"

    # using selenium to find and click the Finalize Tables button
    finalize_tables_button = dash_duo.driver.find_element(
        by=By.ID, value="finalize-metadata-table-button")
    finalize_tables_button.click()

    id_list_2 = [
        'Batch-tab-table', 'metadata-tabs'
        ]
    
    #testing for id's found in id_list_1
    for element_id_2 in id_list_2:
        css_selector = f'#{element_id_2}'
        wait = WebDriverWait(dash_duo._driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        assert element is not None, f"Element with id of '{element_id_2}' not found"