########################################################################
####                                                                ####
####                        Imports                                 ####
####                                                                ####
########################################################################
from app.utils.callback_functions import create_figure_from_filepath, eval_bool
from app.utils.callback_functions import motility_or_segment_run, cellprofile_wormsize_run, cellprofile_wormsize_intesity_cellpose_run, cellprofile_mf_celltox_run, cellprofile_feeding_run, preamble_to_run_wrmXpress_non_tracking, preamble_to_run_wrmXpress_tracking
import time
from pathlib import Path
import os
import subprocess

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
    tracking = store["tracking"]
    # Check if the submit button has been clicked
    if n_clicks:
        if eval_bool(tracking) == False:
            return run_analysis_non_tracking(set_progress, store)
        elif eval_bool(tracking) == True:
            return run_analysis_tracking(set_progress, store)
       

def run_analysis_tracking(
    set_progress,
    store,
):
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
          wells_analyzed
    ] = preamble_to_run_wrmXpress_tracking(store)
    
    while not os.path.exists(output_folder):
        time.sleep(1)
    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Create an empty list to store the docker output
        docker_output = []

        for line in iter(process.stdout.readline, b''):
            # Add the line to docker_output for further processing
            docker_output.append(line)
            file.write(line)
            file.flush()
            if 'Generating w1 thumbnails' in line:
                return None, False, False, f'', f'```hello world```'
            elif 'Reconfiguring' in line:
                # find the well that is being analyzed
                current_well = line.split('.')[0].split('_')[-1]

                # add the well to the list of wells analyzed if it is not already there
                if current_well not in wells_analyzed:
                    wells_analyzed.append(current_well)
                # obtain file path to current well
                current_well_path = Path(volume, 'input', platename, 'TimePoint_1', f'{platename}_{wells_analyzed[-1]}.TIF')

                # ensure file path exists
                while not os.path.exists(current_well_path):
                    time.sleep(1)

                # create figure from file path
                fig = create_figure_from_filepath(current_well_path)
                docker_output_formatted = ''.join(docker_output)

                set_progress((str(len(wells_analyzed)), str(len(wells)), fig, f'```{current_well_path}```' ,f'```{docker_output_formatted}```'))
            
            
# create function to run analysis
def run_analysis_non_tracking(
  set_progress,
  store,      
):
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

    if motility == 'True' or segment == 'True':
        motility_or_segment_run(output_folder=output_folder, 
                                       output_file=output_file, 
                                       wrmxpress_command_split=wrmxpress_command_split, 
                                       set_progress=set_progress, 
                                       volume=volume, 
                                       platename=platename, 
                                       wells=wells, 
                                       plate_base=plate_base)
            
    if cellprofiler == 'True': 
            if cellprofilepipeline == 'wormsize':
                cellprofile_wormsize_run(
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
            
            elif cellprofilepipeline == 'wormsize_intensity_cellpose':
                cellprofile_wormsize_intesity_cellpose_run(
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
            
            elif cellprofilepipeline == "mf_celltox":
               cellprofile_mf_celltox_run(
                    output_folder, output_file, wrmxpress_command_split,
                    wells, volume, platename, plate_base, set_progress,
                    cellprofilepipeline
                ) 
            
            elif cellprofilepipeline == "feeding":
                cellprofile_feeding_run(
                    output_folder, output_file, wrmxpress_command_split,
                    wells, volume, platename, plate_base, set_progress,
                    cellprofilepipeline
                )