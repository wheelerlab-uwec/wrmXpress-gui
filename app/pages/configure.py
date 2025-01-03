# In[1]: Imports

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

# In[2]: Configure Page Layout

layout = configure_layout

# In[3]: Callbacks


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
        # Input("file-structure", "value"),
        Input("mask", "value"),
        Input("static-dx", "value"),
        Input("video-dx", "value"),
        Input("cellpose-model-type-segmentation", "value"),
    ],
)
# appearing selections upon meeting certain critera
def update_options_visibility(
    imaging_mode,
    # file_structure,
    mask,
    static_dx,
    video_dx,
    cellprofiler_pipeline_selection,
):
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
    Output("cellprofiler_params", "style"),
    Output("tracking_params", "style"),
    Input("pipeline-selection", "value"),
)
def update_params_visibility(pipeline):
    """This function will display the parameters based on the pipeline selected."""
    if pipeline == "motility":
        return (
            {"display": "flex"},
            {"display": "flex"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        )
    elif pipeline == "segmentation":
        return (
            {"display": "flex"},
            {"display": "none"},
            {"display": "flex"},
            {"display": "none"},
            {"display": "none"},
        )
    elif pipeline == "cellprofiler":
        return (
            {"display": "flex"},
            {"display": "none"},
            {"display": "none"},
            {"display": "flex"},
            {"display": "none"},
        )
    elif pipeline == "tracking":
        return (
            {"display": "flex"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "flex"},
        )
    else:
        return (
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        )


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
    Input("cellpose-model-cellprofiler", "value"),
    Input("wavelengths-cellprofiler", "value"),
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
    cellpose_model_cellprofiler,
    wavelengths_cellprofiler,
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
        cellpose_model_cellprofiler,
        wavelengths_cellprofiler,
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
        "wrmXpress_gui_obj": serialized_obj,
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
            initial_error_messages = [
                "While finalizing the configuration, the following errors were found:"
            ]
            initial_minor_error_messages = [
                "Warning: when finalizing the configuration, the following values were not set. The default will be used."
            ]

            # create a wrmXpress gui object from the stored data and use the validate method to check for errors

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
                pipeline_selection=store_data["wrmXpress_gui_obj"][
                    "pipeline_selection"
                ],
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
                python_model_sigma=store_data["wrmXpress_gui_obj"][
                    "python_model_sigma"
                ],
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
                tracking_noisesize=store_data["wrmXpress_gui_obj"][
                    "tracking_noisesize"
                ],
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
                well_selection_list=store_data["wrmXpress_gui_obj"][
                    "well_selection_list"
                ],
            )

            error_occured, error_messages, warning_occured, warning_messages = (
                wrmXpress_gui_obj.validate()
            )

            # check to see if there was an error message
            if error_occured == True:

                # add error messages to the initial error messages
                error_messages = initial_error_messages + error_messages

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
        # config = prep_yaml(
        #     store_data
        #     )

        config = wrmXpress_gui_obj.prep_yml()

        output_file = Path(
            store_data["wrmXpress_gui_obj"]["mounted_volume"],
            store_data["wrmXpress_gui_obj"]["plate_name"] + ".yml",
        )

        # dump preview data to YAML file
        with open(output_file, "w") as yaml_file:
            yaml.dump(config, yaml_file, default_flow_style=False)

        if warning_occured == True:

            # add error messages to the initial error messages
            warning_messages = initial_minor_error_messages + warning_messages

            # formats the first line of the error message
            warning_messages[0] = html.H5(
                f"{warning_messages[0]}", className="alert-heading"
            )

            # format the content of the error messages
            for i in range(1, len(warning_messages)):
                warning_messages[i] = html.P(
                    f"{i}. {warning_messages[i]}", className="mb-0"
                )

            return "warning", True, warning_messages, "warning"

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

    elif module_initial == "cellprofiler":
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
