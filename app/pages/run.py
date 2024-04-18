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
    [
        Output("analysis-postview", "figure"),
        Output("analysis-postview-message", "children"),
        Output("first-view-of-analysis-alert", "is_open"),
        Output("additional-view-of-analysis-alert", "is_open"),
    ],
    State("analysis-dropdown", "value"),
    Input("load-analysis-img", "n_clicks"),
    State("store", "data"),
    allow_duplicate=True,
    prevent_initial_call=True,
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
        - is_open : bool : weather the (first-view-of-analysis) alert is open or not
            +- True : if the alert is open
            +- False : if the alert is not open
        - is_open : bool : weather the (additional view of analysis) alert is open or not
            +- True : if the alert is open
            +- False : if the alert is not open
    """
    # check to see if store exists
    if not store:
        return None, None, False, False

    # get the store from the data
    volume = store["mount"]
    platename = store["platename"]
    plate_base = platename.split("_", 1)[0]
    wells = store["wells"]

    img_path = None
    scale = "gray"
    # check to see if selection option exists in output thumbs folder
    if n_clicks:

        if selection == "straightened_worms":
            img_path = Path(
                volume, f"output/strightened_worms/{plate_base}_{wells[0]}.tiff"
            )

        elif selection == "motility":
            selection = "_motility"
            scale = "inferno"
            img_path = Path(volume, f"output/thumbs/{platename}{selection}.png")
        elif selection == "plate":
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

            return fig, f"```{img_path}```", False, True

        else:
            return None, None, False, False

    else:
        return None, None, True, False


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
        selection_dict = {"motility": "motility", "segment": "binary", "plate": "plate"}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict  # return the option dictionary

    elif pipeline_selection == "fecundity":

        # create the options
        selection_dict = {"binary": "binary", "plate": "plate"}

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
        selection_dict = {"plate": "plate", "straightened_worms": "straightened_worms"}

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
        thumbs_file_path = Path(volume, "output/thumbs/")

        # create the options
        selection_dict = {
            "plate": "plate",
            "straightened_worms": "straightened_worms",
        }

        # New code to add: list all matching files and extract unique identifiers
        pattern = f"{platename}*.png"
        # Using glob to match the pattern
        all_files = list(thumbs_file_path.glob(pattern))
        # Extracting unique identifiers from filenames (e.g., _w1, _w2, etc.)
        wavelengths = set()
        for file_path in all_files:
            parts = file_path.name.split("_")
            if (
                len(parts) > 1
                and parts[-1].startswith("w")
                and parts[-1].endswith(".png")
            ):
                wavelengths.add(parts[-1].replace(".png", ""))

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
