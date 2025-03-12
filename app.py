# In[1]: Imports

import dash
from waitress import serve
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, DiskcacheManager
from dash.dependencies import Input, Output, State

# Importing Components
from app.utils.styling import CONTENT_STYLE, SIDEBAR_STYLE
from app.components.header import header
from app.components.fetch_data_modal import fetch_data_modal
from app.utils.background_callback import callback
from app.utils.wrmxpress_gui_obj import WrmXpressGui

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

# In[2]: App Layout

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
            ],
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.Button(
                            html.Img(
                                src="assets/zenodo-white-border.svg",
                                style={"width": "95%"},
                            ),
                            id="fetch-data-link",
                            style={"width": "90%"},
                        ),
                        # Tooltip for the NavLink
                        dbc.Tooltip(
                            "Click to fetch example data from Zenodo and download it to your Downloads folder.",
                            target="fetch-data-link",  # Associate tooltip with the NavLink ID
                            placement="top",  # Position the tooltip (optional)
                        ),
                    ]
                ),
            ],
            style={"position": "fixed", "bottom": 10},
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
        fetch_data_modal,  # Fetch data modal, see fetch_data_modal.py
    ]
)

# In[3]: Callbacks


@app.callback(
    output=[
        Output("image-analysis-preview", "figure"),
        Output("load-analysis-img", "disabled"),
        Output("run-page-alert", "is_open"),
        Output("run-page-alert", "children"),
        Output("progress-message-run-page-markdown", "children"),
        Output("progress-message-run-page-for-analysis", "children"),
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
            Output("progress-bar-run-page", "animated"),
            True,
            False,
        ),
    ],
    cancel=[Input("cancel-analysis", "n_clicks")],
    progress=[
        Output("progress-bar-run-page", "value"),
        Output("progress-bar-run-page", "max"),
        Output("image-analysis-preview", "figure"),
        Output("progress-message-run-page-for-analysis", "children"),
        Output("progress-message-run-page-markdown", "children"),
        Output("first-view-of-analysis-alert", "is_open"),
        Output("before-first-view-of-analysis-alert", "is_open"),
    ],
    prevent_initial_call=True,
    allow_duplicate=True,
    background=True,
)
def background_callback(set_progress, n_clicks, store_data):
    """
    This function runs the wrmXpress analysis in the background.
    """

    try:

        if not store_data:
            return (
                {},
                True,
                True,
                "No Configuration Found. Please go to the Configuration Page to set the configuration.",
                None,
                None,
            )

        wrmXpress_gui_obj = WrmXpressGui(
            file_structure=store_data["wrmXpress_gui_obj"]["file_structure"],
            imaging_mode=store_data["wrmXpress_gui_obj"]["imaging_mode"],
            multi_well_row=store_data["wrmXpress_gui_obj"]["multi_well_row"],
            multi_well_col=store_data["wrmXpress_gui_obj"]["multi_well_col"],
            multi_well_detection=store_data["wrmXpress_gui_obj"][
                "multi_well_detection"
            ],
            x_sites=store_data["wrmXpress_gui_obj"]["x_sites"],
            y_sites=store_data["wrmXpress_gui_obj"]["y_sites"],
            stitch_switch=store_data["wrmXpress_gui_obj"]["stitch_switch"],
            well_col=store_data["wrmXpress_gui_obj"]["well_col"],
            well_row=store_data["wrmXpress_gui_obj"]["well_row"],
            mask=store_data["wrmXpress_gui_obj"]["mask"],
            mask_diameter=store_data["wrmXpress_gui_obj"]["mask_diameter"],
            pipeline_selection=store_data["wrmXpress_gui_obj"]["pipeline_selection"],
            wavelengths=store_data["wrmXpress_gui_obj"]["wavelengths"],
            pyrscale=store_data["wrmXpress_gui_obj"]["pyrscale"],
            levels=store_data["wrmXpress_gui_obj"]["levels"],
            winsize=store_data["wrmXpress_gui_obj"]["winsize"],
            iterations=store_data["wrmXpress_gui_obj"]["iterations"],
            poly_n=store_data["wrmXpress_gui_obj"]["poly_n"],
            poly_sigma=store_data["wrmXpress_gui_obj"]["poly_sigma"],
            flags=store_data["wrmXpress_gui_obj"]["flags"],
            cellpose_model_segmentation=store_data["wrmXpress_gui_obj"][
                "cellpose_model_segmentation"
            ],
            type_segmentation=store_data["wrmXpress_gui_obj"]["type_segmentation"],
            python_model_sigma=store_data["wrmXpress_gui_obj"]["python_model_sigma"],
            wavelengths_segmentation=store_data["wrmXpress_gui_obj"][
                "wavelengths_segmentation"
            ],
            cellprofiler_pipeline_selection=store_data["wrmXpress_gui_obj"][
                "cellprofiler_pipeline_selection"
            ],
            cellpose_model_cellprofiler=store_data["wrmXpress_gui_obj"][
                "cellpose_model_cellprofiler"
            ],
            wavelengths_cellprofiler=store_data["wrmXpress_gui_obj"][
                "wavelengths_cellprofiler"
            ],
            wavelengths_tracking=store_data["wrmXpress_gui_obj"][
                "wavelengths_tracking"
            ],
            tracking_diameter=store_data["wrmXpress_gui_obj"]["tracking_diameter"],
            tracking_minmass=store_data["wrmXpress_gui_obj"]["tracking_minmass"],
            tracking_noisesize=store_data["wrmXpress_gui_obj"]["tracking_noisesize"],
            tracking_searchrange=store_data["wrmXpress_gui_obj"][
                "tracking_searchrange"
            ],
            tracking_memory=store_data["wrmXpress_gui_obj"]["tracking_memory"],
            tracking_adaptivestop=store_data["wrmXpress_gui_obj"][
                "tracking_adaptivestop"
            ],
            static_dx=store_data["wrmXpress_gui_obj"]["static_dx"],
            static_dx_rescale=store_data["wrmXpress_gui_obj"]["static_dx_rescale"],
            video_dx=store_data["wrmXpress_gui_obj"]["video_dx"],
            video_dx_format=store_data["wrmXpress_gui_obj"]["video_dx_format"],
            video_dx_rescale=store_data["wrmXpress_gui_obj"]["video_dx_rescale"],
            mounted_volume=store_data["wrmXpress_gui_obj"]["mounted_volume"],
            plate_name=store_data["wrmXpress_gui_obj"]["plate_name"],
            well_selection_list=store_data["wrmXpress_gui_obj"]["well_selection_list"],
        )

        error_occured, _, _, _ = wrmXpress_gui_obj.validate()

        if error_occured:

            return (
                {},
                True,
                True,
                "A configuration error has occurred. Please return to the Configuration Page to fix the error.",
                None,
                None,
            )

        if n_clicks:

            # print("Preparing to run analysis")
            # wrmXpress_gui_obj.setup_run_analysis(store_data["file_structure"])
            # print("Running analysis")
            # wrmXpress_gui_obj.run_analysis(set_progress)

            return callback(set_progress, store_data, wrmXpress_gui_obj)

    except Exception as e:
        error_message = f"An error occurred (this one): {str(e)}"
        print(error_message)
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
            None,
        )


# Add callbacks for handling the modal and fetch operation
@app.callback(
    Output("fetch-data-modal", "is_open"),  # Controls the modal visibility
    [
        Input("fetch-data-link", "n_clicks"),
        Input("confirm-fetch", "n_clicks"),
        Input("cancel-fetch", "n_clicks"),
    ],
    [State("fetch-data-modal", "is_open")],
)
def toggle_modal(fetch_click, confirm_click, cancel_click, is_open):
    # Open the modal on fetch-data-link click
    if fetch_click and not is_open:
        return True
    # Close the modal on Yes or No button click
    if confirm_click or cancel_click:
        return False
    return is_open


# In[4]: Run the app

if __name__ == "__main__":
    # for dev/debugging
    # app.run_server(debug=True, host="0.0.0.0", port=9000)
    serve(app.server, host="0.0.0.0", port=9000, threads=16)
