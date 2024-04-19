########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
from dash import callback
from dash.dependencies import Input, Output, State
import time
from pathlib import Path
import os

# importing utils
from app.utils.callback_functions import create_figure_from_filepath
from app.utils.preview_callback_functions import preview_callback_functions
from app.components.preview_layout import preview_layout

dash.register_page(__name__)

# Assuming we have a fixed height for the headers and buttons in CSS
fixed_header_class = "fixed-header"
fixed_button_class = "fixed-button"

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

layout = preview_layout

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@callback(
    Output("analysis-preview-other-img", "figure"),
    Output("preview-img-view-alert", "is_open"),
    Output("post-analysis-first-well-img-view-alert", "is_open"),
    Output("no-store-data-alert", "is_open"),
    Output("submit-val", "disabled"),
    State("preview-dropdown", "value"),
    Input("preview-change-img-button", "n_clicks"),
    State("store", "data"),
)
def update_analysis_preview_imgage(selection, nclicks, store):
    """
    This function updates the analysis preview image based on the selection
    =======================================================================
    Arguments:
        - selection : str : The selection from the dropdown
        - nclicks : int : The number of times the button has been clicked
        - store : dict : The store data
    =======================================================================
    Returns:
        - fig : plotly.graph_objs._figure.Figure : The figure to be displayed
        - is_open : bool : Whether the (preview-imgage) alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - is_open : bool : Whether the (post analysis first well) alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - is_open : bool : Whether the (no store )alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - disabled : bool : Whether the button is disabled
            +- True : The button is disabled
            +- False : The button is enabled
    """
    # Check if store is empty
    if not store:
        return None, True, False, True, True

    # Get the store data
    volume = store["mount"]
    platename = store["platename"]
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    pipeline_selection = store["pipeline_selection"]

    if nclicks:  # If the button has been clicked

        if pipeline_selection == "motility":
            # assumes IX-like file structure
            if selection == "plate":
                selection = ""
            elif selection == "segment":
                selection = "_binary"
            else:
                selection = f"_{selection}"

            img_path = Path(
                f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection}.png"
            )

            # Check if the image exists
            if os.path.exists(img_path):

                # checking the selection and changing the scale accordingly
                if selection == "_motility":
                    scale = "inferno"
                else:
                    scale = "gray"

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path, scale=scale)

                # Return the figure and the open status of the alerts
                return fig, False, True, False, ""
        elif pipeline_selection == "fecundity":
            # assumes IX-like file structure
            if selection == "plate":
                selection = ""
            else:
                selection = f"_{selection}"

            img_path = Path(
                f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection}.png"
            )

            # Check if the image exists
            if os.path.exists(img_path):

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)

                # Return the figure and the open status of the alerts
                return fig, False, True, False, ""
        elif pipeline_selection == "tracking":
            # assumes IX-like file structure
            if selection == "plate":
                selection = ""
            else:
                selection = f"_{selection}"

            img_path = Path(
                f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}{selection}.png"
            )

            # Check if the image exists
            if os.path.exists(img_path):

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)

                # Return the figure and the open status of the alerts
                return fig, False, True, False, ""
        elif pipeline_selection == "wormsize_intensity_cellpose":

            # assumes IX-like file structure
            if selection == "plate":

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

            # Check if the image exists
            if os.path.exists(img_path):

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)

                # Return the figure and the open status of the alerts
                return fig, False, True, False, ""
        elif pipeline_selection == "mf_celltox":
            # assumes IX-like file structure
            if selection == "plate":

                img_path = Path(
                    f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
                )

            # Check if the image exists
            if os.path.exists(img_path):

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)

                # Return the figure and the open status of the alerts
                return fig, False, True, False, ""
        elif pipeline_selection == "wormsize":
            # assumes IX-like file structure
            if selection == "plate":

                img_path = Path(
                    f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
                )

            elif selection == "straightened_worms":

                img_path = Path(
                    f"{volume}/output/straightened_worms/{plate_base}_{wells[0]}.tiff"
                )

            # Check if the image exists
            if os.path.exists(img_path):

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)

                # Return the figure and the open status of the alerts
                return fig, False, True, False, ""
        elif pipeline_selection == "feeding":
            # assumes IX-like file structure
            if selection == "plate":

                img_path = Path(
                    f"{volume}/work/{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
                )

            elif selection == "straightened_worms":

                img_path = Path(
                    f"{volume}/output/straightened_worms/{plate_base}_{wells[0]}.tiff"
                )

            elif selection.startswith("wavelength_"):

                print("selection", selection)
                selection = selection.split("_", 1)[-1]

                img_path = Path(
                    f"{volume}/output/thumbs/{platename}_{wells[0]}_{selection}.png"
                )

            # Check if the image exists
            if os.path.exists(img_path):

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)

                # Return the figure and the open status of the alerts
                return fig, False, True, False, ""
        else:
            return None, True, False, False, False
    return None, True, False, False, False


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
    =======================================================
    Arguments:
        - n_clicks : int : The number of times the button has been clicked
        - store : dict : The store data
    =======================================================
    Returns:
        - str : The path to the image
        - fig : plotly.graph_objs._figure.Figure : The figure to be displayed
    """
    # Obtaining the store data
    wells = store["wells"]  # Get the wells
    first_well = wells[0].replace(", ", "")  # Get the first well
    platename = store["platename"]  # Get the platename
    plate_base = platename.split("_", 1)[0]  # Get the plate base
    volume = store["mount"]  # Get the volume
    file_structure = store["file_structure"]  # Get the file structure

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
            while not os.path.exists(img_path):
                time.sleep(1)
            if os.path.exists(img_path):
                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)
                return f"```{img_path}```", fig


@callback(
    Output(
        "preview-dropdown", "options"
    ),  # update the option dropdown when the previous load is clicked
    Input("submit-val", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
)
def get_options_preview(nclicks, store):
    """
    This function gets the options for the preview of the analysis.
    =========================================================================================
    Arguments:
        - nclicks : int : The number of clicks
        - store : dict : The store data
    =========================================================================================
    Returns:
        - options : list : The options
    """
    # check to see if store exists
    if not store:
        return {}
    # get the store from the data
    pipeline_selection = store["pipeline_selection"]
    if pipeline_selection == "motility":

        # create the options
        selection_dict = {
            "motility": "motility",
            "segment": "binary",
            "blur": "blur",
            "edge": "edge",
            "plate": "plate",
        }

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict  # return the option dictionary
    elif pipeline_selection == "fecundity":

        # create the options
        selection_dict = {
            "binary": "binary",
            "blur": "blur",
            "edge": "edge",
            "plate": "plate",
        }

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == "tracking":

        # create the options
        selection_dict = {"tracks": "tracks", "plate": "plate"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == "wormsize_intensity_cellpose":

        # create the options
        selection_dict = {
            "plate": "plate",
            "straightened_worms": "straightened_worms",
            "cp_masks": "cp_masks",
        }

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == "mf_celltox":

        # create the options
        selection_dict = {"plate": "plate"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == "wormsize":
        # create the options
        selection_dict = {"plate": "plate", "straightened_worms": "straightened_worms"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == "feeding":
        # obtain the wavelength options
        volume = store["mount"]
        platename = store["platename"]
        plate_base = platename.split("_", 1)[0]
        input_file_path = Path(volume, f"{platename}/TimePoint_1/")

        # create the options
        selection_dict = {
            "straightened_worms": "straightened_worms",
        }

        # New code to add: list all matching files and extract unique identifiers
        pattern = f"{plate_base}*.TIF"
        # Using glob to match the pattern
        all_files = list(input_file_path.glob(pattern))
        # Extracting unique identifiers from filenames (e.g., _w1, _w2, etc.)
        wavelengths = set()
        for file_path in all_files:
            parts = file_path.name.split("_")
            if (
                len(parts) > 1
                and parts[-1].startswith("w")
                and parts[-1].endswith(".TIF")
            ):
                wavelengths.add(parts[-1].replace(".TIF", ""))

        # Adding these wavelengths to the selection dictionary
        for wave in sorted(wavelengths):
            selection_key = f"wavelength_{wave}"  # Format the key as you see fit
            selection_dict[selection_key] = wave

        # Assuming nclicks is some condition you've checked elsewhere
        nclicks = 1
        if nclicks is not None:
            return selection_dict
    else:
        return {"plate": "plate"}


@callback(
    Output("analysis-preview-message", "children"),
    Output("analysis-preview", "figure"),
    Output("resolving-error-issue-preview", "is_open"),
    Output("resolving-error-issue-preview", "children"),
    Output("preview-change-img-button", "disabled"),
    Input("submit-val", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
)
def run_analysis(
    nclicks,
    store,
):
    """
    This function runs the analysis of the first well if the first well has not been run before and the button has been clicked
    =======================================================
    Arguments:
        - nclicks : int : The number of times the button has been clicked
        - store : dict : The store data
    =======================================================
    Returns:
        - str : The command message
        - fig : plotly.graph_objs._figure.Figure : The figure to be displayed
        - is_open : bool : Whether the alert is open
            +- True : The alert is open
            +- False : The alert is closed
        - str : The message to be displayed
        - disabled : bool : Whether the button is disabled
            +- True : The button is disabled
            +- False : The button is enabled
    """
    # Check if the button has been clicked
    if nclicks:

        return preview_callback_functions(store)
