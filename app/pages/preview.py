# In[1]: Imports

import dash
from dash import callback, Input, Output, State
import time
from pathlib import Path
import os

# importing utils
from app.utils.callback_functions import create_figure_from_filepath
from app.utils.preview_callback_functions import preview_callback_functions
from app.components.preview_layout import preview_layout
from app.utils.wrmxpress_gui_obj import WrmXpressGui

dash.register_page(__name__)

# In[2]: Layout

layout = preview_layout

# In[3]: Callbacks


@callback(
    Output("analysis-preview-other-img", "figure"),
    Output("preview-img-view-alert", "is_open"),
    Output("post-analysis-first-well-img-view-alert", "is_open"),
    Output("no-store-data-alert", "is_open"),
    Output("submit-val", "disabled"),
    Output("analysis-preview-message-alert", "is_open"),
    Output("analysis-preview-dx-alert-message", "is_open"),
    Output("analysis-preview-dx-message", "children"),
    State("preview-dropdown", "value"),
    Input("preview-change-img-button", "n_clicks"),
    State("store", "data"),
)
def update_analysis_preview_image(selection, nclicks, store):
    """
    This function updates the analysis preview image based on the selection
    """

    # if store == error_test:
    #     return error_check_test_true()

    # Check if store is empty
    if not store:
        return (
            None,
            True,
            False,
            True,
            True,
            True,
            False,
            None,
        )

    # check if store has the essential elements
    if (
        store["wrmXpress_gui_obj"]["plate_name"] == None
        or store["wrmXpress_gui_obj"]["mounted_volume"] == None
    ):
        return (
            None,
            True,
            False,
            True,
            True,
            True,
            False,
            None,
        )

    try:
        volume = store["wrmXpress_gui_obj"]["mounted_volume"]
        platename = store["wrmXpress_gui_obj"]["plate_name"]
        wells = store["wrmXpress_gui_obj"]["well_selection_list"]

        try:
            plate_base = platename.split("_", 1)[0]

        except Exception as e:
            return None, True, False, False, False, True, False, f"```{str(e)}```"

        pipeline_selection = store["wrmXpress_gui_obj"]["pipeline_selection"]

        if nclicks:
            if pipeline_selection == "motility":
                if selection == "raw":
                    selection = ""
                elif selection == "segment":
                    selection = "_binary"
                else:
                    selection = f"_{selection}"

                img_path = Path(
                    f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection}.png"
                )
            elif pipeline_selection == "fecundity":
                if selection == "raw":
                    selection = ""
                else:
                    selection = f"_{selection}"

                img_path = Path(
                    f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection}.png"
                )
            elif pipeline_selection == "tracking":
                if selection == "raw":
                    selection = ""
                else:
                    selection = f"_{selection}"

                img_path = Path(
                    f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection}.png"
                )
            elif pipeline_selection == "wormsize_intensity_cellpose":
                if selection == "raw":
                    img_path = Path(
                        f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
                    )
                elif selection == "straightened_worms":
                    img_path = Path(
                        f"{volume}/output/straightened_worms/{plate_base}_{wells[0]}.tiff"
                    )
                elif selection == "cp_masks":
                    img_path = Path(
                        f"{volume}/input/{platename}/TimePoint_1/{plate_base}_{wells[0]}_cp_masks.png"
                    )
            elif pipeline_selection == "mf_celltox":
                if selection == "raw":
                    img_path = Path(
                        f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
                    )
            elif pipeline_selection == "wormsize":
                if selection == "raw":
                    img_path = Path(
                        f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
                    )
                elif selection == "straightened_worms":
                    img_path = Path(
                        f"{volume}/output/straightened_worms/{plate_base}_{wells[0]}.tiff"
                    )
            elif pipeline_selection == "feeding":
                if selection == "raw":
                    img_path = Path(
                        f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
                    )
                elif selection == "straightened_worms":
                    img_path = Path(
                        f"{volume}/output/straightened_worms/{plate_base}_{wells[0]}.tiff"
                    )
                elif selection.startswith("wavelength_"):
                    selection = selection.split("_", 1)[-1]
                    img_path = Path(
                        f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}_{selection}.png"
                    )
            else:
                return None, True, False, False, False, True, False, None

            if os.path.exists(img_path):
                scale = "inferno" if selection == "_motility" else "gray"
                fig = create_figure_from_filepath(img_path, scale=scale)
                return (
                    fig,
                    False,
                    True,
                    False,
                    "",
                    False,
                    True,
                    f"```{img_path}```",
                )
        return None, True, False, False, False, True, False, None
    except Exception as e:
        return None, True, False, False, False, True, False, f"```{str(e)}```"


@callback(
    Output("input-path-output", "children"),
    Output("input-preview", "figure"),
    Input("submit-val", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
)
def update_preview_image(n_clicks, store):
    """
    This function updates the input preview image
    """
    # Obtaining the store data
    wells = store["wrmXpress_gui_obj"]["well_selection_list"]  # Get the wells
    first_well = wells[0].replace(", ", "")  # Get the first well
    platename = store["wrmXpress_gui_obj"]["plate_name"]  # Get the platename

    try:
        plate_base = platename.split("_", 1)[0]  # Get the plate base
    except Exception as e:
        return "```Please finish setting up the configuration```", {}

    volume = store["wrmXpress_gui_obj"]["mounted_volume"]  # Get the volume
    file_structure = store["wrmXpress_gui_obj"][
        "file_structure"
    ]  # Get the file structure

    # Check if the button has been clicked
    if n_clicks >= 1:
        if file_structure == "imagexpress":
            # assumes IX-like file structure
            img_path = Path(
                volume, f"{platename}/TimePoint_1/{plate_base}_{first_well}.TIF"
            )
            if os.path.exists(img_path):
                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)
                return f"```{img_path}```", fig  # Return the path and the figure

            else:  # checking for other file extensions
                img_path_s1 = Path(
                    volume, f"{platename}/TimePoint_1/{plate_base}_{first_well}_s1.TIF"
                )
                img_path_w1 = Path(
                    volume, f"{platename}/TimePoint_1/{plate_base}_{first_well}_w1.TIF"
                )
                if os.path.exists(img_path_s1):
                    # Open the image and create a figure
                    fig = create_figure_from_filepath(img_path_s1)
                    return f"```{img_path_s1}```", fig
                elif os.path.exists(img_path_w1):
                    # Open the image and create a figure
                    fig = create_figure_from_filepath(img_path_w1)
                    return f"```{img_path_w1}```", fig

        elif file_structure == "avi":
            # assumes AVI-like file structure
            img_path = Path(
                volume, "input", f"{platename}/TimePoint_1/{platename}_{first_well}.TIF"
            )

            # Should try and figure out an alternative to this
            # potential brick mechanism for the user
            while not os.path.exists(img_path):
                time.sleep(1)

            if os.path.exists(img_path):
                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)
                return f"```{img_path}```", fig

    # Default return if no conditions are met
    return "", {}


# @callback(
#     Output(
#         "preview-dropdown", "options"
#     ),  # update the option dropdown when the previous load is clicked
#     Input("submit-val", "n_clicks"),
#     State("store", "data"),
#     prevent_initial_call=True,
# )
# def get_options_preview(nclicks, store_data):
#     """
#     This function gets the options for the preview of the analysis.
#     """
#     # check to see if store exists
#     if not store_data:
#         return {}

#     # get the store from the data
#     wrmXpress_gui_obj = WrmXpressGui(
#         file_structure=store_data["wrmXpress_gui_obj"]["file_structure"],
#         imaging_mode=store_data["wrmXpress_gui_obj"]["imaging_mode"],
#         multi_well_row=store_data["wrmXpress_gui_obj"]["multi_well_row"],
#         multi_well_col=store_data["wrmXpress_gui_obj"]["multi_well_col"],
#         multi_well_detection=store_data["wrmXpress_gui_obj"]["multi_well_detection"],
#         x_sites=store_data["wrmXpress_gui_obj"]["x_sites"],
#         y_sites=store_data["wrmXpress_gui_obj"]["y_sites"],
#         stitch_switch=store_data["wrmXpress_gui_obj"]["stitch_switch"],
#         well_col=store_data["wrmXpress_gui_obj"]["well_col"],
#         well_row=store_data["wrmXpress_gui_obj"]["well_row"],
#         mask=store_data["wrmXpress_gui_obj"]["mask"],
#         mask_diameter=store_data["wrmXpress_gui_obj"]["mask_diameter"],
#         pipeline_selection=store_data["wrmXpress_gui_obj"]["pipeline_selection"],
#         wavelengths=store_data["wrmXpress_gui_obj"]["wavelengths"],
#         pyrscale=store_data["wrmXpress_gui_obj"]["pyrscale"],
#         levels=store_data["wrmXpress_gui_obj"]["levels"],
#         winsize=store_data["wrmXpress_gui_obj"]["winsize"],
#         iterations=store_data["wrmXpress_gui_obj"]["iterations"],
#         poly_n=store_data["wrmXpress_gui_obj"]["poly_n"],
#         poly_sigma=store_data["wrmXpress_gui_obj"]["poly_sigma"],
#         flags=store_data["wrmXpress_gui_obj"]["flags"],
#         cellpose_model_segmentation=store_data["wrmXpress_gui_obj"][
#             "cellpose_model_segmentation"
#         ],
#         cellpose_model_type_segmentation=store_data["wrmXpress_gui_obj"][
#             "cellpose_model_type_segmentation"
#         ],
#         python_model_sigma=store_data["wrmXpress_gui_obj"]["python_model_sigma"],
#         wavelengths_segmentation=store_data["wrmXpress_gui_obj"][
#             "wavelengths_segmentation"
#         ],
#         cellprofiler_pipeline_selection=store_data["wrmXpress_gui_obj"][
#             "cellprofiler_pipeline_selection"
#         ],
#         cellpose_model_cellprofiler=store_data["wrmXpress_gui_obj"][
#             "cellpose_model_cellprofiler"
#         ],
#         wavelengths_cellprofiler=store_data["wrmXpress_gui_obj"][
#             "wavelengths_cellprofiler"
#         ],
#         tracking_diameter=store_data["wrmXpress_gui_obj"]["tracking_diameter"],
#         tracking_minmass=store_data["wrmXpress_gui_obj"]["tracking_minmass"],
#         tracking_noisesize=store_data["wrmXpress_gui_obj"]["tracking_noisesize"],
#         tracking_searchrange=store_data["wrmXpress_gui_obj"]["tracking_searchrange"],
#         tracking_memory=store_data["wrmXpress_gui_obj"]["tracking_memory"],
#         tracking_adaptivestop=store_data["wrmXpress_gui_obj"]["tracking_adaptivestop"],
#         static_dx=store_data["wrmXpress_gui_obj"]["static_dx"],
#         static_dx_rescale=store_data["wrmXpress_gui_obj"]["static_dx_rescale"],
#         video_dx=store_data["wrmXpress_gui_obj"]["video_dx"],
#         video_dx_format=store_data["wrmXpress_gui_obj"]["video_dx_format"],
#         video_dx_rescale=store_data["wrmXpress_gui_obj"]["video_dx_rescale"],
#         mounted_volume=store_data["wrmXpress_gui_obj"]["mounted_volume"],
#         plate_name=store_data["wrmXpress_gui_obj"]["plate_name"],
#         well_selection_list=store_data["wrmXpress_gui_obj"]["well_selection_list"],
#     )

#     # get the pipeline selection
#     selection_dict = wrmXpress_gui_obj.get_image_diagnostic_parameters()

#     if nclicks is not None:
#         return selection_dict
#     else:
#         return {"raw": "raw"}


@callback(
    Output("analysis-preview-message", "children"),
    Output("analysis-preview", "figure"),
    Output("resolving-error-issue-preview", "is_open"),
    Output("resolving-error-issue-preview", "children"),
    # Output("preview-change-img-button", "disabled"),
    Input("submit-val", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
)
def run_analysis(
    nclicks,
    store_data,
):
    """
    This function runs the analysis of the first well if the first well has not been run before and the button has been clicked
    """
    try:
        
        # Check if the store is empty or has None values for essential elements
        if not store_data:
            return (
                "",
                {},
                True,
                ""
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
        
        error_occured, error_message, _, _ = wrmXpress_gui_obj.validate()
        if error_occured:
            print('error_occured', error_message)
            return (
                "",
                {},
                True,
                "",
            )

        # Check if the button has been clicked
        if nclicks:
            print('step 0')
            wrmXpress_gui_obj.analysis_setup("preview")

            return (
                wrmXpress_gui_obj.formatted_preview_first_well_path,
                wrmXpress_gui_obj.preview_first_well_figure,
                False,
                "",
            )
            # return preview_callback_functions(store_data)

    except Exception as e:
        return f"```{str(e)}```", {}, True, f"```{str(e)}```"
