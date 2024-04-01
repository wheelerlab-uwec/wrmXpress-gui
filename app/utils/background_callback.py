########################################################################
####                                                                ####
####                        Imports                                 ####
####                                                                ####
########################################################################
from app.utils.callback_functions import eval_bool, tracking_wrmXpress_run
from app.utils.callback_functions import motility_or_segment_run, cellprofile_wormsize_run 
from app.utils.callback_functions import cellprofile_wormsize_intesity_cellpose_run, cellprofile_mf_celltox_run, cellprofile_feeding_run
from app.utils.callback_functions import preamble_to_run_wrmXpress_non_tracking, preamble_to_run_wrmXpress_tracking

########################################################################
####                                                                ####
####                       Function                                 ####
####                                                                ####
########################################################################
def callback(set_progress, n_clicks, store):
    """
    This function runs the analysis on the wrmXpress container
    ===============================================================================
    Arguments:
        - set_progress : function : A function that sets the progress of the analysis        
        - n_clicks : int : The number of times the submit button has been clicked
        - store : dict : A dictionary containing the data from the store
    ===============================================================================
    Returns:
        - fig_1 : plotly.graph_objs._figure.Figure : A figure showing the analysis
        - disabled : bool : A boolean value indicating whether the load button is disabled
            +- True : The load button is disabled
            +- False : The load button is not disabled
        - is_open : bool : A boolean value indicating whether the alert is open
            +- True : The alert is open
            +- False : The alert is not open
        - children : str : A string containing the alert message
    ===============================================================================
    Runnning:
        - submit-analysis : disabeled : A boolean value indicating whether the submit button has been disabeled
            +- True : The submit button has been disabeled
            +- False : The submit button has not been disabeled
        - cancel-analysis : disabeled : A boolean value indicating whether the cancel button has been disabeled
            +- True : The cancel button has been disabeled
            +- False : The cancel button has not been disabeled
        - image-analysis-preview : style : A dictionary containing the style of the image analysis preview
            +- {'visibility': 'visible'} : The image analysis preview is visible
            +- {'visibility': 'hidden'} : The image analysis preview is hidden
        - progress-bar-run-page : style : A dictionary containing the style of the progress bar
            +- {'visibility': 'visible'} : The progress bar is visible
            +- {'visibility': 'hidden'} : The progress bar is hidden
    ===============================================================================
    Cancel:
        - cancel-analysis : n_clicks : The number of times the cancel button has been clicked
            +- will cancel the analysis upon a single click
    ===============================================================================
    Progress:
        - progress-bar-run-page : value : The value of the progress bar
        - progress-bar-run-page : max : The maximum value of the progress bar
        - image-analysis-preview : figure : A figure showing the analysis
        - progress-message-run-page-for-analysis : children : A string containing the progress message
    ===============================================================================
    """
    # Check if store is empty
    if not store:
        return None, True, True, "No configuration found. Please go to the configuration page to set up the analysis.", "No configuration found. Please go to the configuration page to set up the analysis."

    # obtain the necessary data from the store
    pipeline_selection = store["pipeline_selection"]
    # Check if the submit button has been clicked
    if n_clicks:
        if pipeline_selection == 'tracking':
            [
                wrmxpress_command_split, 
                output_folder, 
                output_file, 
                command_message, 
                wells, 
                volume,
                platename, 
                motility, 
                segment, 
                cellprofiler, 
                cellprofilepipeline, 
                wells_analyzed, 
                tracking_well
            ] = preamble_to_run_wrmXpress_tracking(store)
            return tracking_wrmXpress_run(
                output_folder,
                output_file,
                wrmxpress_command_split,
                volume,
                platename,
                wells,
                wells_analyzed,
                tracking_well,
                set_progress
            )
        
        else:

            [wrmxpress_command_split,
                output_folder, 
                output_file, 
                command_message, 
                wells, 
                volume, 
                platename, 
                plate_base, 
                motility, 
                segment, 
                cellprofiler, 
                cellprofilepipeline] = preamble_to_run_wrmXpress_non_tracking(store)
            
            if pipeline_selection == 'motility':
                return motility_or_segment_run(output_folder=output_folder, 
                                       output_file=output_file, 
                                       wrmxpress_command_split=wrmxpress_command_split, 
                                       set_progress=set_progress, 
                                       volume=volume, 
                                       platename=platename, 
                                       wells=wells, 
                                       plate_base=plate_base)
            
            elif pipeline_selection == 'fecundity':
                return
            
            elif pipeline_selection == 'wormsize_intensity_cellpose':
                return cellprofile_wormsize_intesity_cellpose_run(
                    output_folder=output_folder,
                    output_file=output_file,
                    wrmxpress_command_split=wrmxpress_command_split,
                    wells = wells,
                    volume=volume,
                    platename=platename,
                    plate_base=plate_base,
                    set_progress=set_progress,
                    cellprofilepipeline=cellprofilepipeline
                )
            
            elif pipeline_selection == 'mf_celltox':
                return cellprofile_mf_celltox_run(
                    output_folder, 
                    output_file, 
                    wrmxpress_command_split,
                    wells, 
                    volume, 
                    platename, 
                    plate_base, 
                    set_progress,
                    cellprofilepipeline
                ) 
            
            elif pipeline_selection == 'feeding':
                return cellprofile_feeding_run(
                    output_folder, output_file, wrmxpress_command_split,
                    wells, volume, platename, plate_base, set_progress,
                    cellprofilepipeline
                )
            
            elif pipeline_selection == 'wormsize':  
                return
       