########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

from dash import callback
from dash.dependencies import Input, Output, State
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
import os
import dash
from dash.long_callback import DiskcacheLongCallbackManager

# importing utils
from app.utils.callback_functions import send_ctrl_c
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

@callback(
    Output("cancel-analysis", 'n_clicks'),
    Input("cancel-analysis", 'n_clicks')
)
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
        send_ctrl_c(1234)
        print('Control + C', 'wrmxpress analysis cancelled')

    return n_clicks

@callback(
    [
        Output('analysis-postview', 'figure'),
        Output('analysis-postview-message', 'children'),
        Output('first-view-of-analysis-alert', 'is_open'),
        Output('additional-view-of-analysis-alert', 'is_open')
    ],
    State('analysis-dropdown', 'value'),
    Input('load-analysis-img', 'n_clicks'),
    State('store', 'data'),
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
    volume = store['mount']
    platename = store['platename']

    # check to see if selection option exists in output thumbs folder
    if n_clicks:

        # check to see if selection is plate
        if selection == 'plate':

            # obtaining the output plate path
            output_plate_path = Path(volume, f'output/thumbs/{platename}.png')

            # creating the image
            img = np.array(Image.open(output_plate_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)

            # return the figure and the output thumbs path
            return fig, f'```{output_plate_path}```', False, True

        # check to see if selection option exists in output thumbs folder
        output_thumbs_path = Path(
            volume, f'output/thumbs/{platename}_{selection}.png'
        )

        # check to see if the output thumbs path exists
        if os.path.exists(output_thumbs_path):

            # creating the image
            img = np.array(Image.open(output_thumbs_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)

            # return the figure and the output thumbs path
            return fig, f'```{output_thumbs_path}```', False, True
    else:
        return None, None, True, False

@callback(
    Output('analysis-dropdown', 'options'),

    # update the option dropdown when the run analysis is clicked
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True
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
        return []

    # get the store from the data
    pipeline_selection = store['pipeline_selection']
    if pipeline_selection == 'motility':

        # create the options
        selection_dict = {'motility': 'motility', 'segment': 'binary', 'plate': 'plate'}

        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict  # return the option dictionary
    elif pipeline_selection == 'fecundity':
            
        # create the options
        selection_dict = {'binary': 'binary', 'plate': 'plate'}
    
        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == 'tracking':
            
        # create the options
        selection_dict = {'tracks': 'tracks', 'plate': 'plate'}
        
        # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == "wormsize_intensity_cellpose":
                
        # create the options
        selection_dict = {'plate': 'plate', 'straightened_worms': 'straightened_worms'}
        
         # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == 'mf_celltox':
                
            # create the options
            selection_dict = {'plate': 'plate'}
            
            # check to see if the button has been clicked (nclicks)
            if nclicks is not None:
                return selection_dict
    elif pipeline_selection == 'wormsize':
        # create the options
        selection_dict = {'plate': 'plate', 'straightened_worms': 'straightened_worms'}
        
         # check to see if the button has been clicked (nclicks)
        if nclicks is not None:
            return selection_dict
    elif pipeline_selection == 'feeding':
       # obtain the wavelength options
        volume = store['mount']
        platename = store['platename']
        thumbs_file_path = Path(volume, 'output/thumbs/')
        
        # create the options
        selection_dict = {
            'plate': 'plate',
            'straightened_worms': 'straightened_worms',
        }

        # New code to add: list all matching files and extract unique identifiers
        pattern = f"{platename}*.png"
        # Using glob to match the pattern
        all_files = list(thumbs_file_path.glob(pattern))
        # Extracting unique identifiers from filenames (e.g., _w1, _w2, etc.)
        wavelengths = set()
        for file_path in all_files:
            parts = file_path.name.split('_')
            if len(parts) > 1 and parts[-1].startswith('w') and parts[-1].endswith('.png'):
                wavelengths.add(parts[-1].replace('.png', ''))

        # Adding these wavelengths to the selection dictionary
        for wave in sorted(wavelengths):
            selection_key = f'wavelength_{wave}'  # Format the key as you see fit
            selection_dict[selection_key] = wave

        # Assuming nclicks is some condition you've checked elsewhere
        nclicks = 1
        if nclicks is not None:
            return selection_dict
    else:   
        return {'plate': 'plate'}
