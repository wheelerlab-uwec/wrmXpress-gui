########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

from dash import callback
from dash.dependencies import Input, Output, State
from pathlib import Path
import os
import dash
from dash.long_callback import DiskcacheLongCallbackManager

# importing utils
from app.utils.callback_functions import send_ctrl_c, create_figure_from_filepath
from app.components.run_layout import run_layout

# Diskcache
import diskcache

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

dash.register_page(__name__, long_callback_manager=long_callback_manager)

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

layout = run_layout

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@callback(Output("cancel-analysis", "n_clicks"), Input("cancel-analysis", "n_clicks"))
def cancel_analysis(n_clicks):
    """
    This function cancels the analysis by typing "Control" + "C" in the terminal.
    =========================================================================================
    Arguments:
        - n_clicks : int : The number of clicks
    =========================================================================================
    Returns:
        - n_clicks : int : The number of clicks
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
def load_analysis_img(selection, n_clicks, store):
    """
    This function loads the analysis image based on the selection.
    =========================================================================================
    Arguments:
        - selection : str : The selection
        - n_clicks : int : The number of clicks
        - store : dict : The store data
    =========================================================================================
    Returns:
        - fig : plotly.graph_objs._figure.Figure : The figure
        - f'```{output_thumbs_path}```' : str : The output thumbs path
        - is_open : bool : whether the (first-view-of-analysis) alert is open or not
            +- True : if the alert is open
            +- False : if the alert is not open
        - is_open : bool : whether the (additional view of analysis) alert is open or not
            +- True : if the alert is open
            +- False : if the alert is not open
    """
    # Check to see if store exists
    if not store:
        return {}, "", True, False, True, True, True, False

    try:
        # Get the store data
        volume = store["mount"]
        platename = store["platename"]

        # Handle NoneType for platename
        if platename is None:
            return {}, "", True, False, True, True, True, False

        plate_base = platename.split("_", 1)[0]
        wells = store["wells"]

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


@callback(
    Output("analysis-dropdown", "options"),
    # update the option dropdown when the run analysis is clicked
    Input("submit-analysis", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
    allow_duplicate=True,
)
def get_options_analysis(nclicks, store):
    """
    This function gets the options for the analysis.
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
        selection_dict = {"motility": "motility", "segment": "binary", "raw": "raw"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict  # return the option dictionary

    elif pipeline_selection == "fecundity":

        # create the options
        selection_dict = {"binary": "binary", "raw": "raw"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict

    elif pipeline_selection == "tracking":

        # create the options
        selection_dict = {"tracks": "tracks", "raw": "raw"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict

    elif pipeline_selection == "wormsize_intensity_cellpose":

        # create the options
        selection_dict = {"raw": "raw", "straightened_worms": "straightened_worms"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict

    elif pipeline_selection == "mf_celltox":

        # create the options
        selection_dict = {"raw": "raw"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict

    elif pipeline_selection == "wormsize":
        # create the options
        selection_dict = {"raw": "raw", "straightened_worms": "straightened_worms"}

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
        return {"raw": "raw"}
