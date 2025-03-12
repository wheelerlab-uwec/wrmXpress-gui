# In[1]: Imports

from dash import callback, Input, Output, State
from pathlib import Path
import os
import dash
from dash.long_callback import DiskcacheLongCallbackManager
import time

# importing utils
from app.utils.callback_functions import send_ctrl_c, create_figure_from_filepath, construct_img_path
from app.components.run_layout import run_layout
from app.utils.wrmxpress_gui_obj import WrmXpressGui

# Diskcache
import diskcache

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

dash.register_page(__name__, long_callback_manager=long_callback_manager)

# In[2]: Layout

layout = run_layout

# In[3]: Callbacks


# Callback to keep updating the dummy component
@callback(
    Output("force-loading-output", "children"), Input("loading-interval", "n_intervals")
)
def keep_loading(n):
    time.sleep(0.5)
    return f""


@callback(Output("cancel-analysis", "n_clicks"), Input("cancel-analysis", "n_clicks"))
def cancel_analysis(n_clicks):
    """
    This function cancels the analysis by typing "Control" + "C" in the terminal.
    """
    if n_clicks:

        # Replace `1234` with the actual PID
        send_ctrl_c(  # Send Control + C to the process with PID 1234
            1234  # see app/utils/callback_functions.py for more details
        )

        print("Control + C", "wrmxpress analysis cancelled")

    return n_clicks


@callback(
    Output("analysis-postview", "figure"),
    Output("analysis-postview-message", "children"),
    Output("first-view-of-analysis-alert", "is_open"),
    Output("additional-view-of-analysis-alert", "is_open"),
    Output("run-page-no-store-alert", "is_open"),
    Output("submit-analysis", "disabled"),
    Output("run-page-file-paths-alert", "is_open"),
    Output("run-page-file-paths-alert-update", "is_open"),
    State("analysis-dropdown", "value"),
    Input("load-analysis-img", "n_clicks"),
    State("store", "data"),
    allow_duplicate=True,
    # prevent_initial_call=True,
)
def load_analysis_img(selection, n_clicks, store_data):
    """
    Load and display the analysis image based on the user's selection.
    """
    # print("selection", selection)

    if not store_data:
        # Store data is None or invalid.
        return {}, "", True, False, True, True, True, False

    # Extract necessary fields from store_data
    gui_obj = store_data.get("wrmXpress_gui_obj", {})
    volume = gui_obj.get("mounted_volume")
    platename = gui_obj.get("plate_name")
    wells = gui_obj.get("well_selection_list", [])
    wavelength = gui_obj.get("wavelengths")

    if not volume or not platename:
        # Mounted volume or plate name is missing.
        return {}, "", True, False, True, True, True, False

    if not n_clicks:
        # No clicks detected
        return None, None, True, False, False, False, True, False
    
    try:
        # Derive plate_base and construct the image path
        plate_base = platename.split("_", 1)[0]
        img_path = construct_img_path(volume, selection, plate_base, wells, wavelength)

        if img_path and img_path.exists():
            # print(f"Image path found: {img_path}")"
            scale = "inferno" if selection == "optical_flow" else "gray"
            fig = create_figure_from_filepath(img_path, scale)
            return (
                fig,
                f"```{str(img_path)}```",
                False,
                True,
                False,
                False,
                False,
                True,
            )
        else:
            print(f"File does not exist or path is invalid: {img_path}")
            return {}, "", True, False, True, True, True, False
    except Exception as e:
        print(f"Error during processing: {e}")
        return {}, "", True, False, True, True, True, False


@callback(
    Output("analysis-dropdown", "options"),
    # update the option dropdown when the run analysis is clicked
    Input("submit-analysis", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def get_options_analysis(nclicks, store_data):
    """
    This function gets the options for the analysis.
    """

    # check to see if store exists
    if not store_data:
        return {}

    # get the store from the data
    wrmXpress_gui_obj = WrmXpressGui(
        file_structure=store_data["wrmXpress_gui_obj"]["file_structure"],
        imaging_mode=store_data["wrmXpress_gui_obj"]["imaging_mode"],
        multi_well_row=store_data["wrmXpress_gui_obj"]["multi_well_row"],
        multi_well_col=store_data["wrmXpress_gui_obj"]["multi_well_col"],
        multi_well_detection=store_data["wrmXpress_gui_obj"]["multi_well_detection"],
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
        type_segmentation=store_data["wrmXpress_gui_obj"][
            "type_segmentation"
        ],
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
        tracking_searchrange=store_data["wrmXpress_gui_obj"]["tracking_searchrange"],
        tracking_memory=store_data["wrmXpress_gui_obj"]["tracking_memory"],
        tracking_adaptivestop=store_data["wrmXpress_gui_obj"]["tracking_adaptivestop"],
        static_dx=store_data["wrmXpress_gui_obj"]["static_dx"],
        static_dx_rescale=store_data["wrmXpress_gui_obj"]["static_dx_rescale"],
        video_dx=store_data["wrmXpress_gui_obj"]["video_dx"],
        video_dx_format=store_data["wrmXpress_gui_obj"]["video_dx_format"],
        video_dx_rescale=store_data["wrmXpress_gui_obj"]["video_dx_rescale"],
        mounted_volume=store_data["wrmXpress_gui_obj"]["mounted_volume"],
        plate_name=store_data["wrmXpress_gui_obj"]["plate_name"],
        well_selection_list=store_data["wrmXpress_gui_obj"]["well_selection_list"],
    )

    # get the pipeline selection
    selection_dict = wrmXpress_gui_obj.get_image_diagnostic_parameters()

    if nclicks is not None:
        options = [
            {"label": key, "value": value} for key, value in selection_dict.items()
        ]
        return options
    else:
        return {"raw": "raw"}
