# In[1]: Imports

from dash import callback, Input, Output, State
from pathlib import Path
import os
import dash
from dash.long_callback import DiskcacheLongCallbackManager

# importing utils
from app.utils.callback_functions import send_ctrl_c, create_figure_from_filepath
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
    This function loads the analysis image based on the selection.
    """
    # Check to see if store exists
    if not store_data:
        return {}, "", True, False, True, True, True, False

    scale = "gray"
    # TODO: Fix this function to work with the new file structure
    # and the selection of the analysis dropdown
    if n_clicks:
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
            cellpose_model_type_segmentation=store_data["wrmXpress_gui_obj"][
                "cellpose_model_type_segmentation"
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

        # print(selection)
        if selection == "optical_flow":
            scale = "inferno"

        wrmXpress_gui_obj.check_for_output_files()

        if wrmXpress_gui_obj.output_files_exist:

            # get the wrmXpress_gui_obj.output_file path for the file that contains selection
            img_paths = wrmXpress_gui_obj.get_output_file_path(selection)
            if len(img_paths) >= 1:
                fig = create_figure_from_filepath(img_paths[0], scale)
                return (
                    fig,
                    f"```{str(img_paths[0])}```",
                    False,
                    True,
                    False,
                    False,
                    False,
                    True,
                )

        return {}, "", True, False, True, True, True, False
    else:
        return None, None, True, False, False, False, True, False

    """
    try:
        # Get the store data
        volume = store["wrmXpress_gui_obj"]["mounted_volume"]
        platename = store["wrmXpress_gui_obj"]["plate_name"]

        # Handle NoneType for platename
        if platename is None:
            return {}, "", True, False, True, True, True, False

        plate_base = platename.split("_", 1)[0]
        wells = store["wrmXpress_gui_obj"]["well_selection_list"]

        img_path = None
        scale = "gray"
        # check to see if selection option exists in output thumbs folder
        if n_clicks:

            if selection == "straightened_worms":

                path_to_straightened_worms = Path(volume, "output/straightened_worms/")
                pattern = f"{plate_base}*{wells[0]}*.tiff"
                all_files = list(path_to_straightened_worms.glob(pattern))
                # Filter files to find those corresponding to the first well in the list
                straightened_worm_files = []
                for file_path in all_files:
                    if file_path.name.startswith(
                        f"{plate_base}_{wells[0]}"
                    ) or file_path.name.startswith(f"{plate_base}-{wells[0]}"):
                        straightened_worm_files.append(file_path)

                if straightened_worm_files:
                    img_path = straightened_worm_files[0]  # Use the first matching file

            elif selection.startswith("wavelength_"):
                selection = selection.split("_", 1)[1]
                img_path = Path(volume, f"output/thumbs/{platename}_{selection}.png")

            elif selection == "motility":
                selection = "_motility"
                scale = "inferno"
                img_path = Path(volume, f"output/thumbs/{platename}{selection}.png")

            elif selection == "raw":
                selection = ""
                img_path = Path(volume, f"output/thumbs/{platename}{selection}.png")

            elif selection == "segment":
                selection = "_binary"
                img_path = Path(volume, f"output/thumbs/{platename}{selection}.png")

            else:
                selection = f"_{selection}"
                img_path = Path(volume, f"output/thumbs/{platename}{selection}.png")

            # check to see if the img exists
            if os.path.exists(img_path):
                fig = create_figure_from_filepath(img_path, scale)

                return fig, f"```{img_path}```", False, True, False, False, False, True

            else:
                return None, None, False, False, False, False, True, False

        else:
            return None, None, True, False, False, False, True, False

    except KeyError:
        return None, None, True, False, True, True, True, False
    """


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
        cellpose_model_type_segmentation=store_data["wrmXpress_gui_obj"][
            "cellpose_model_type_segmentation"
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
        return selection_dict
    else:
        return {}
