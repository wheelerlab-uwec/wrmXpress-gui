########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
from dash import callback, html, Input, Output, State, dash_table
import itertools
import yaml
from pathlib import Path
import os
import dash_bootstrap_components as dbc

# Importing Components and functions
from app.utils.callback_functions import create_df_from_inputs, prep_yaml
from app.components.configure_layout import configure_layout
from app.utils.wrmxpress_gui_obj import WrmXpressGui

# Registering this page
dash.register_page(__name__)

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

layout = configure_layout

########################################################################
####                                                                ####
####                              Callback                          ####
####                                                                ####
########################################################################


@callback(
    [
        Output("multi-well-options-row", "style"),
        Output("additional-options-row", "style"),
        Output("multi-site-options-row", "style"),
        Output("mask-options-row", "style"),
        Output("static-dx-rescale", "style"),
        Output("video-dx-options", "style"),
        Output("python-model-sigma-row", "style"),
    ],
    [
        Input("imaging-mode", "value"),
        Input("file-structure", "value"),
        Input("mask", "value"),
        Input("static-dx", "value"),
        Input("video-dx", "value"),
        Input("cellpose-model-type-segmentation", "value"),
    ],
)
# appearing selections upon meeting certain critera
def update_options_visibility(imaging_mode, file_structure, mask, static_dx, video_dx, cellprofiler_pipeline_selection):
    """
    This function will display the multi-well options and additional options based on the imaging mode and file structure selected.
    """
    multi_well_options_style = {"display": "none"}
    additional_options_style = {"display": "none"}
    multi_site_options_style = {"display": "none"}
    mask_options_style = {"display": "none"}
    static_dx_options_style = {"display": "none"}
    video_dx_options_style = {"display": "none"}
    python_model_sigma_row = {"display": "none"}

    if imaging_mode == "multi-well":  # if multi-well is selected
        # display the multi-well options
        multi_well_options_style = {"display": "flex"}
        additional_options_style = {"display": "flex"}

        # if file_structure == "avi":  # if avi is selected
        #     # display the additional options
        #     additional_options_style = {"display": "flex"}

    elif imaging_mode == "multi-site":
        multi_site_options_style = {"display": "flex"}

    if mask == "circular" or mask == "square":
        mask_options_style = {"display": "flex"}

    if static_dx:
        static_dx_options_style = {"display": "flex"}

    if video_dx:
        video_dx_options_style = {"display": "flex"}

    if cellprofiler_pipeline_selection == "python":
        python_model_sigma_row = {"display": "flex"}

    return (
        multi_well_options_style,
        additional_options_style,
        multi_site_options_style,
        mask_options_style,
        static_dx_options_style,
        video_dx_options_style,
        python_model_sigma_row,
    )  # return the styles


@callback( 
    Output("pipeline-params-header", "style"),
    Output("motility_params", "style"),
    Output("segmentation_params", "style"),
    Output("cellprofile_params", "style"),
    Output("tracking_params", "style"),
    Input("pipeline-selection", "value"),
)
def update_params_visibility(pipeline):
    """ This function will display the parameters based on the pipeline selected.
    """
    if pipeline == "motility":
        return {"display": "flex"}, {"display": "flex"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif pipeline == "segmentation":
        return {"display": "flex"}, {"display": "none"}, {"display": "flex"}, {"display": "none"}, {"display": "none"}
    elif pipeline == "cellprofile":
        return {"display": "flex"}, {"display": "none"}, {"display": "none"}, {"display": "flex"}, {"display": "none"}
    elif pipeline == "tracking":
        return {"display": "flex"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "flex"}
    else:
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

@callback(
    Output("store", "data"),
    Input("file-structure", "value"),
    Input("imaging-mode", "value"),
    Input("multi-well-row", "value"),
    Input("multi-well-col", "value"),
    Input("multi-well-detection", "value"),
    Input("x-sites", "value"),
    Input("y-sites", "value"),
    Input("stitch-switch", "value"),
    Input("well-col", "value"),
    Input("well-row", "value"),
    Input("mask", "value"),
    Input("mask-diameter", "value"),
    Input("pipeline-selection", "value"),
    Input("wavelengths", "value"),
    Input("pyrscale", "value"),
    Input("levels", "value"),
    Input("winsize", "value"),
    Input("iterations", "value"),
    Input("poly_n", "value"),
    Input("poly_sigma", "value"),
    Input("flags", "value"),
    Input("cellpose-model-segmentation", "value"),
    Input("cellpose-model-type-segmentation", "value"),
    Input("python-model-sigma", "value"),
    Input("wavelengths-segmentation", "value"),
    Input("cellprofiler-pipeline-selection", "value"),
    Input("cellpose-model-cellprofile", "value"),
    Input("wavelengths-cellprofile", "value"),
    Input("tracking-diameter", "value"),
    Input("tracking-minmass", "value"),
    Input("tracking-noisesize", "value"),
    Input("tracking-searchrange", "value"),
    Input("tracking-memory", "value"),
    Input("tracking-adaptivestop", "value"),
    Input("static-dx", "value"),
    Input("static-dx-rescale-input", "value"),
    Input("video-dx", "value"),
    Input("video-dx-format", "value"),
    Input("video-dx-rescale", "value"),
    Input("mounted-volume", "value"),
    Input("plate-name", "value"),
    Input("well-selection-list", "children"),
    prevent_initial_call=True,
)
def store_values(
    file_structure,
    imaging_mode,
    multi_well_row,
    multi_well_col,
    multi_well_detection,
    x_sites,
    y_sites,
    stitch_switch,
    well_col,
    well_row,
    mask,
    mask_diameter,
    pipeline_selection,
    wavelengths,
    pyrscale,
    levels,
    winsize,
    iterations,
    poly_n,
    poly_sigma,
    flags,
    cellpose_model_segmentation,
    cellpose_model_type_segmentation,
    python_model_sigma,
    wavelengths_segmentation,
    cellprofiler_pipeline_selection,
    cellpose_model_cellprofile,
    wavelengths_cellprofile,
    tracking_diameter,
    tracking_minmass,
    tracking_noisesize,
    tracking_searchrange,
    tracking_memory,
    tracking_adaptivestop,
    static_dx,
    static_dx_rescale,
    video_dx,
    video_dx_format,
    video_dx_rescale,
    mounted_volume,
    plate_name,
    well_selection_list,
):
    """
    This function will store the wrmXpress gui object for the rest of the application.
    """
    wrmXpress_gui_obj = WrmXpressGui(
        file_structure,
        imaging_mode,
        multi_well_row,
        multi_well_col,
        multi_well_detection,
        x_sites,
        y_sites,
        stitch_switch,
        well_col,
        well_row,
        mask,
        mask_diameter,
        pipeline_selection,
        wavelengths,
        pyrscale,
        levels,
        winsize,
        iterations,
        poly_n,
        poly_sigma,
        flags,
        cellpose_model_segmentation,
        cellpose_model_type_segmentation,
        python_model_sigma,
        wavelengths_segmentation,
        cellprofiler_pipeline_selection,
        cellpose_model_cellprofile,
        wavelengths_cellprofile,
        tracking_diameter,
        tracking_minmass,
        tracking_noisesize,
        tracking_searchrange,
        tracking_memory,
        tracking_adaptivestop,
        static_dx,
        static_dx_rescale,
        video_dx,
        video_dx_format,
        video_dx_rescale,
        mounted_volume,
        plate_name,
        well_selection_list,
    )

    serialized_obj = wrmXpress_gui_obj.to_dict()

    return {
        "cols": well_col,
        "rows": well_row,
        "mount": mounted_volume,
        "platename": plate_name,
        "wells": well_selection_list,
        "img_mode": imaging_mode,
        "file_structure": file_structure,
        "pipeline_selection": pipeline_selection,
        "wrmXpress_gui_obj": serialized_obj
    }


@callback(
    Output("well-selection-table", "children"),
    [Input("well-row", "value"), Input("well-col", "value")],
)
# creating a selection table based on the dimensions of rows and columns selected
def update_table(rows, cols):
    """
    This function will create a selection table based on the dimensions of rows and columns selected.
    """
    # default values for rows and columns
    default_cols = 12
    default_rows = 8
    if rows is None:  # if rows is not selected
        rows = default_rows
    if cols is None:  # if cols is not selected
        cols = default_cols

    # create a dataframe from the inputs, see callback_functions.py
    df = create_df_from_inputs(rows, cols)

    # create a table from the dataframe
    well_selection = dash_table.DataTable(
        data=df.reset_index().to_dict("records"),
        columns=[{"name": "Row", "id": "index", "editable": False}]
        + [{"name": col, "id": col} for col in df.columns],
        editable=True,  # table is editable
        style_table={"overflowX": "auto"},  # table style
        style_cell={"textAlign": "center"},  # cell style
        id="dynamic-table-container-well-selection-table",
    )
    return well_selection  # return the table


@callback(
    Output("well-selection-list", "children"),
    Input("dynamic-table-container-well-selection-table", "data"),
)
# updating the list of wells to be analyzed
def update_wells(table_contents):  # list of cells from selection table
    """
    This function will populate the list of wells to be analyzed.
    """
    values_list = [list(d.values()) for d in table_contents]
    flattened_list = list(itertools.chain.from_iterable(values_list))
    filtered_list = []
    for item in flattened_list:  # remove empty cells
        if item is None:
            continue
        elif len(item) == 1:  # remove single character cells
            continue
        else:
            filtered_list.append(item)  # append the item to the filtered list

    sorted_list = sorted(filtered_list)  # sort the list
    return sorted_list  # return the sorted list


@callback(
    [
        Output("finalize-configure-button", "color"),
        Output("resolving-error-issue-configure", "is_open"),
        Output("resolving-error-issue-configure", "children"),
        Output("resolving-error-issue-configure", "color"),
    ],
    Input("finalize-configure-button", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
    allow_duplicate=True,
)
# saving the yaml file from the sections in the configuration page
def save_configuration_upon_clicking_finalize_button(  # function to save the yaml file from the sections in the configuration page
    nclicks,
    store_data,
):

    if nclicks:

        # try to catch any errors that may occur
        # return an error message if an error occurs
        # try: will include something here later
        try:
            # initializing the first error message
            error_messages = [
                "While finalizing the configuration, the following errors were found:"
            ]
            minor_error_messages = [
                "Warning: when finalizing the configuration, the following values were not set. The default will be used."
            ]

            error_occured = False  # initializing the error flag
            minor_error_occured = False  # initializing the minor error flag

            # checks volume and plate names to ensure they are adequately named
            check_cases = [None, "", " "]

            if store_data["wrmXpress_gui_obj"]["imaging_mode"] == "multi-well":
                rows_missing = (
                    store_data["wrmXpress_gui_obj"]["multi_well_row"] is None 
                    or store_data["wrmXpress_gui_obj"]["multi_well_row"] == ""
                )
                cols_missing = (
                    store_data["wrmXpress_gui_obj"]["multi_well_col"] is None 
                    or store_data["wrmXpress_gui_obj"]["multi_well_col"] == ""
                )

                if rows_missing and cols_missing:
                    error_occured = True
                    error_messages.append(
                        "Both the number of rows and columns for the multi-well plate are missing."
                    )
                elif rows_missing:
                    error_occured = True
                    error_messages.append("The number of rows for the multi-well plate is missing.")
                elif cols_missing:
                    error_occured = True
                    error_messages.append("The number of columns for the multi-well plate is missing.")

            if store_data["wrmXpress_gui_obj"]["imaging_mode"] == "multi-site":
                missing_x_sites = (
                    store_data["wrmXpress_gui_obj"]["x_sites"] is None 
                    or store_data["wrmXpress_gui_obj"]["x_sites"] == ""
                )

                missing_y_sites = (
                    store_data["wrmXpress_gui_obj"]["y_sites"] is None 
                    or store_data["wrmXpress_gui_obj"]["y_sites"] == ""
                )

                if missing_x_sites and missing_y_sites:
                    error_occured = True
                    error_messages.append(
                        "Both the number of x and y sites for the multi-site plate are missing."
                    )

                elif missing_x_sites:
                    error_occured = True
                    error_messages.append("The number of x sites for the multi-site plate is missing.")

                elif missing_y_sites:
                    error_occured = True
                    error_messages.append("The number of y sites for the multi-site plate is missing.")

            # check mask diameter
            if store_data["wrmXpress_gui_obj"]["mask"] in ["circular", "square"]:
                if store_data["wrmXpress_gui_obj"]["mask_diameter"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Mask diameter is missing. Default value (0) will be used.")

            # check if the pipeline is selected
            if store_data["wrmXpress_gui_obj"]["pipeline_selection"] is None:
                error_occured = True
                error_messages.append("No pipeline selected.")

            # check platename
            if store_data["wrmXpress_gui_obj"]["plate_name"] in check_cases:
                error_occured = True
                error_messages.append("Plate/Folder name is missing.")

            # check mounted volume
            if store_data["wrmXpress_gui_obj"]["mounted_volume"] in check_cases:
                error_occured = True
                error_messages.append("Volume path is missing.")

            # check to see if the well selection list is empty
            if store_data["wrmXpress_gui_obj"]["well_selection_list"] == []:
                error_occured = True
                error_messages.append("No wells selected.")

            # minor error messages if parameters for motility are missing
            if store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "motility":
                if store_data["wrmXpress_gui_obj"]["pyrscale"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Pyrscale is missing. Default value (0.5) will be used.")
                if store_data["wrmXpress_gui_obj"]["levels"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Levels is missing. Default value (5) will be used.")
                if store_data["wrmXpress_gui_obj"]["winsize"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Winsize is missing. Default value (20) will be used.")
                if store_data["wrmXpress_gui_obj"]["iterations"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Iterations is missing. Default value (7) will be used.")
                if store_data["wrmXpress_gui_obj"]["poly_n"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Poly_n is missing. Default value (5) will be used.")
                if store_data["wrmXpress_gui_obj"]["poly_sigma"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Poly_sigma is missing. Default value (1.1) will be used.")
                if store_data["wrmXpress_gui_obj"]["flags"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Flags is missing. Default value (0) will be used.")

            # minor error messages if parameters for segmentation are missing
            if store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "segmentation":
                if store_data["wrmXpress_gui_obj"]["cellpose_model_type_segmentation"] == "python":
                    if store_data["wrmXpress_gui_obj"]["python_model_sigma"] is None:
                        minor_error_occured = True
                        minor_error_messages.append("Python model sigma is missing. Default value (0.25) will be used.")

            # minor error messages if parameters for tracking are missing
            if store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "tracking":
                if store_data["wrmXpress_gui_obj"]["tracking_diameter"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Tracking diameter is missing. Default value (35) will be used.")
                if store_data["wrmXpress_gui_obj"]["tracking_minmass"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Tracking minmass is missing. Default value (1200) will be used.")
                if store_data["wrmXpress_gui_obj"]["tracking_noisesize"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Tracking noisesize is missing. Default value (2) will be used.")
                if store_data["wrmXpress_gui_obj"]["tracking_searchrange"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Tracking searchrange is missing. Default value (45) will be used.")
                if store_data["wrmXpress_gui_obj"]["tracking_memory"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Tracking memory is missing. Default value (25) will be used.")
                if store_data["wrmXpress_gui_obj"]["tracking_adaptivestop"] is None:
                    minor_error_occured = True
                    minor_error_messages.append("Tracking adaptivestop is missing. Default value (30) will be used.")

            # avi should only be selected for motility and tracking
            if store_data["wrmXpress_gui_obj"]["file_structure"] == "avi" and store_data["wrmXpress_gui_obj"]["pipeline_selection"] not in ["motility", "tracking"]:
                error_occured = True
                error_messages.append("AVI mode is not supported for the selected pipeline.")

            # check to see if the volume path and plate name are valid
            if store_data["wrmXpress_gui_obj"]["mounted_volume"] not in check_cases:

                # ensure that the volume path exists
                if not os.path.exists(
                    store_data["wrmXpress_gui_obj"]["mounted_volume"]
                ):
                    error_occured = True
                    error_messages.append("The volume path does not exist.")

                if store_data["wrmXpress_gui_obj"]["plate_name"] not in check_cases:
                    # ensure that the plate name path exists and lives in the volume path
                    platename_path = Path(
                        store_data["wrmXpress_gui_obj"]["mounted_volume"],
                        store_data["wrmXpress_gui_obj"]["plate_name"],
                    )
                    if not os.path.exists(platename_path):
                        error_occured = True
                        error_messages.append("No Plate/Folder in the volume.")

                    # if imagexpress mode is selected, ensure that an .htd file exists
                    if (
                        store_data["wrmXpress_gui_obj"]["file_structure"]
                        == "imagexpress"
                    ):
                        # Define the directory to search
                        platename_path = Path(platename_path)

                        # Search for .htd and .HTD files
                        htd_files = list(platename_path.glob("*.htd"))
                        HTD_files = list(platename_path.glob("*.HTD"))

                        # Check if no matching files exist
                        if not htd_files and not HTD_files:
                            error_occured = True
                            error_messages.append("No .HTD file found in the Plate/Folder.")

                        # get a list of all subdirectories in the plate/folder
                        subdirectories = [
                            x for x in platename_path.iterdir()
                            if x.is_dir()
                        ]

                        for subdirectory in subdirectories:
                            # get a list of all files in the subdirectory
                            files = list(subdirectory.glob("*"))

                            # check if the str(well) is in the list of files
                            # if not, set error flags
                            for well in store_data["wrmXpress_gui_obj"]["well_selection_list"]:
                                if not any([str(well) in str(file) for file in files]):
                                    error_occured = True
                                    error_messages.append(
                                        f"No images found for well {well}. This may result in unexpected errors or results."
                                    )

                    # if avi mode is selected, ensure that an avi file exists
                    if store_data["wrmXpress_gui_obj"]["file_structure"] == "avi":
                        avi_folder_path = Path(
                            store_data["wrmXpress_gui_obj"]["mounted_volume"],
                            store_data["wrmXpress_gui_obj"]["plate_name"],
                        )
                        avi_pattern = (
                            f"{store_data['wrmXpress_gui_obj']['plate_name']}_"
                        )
                        matched_files_avi = list(
                            avi_folder_path.glob(avi_pattern + "*.avi")
                        )
                        if not matched_files_avi:
                            error_occured = True
                            error_messages.append(
                                "No AVI files found in the Plate/Folder."
                            )

                        # check to see if all wells selected have an associated .avi file
                        for well in store_data["wrmXpress_gui_obj"]["well_selection_list"]:
                            # Construct a pattern to match files for the current well, ignoring suffixes
                            pattern = f"{store_data['wrmXpress_gui_obj']['plate_name']}_{well}"
                            # Find all files in the directory that match the well pattern
                            matched_files = list(avi_folder_path.glob(pattern + "*.avi"))
                            # If no files match the current well, set error flags
                            if not matched_files:
                                error_occured = True
                                error_messages.append(
                                    f"No images found for well {well}. This may result in unexpected errors or results."
                                )

            # check to see if there was an error message
            if error_occured == True:

                # formats the first line of the error message
                error_messages[0] = html.H5(
                    f"{error_messages[0]}", className="alert-heading"
                )

                # format the content of the error messages
                for i in range(1, len(error_messages)):
                    error_messages[i] = html.P(
                        f"{i}. {error_messages[i]}", className="mb-0"
                    )

                # return the error messages
                return "danger", True, error_messages, "danger"

        # additional error messages that we have not accounted for
        except ValueError:
            return "danger", True, "A ValueError occurred", "danger"
        except Exception as e:
            return "danger", True, f"An unexpected error occurred: {str(e)}", "danger"

        # diagnosticdx = "True"  # set diagnosticdx to True

        # if no error messages are found, write the configuration to a YAML file
        config = prep_yaml(
            store_data
            )

        output_file = Path(store_data['wrmXpress_gui_obj']['mounted_volume'], store_data['wrmXpress_gui_obj']['plate_name'] + ".yml")

        # dump preview data to YAML file
        with open(output_file, "w") as yaml_file:
            yaml.dump(config, yaml_file, default_flow_style=False)

        if minor_error_occured == True:
            # formats the first line of the error message
            minor_error_messages[0] = html.H5(
                f"{minor_error_messages[0]}", className="alert-heading"
            )

            # format the content of the error messages
            for i in range(1, len(minor_error_messages)):
                minor_error_messages[i] = html.P(
                    f"{i}. {minor_error_messages[i]}", className="mb-0"
                )

            return "warning", True, minor_error_messages, "warning"

        # return success message
        return "success", True, f"Configuration written to {output_file}", "success"


@callback(
    Output("configure-input-preview", "src"),
    Output("configure-input-preview", "style"),
    Output("configure-input-text", "children"),
    Input("pipeline-selection", "value"),
    Input("cellprofiler-pipeline-selection", "value"),
    prevent_initial_call=True,  # Preventing callback from running before any action is taken
)
# updating the image preview based on the selected pipeline
def update_figure_based_on_selection(module_initial, cellprofiler_pipeline_selection):
    """
    This function will load the image module for the selected pipeline.
    """

    if module_initial == "motility":
        fig = "assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01_motility.png"
        return (
            fig,
            {"width": "40%"},
            'The motility pipeline exports a "flow cloud" as a diagnostic and saves a single value as output.',
        )

    elif module_initial == "segmentation":
        fig = "assets/configure_assets/fecundity/A01/img/20210906-p01-NJW_857_A01_binary.png"
        return (
            fig,
            {"width": "40%"},
            "The fecundity pipeline exports a segmented image as a diagnostic and saves a single value as output.",
        )

    elif module_initial == "tracking":
        fig = "assets/configure_assets/tracking/20240307-p01-RVH_A05_tracks.png"
        return (
            fig,
            {"width": "40%"},
            "The tracking pipeline exports tracks as a diagnostic and saves a single value per track as output.",
        )

    elif module_initial == "cellprofile":
        if cellprofiler_pipeline_selection == "wormsize_intensity_cellpose":
            fig = "assets/configure_assets/wormsize_intensity_cellpose/A01/img/20220408-p01-MGC_A01.png"
            return (
                fig,
                {"width": "100%"},
                "The wormsize/intensity (Cellpose) pipeline exports straightened worms as a diagnostic and saves many values per worm as output.",
            )

        elif cellprofiler_pipeline_selection == "mf_celltox":
            fig = "assets/configure_assets/mf_celltox/viability.png"
            return (
                fig,
                {"width": "40%"},
                "The viability pipeline exports a segmented image as a diagnostic and saves a single value as output.",
            )

        elif cellprofiler_pipeline_selection == "feeding":
            fig = "assets/configure_assets/feeding/A01/img/20210823-p01-KJG_795_A01.png"
            return (
                fig,
                {"width": "100%"},
                "The feeding pipeline exports straightened worms (with fluorescence) as a diagnostic and saves many values per worm as output.",
            )

        elif cellprofiler_pipeline_selection == "wormsize":
            fig = "assets/configure_assets/wormsize/A01/img/straightened.png"
            return (
                fig,
                {"width": "60%"},
                "The wormsize pipeline exports straightened worms as a diagnostic and saves many values per worm as output.",
            )
