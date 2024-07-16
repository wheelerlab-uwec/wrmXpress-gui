########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
from waitress import serve
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, DiskcacheManager
from dash.dependencies import Input, Output, State

# Importing Components
from app.utils.styling import CONTENT_STYLE, SIDEBAR_STYLE
from app.components.header import header
from app.utils.background_callback import callback

# Diskcache
import diskcache

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(
    __name__,
    long_callback_manager=background_callback_manager,
    use_pages=True,
    pages_folder="app/pages",
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
)

########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

sidebar = html.Div(
    [
        html.A(
            html.Img(
                src="https://github.com/zamanianlab/wrmXpress/blob/main/img/logo/output.png?raw=true",  # wrmXpress image
                height="200px",
            ),
            # clicked takes user to wrmXpress github
            href="https://github.com/zamanianlab/wrmxpress",
            style={"textDecoration": "none"},
            className="ms-3",
        ),
        html.Hr(),
        html.Div(
            [
                dbc.Nav(
                    children=dbc.NavLink(
                        # Page name
                        f"{page['name']}",
                        href=page["relative_path"],  # Page path
                        active="exact",
                    ),
                    pills=True,  # Style of the navigation
                    vertical=True,  # Style of the navigation
                )
                for page in dash.page_registry.values()  # Iterate through each page
            ]
        ),
    ],
    style=SIDEBAR_STYLE,  # Style of the sidebar, see styling.py
)

app.layout = html.Div(
    [
        dcc.Store(id="store", data={}),  # Store data
        sidebar,  # Sidebar see above
        html.Div(
            id="page-content",
            children=[
                header,  # Header see header.py
                dash.page_container,  # Page container, see app/pages/
            ],
            style=CONTENT_STYLE,  # Style of the content, see styling.py
        ),
    ]
)

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@app.callback(
    output=[
        Output("image-analysis-preview", "figure"),
        Output("load-analysis-img", "disabled"),
        Output("run-page-alert", "is_open"),
        Output("run-page-alert", "children"),
        Output("progress-message-run-page-markdown", "children"),
    ],
    inputs=[
        Input("submit-analysis", "n_clicks"),
        State("store", "data"),
    ],
    running=[
        (Output("submit-analysis", "disabled"), True, False),
        (Output("cancel-analysis", "disabled"), False, True),
        (
            Output("image-analysis-preview", "style"),
            {"visibility": "visible"},
            {"visibility": "visible"},
        ),
        (
            Output("progress-bar-run-page", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"},
        ),
        (
            Output("progress-message-run-page-for-analysis", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"},
        ),
    ],
    cancel=[Input("cancel-analysis", "n_clicks")],
    progress=[
        Output("progress-bar-run-page", "value"),
        Output("progress-bar-run-page", "max"),
        Output("image-analysis-preview", "figure"),
        Output("progress-message-run-page-for-analysis", "children"),
        Output("progress-message-run-page-markdown", "children"),
    ],
    prevent_initial_call=True,
    allow_duplicate=True,
    background=True,
)
def background_callback(set_progress, n_clicks, store):
    """
    This function runs the wrmXpress analysis in the background.
    =========================================================================================
    Arguments:
        - set_progress : function : The function to set the progress
            +- progress bar value : int : The progress bar value
            +- progress bar max : int : The progress bar max
            +- image analysis preview : dict : The image analysis preview
            +- progress message run page for analysis : str : The progress message run page for analysis
            +- progress message run page markdown : str : The progress message run page markdown
        - n_clicks : int : The number of clicks of the submit button on the run page
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
    =========================================================================================
    Returns:
        - callback : function : The callback function defined in app/utils/background_callback.py
            +- set progress : function : The set progress function defined above
            +- n_clicks : int : The number of clicks from the submit button on the run page
            +- store : dict : The store data defined above
    =========================================================================================
    """
    try:
        return callback(set_progress, n_clicks, store)

    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


########################################################################
####                                                                ####
####                        RUNNING SERVER                          ####
####                                                                ####
########################################################################

if __name__ == "__main__":
    # for dev/debugging
    # app.run_server(debug=True, host="0.0.0.0", port=9000)
    serve(app.server, host="0.0.0.0", port=9000, threads=16)
