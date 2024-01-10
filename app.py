########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

# Importing Components
# from app.components.header import header, collapsing_navbar
# from app.pages.save_page_content import save_page, save_page_yaml
# from app.pages.info_page_content import info_page
# from app.pages.preview_page_content import preview_page, load_first_img, preview_analysis, populate_options
# from app.components.tabs_content import tabs_content
# from app.components.change_page_callback import get_callbacks
# from app.components.run_time_settings import update_well_selection_table, populate_list_of_wells
# from app.components.instrument_settings import hidden_multi_row_col_feature
# from app.components.create_metadata_tabs_from_checklist import create_metadata_tables_from_checklist
# from app.components.metadata_table_checklist import add_metadata_table_checklist
# from app.components.save_metadata_tables import save_metadata_tables_to_csv
# from app.pages.sidebar import sidebar, content, change_page_from_sidebar

app = Dash(__name__,
           use_pages=True,
           pages_folder='app/pages',
           external_stylesheets=[
               dbc.themes.FLATLY,
               dbc.icons.FONT_AWESOME],
           suppress_callback_exceptions=True)


########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

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
                vertical=True,
                pills=True,
                children=dbc.NavLink(f"{page['name']} - {page['path']}",
                                     href=page["relative_path"])
            ) for page in dash.page_registry.values()
        ])
    ],
    style=SIDEBAR_STYLE
)


app.layout = html.Div([
    dcc.Store(id='store', data={}),
    sidebar,
    html.Div(id="page-content",
             children=dash.page_container,
             style=CONTENT_STYLE)])

########################################################################
####                                                                ####
####                           CALLBACKS                            ####
####                                                                ####
########################################################################

# get_callbacks(app)
# collapsing_navbar(app)
# save_page_yaml(app)
# add_metadata_table_checklist(app)
# update_well_selection_table(app)
# hidden_multi_row_col_feature(app)
# populate_list_of_wells(app)
# load_first_img(app)
# preview_analysis(app)
# create_metadata_tables_from_checklist(app)
# save_metadata_tables_to_csv(app)
# populate_options(app)
# change_page_from_sidebar(app)

########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=9000)
