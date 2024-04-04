########################################################################
####                                                                ####
####                        Imports                                 ####
####                                                                ####
########################################################################

import pandas as pd
from pathlib import Path
import os
import pandas as pd
from pathlib import Path
import os
import subprocess
import time
import shlex
import re
import glob

from app.utils.callback_functions import eval_bool, create_figure_from_filepath
from app.utils.callback_functions import update_yaml_file, clean_and_create_directories, copy_files_to_input_directory

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
                plate_base] = preamble_to_run_wrmXpress_non_tracking(store)
            
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
                return fecundity_run(output_folder=output_folder, 
                                       output_file=output_file, 
                                       wrmxpress_command_split=wrmxpress_command_split, 
                                       set_progress=set_progress, 
                                       volume=volume, 
                                       platename=platename, 
                                       wells=wells, 
                                       plate_base=plate_base)
            
            elif pipeline_selection == 'wormsize_intensity_cellpose':
                return cellprofile_wormsize_intesity_cellpose_run(
                    output_folder=output_folder,
                    output_file=output_file,
                    wrmxpress_command_split=wrmxpress_command_split,
                    wells = wells,
                    volume=volume,
                    platename=platename,
                    plate_base=plate_base,
                    set_progress=set_progress
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
                    set_progress
                ) 
            
            elif pipeline_selection == 'feeding':
                return cellprofile_feeding_run(
                    output_folder, output_file, wrmxpress_command_split,
                    wells, volume, platename, plate_base, set_progress
                    
                )
            
            elif pipeline_selection == 'wormsize':  
                return cellprofile_wormsize_run(output_folder, output_file, wrmxpress_command_split,
                             wells, volume, platename, plate_base, set_progress
                             )

########################################################################
####                                                                ####
####                       app.py functions                         ####
####                                                                ####
########################################################################

def preamble_to_run_wrmXpress_tracking(store):
    """
    The purpose of this function is to prepare the wrmXpress command, output folder, output file, 
    command message, wells, volume, platename, motility, segment, cellprofiler, and cellprofilepipeline.
    ===============================================================================
    Arguments:
        - store : dict : A dictionary containing the store
    ===============================================================================
    Returns:
        - wrmxpress_command_split : list : List of wrmXpress commands
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - command_message : str : A command message
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - wells_analyzed : list : List of wells analyzed
        - tracking_well : list : List of tracking wells
    ===============================================================================

    """
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    file_structure = store['file_structure']
    print('Running wrmXpress.')
    # necessary file paths
    img_dir = Path(volume, platename)
    input_dir = Path(volume, 'input')
    platename_input_dir = Path(input_dir, platename)
    full_yaml = Path(volume, platename + '.yml')

    update_yaml_file(
            full_yaml,
            full_yaml,
            {'wells': ['All']}
        )

        # clean and create directories
    clean_and_create_directories(
            input_path=Path(volume, 'input', platename), 
            work_path=Path(volume, 'work', platename),
            output_path=Path(volume, 'output')
        )
    if file_structure == 'avi':
        copy_files_to_input_directory(
                platename_input_dir=platename_input_dir,
                htd_file= None,
                img_dir=img_dir,
                wells=wells,
                plate_base=None,
                platename=platename
            )
    elif file_structure == 'imagexpress':
        htd_file = Path(img_dir, f'{platename}.HTD')
        copy_files_to_input_directory(
                platename_input_dir=platename_input_dir,
                htd_file= htd_file,
                img_dir=img_dir,
                wells=wells,
                plate_base=None,
                platename=platename
            )
        # Command message
    command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

    wrmxpress_command = f'python -u wrmXpress/wrapper.py {volume}/{platename}.yml {platename}'
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_folder = Path(volume, 'work', platename)
    output_file = Path(volume, 'work', platename, f"{platename}_run.log")  # Specify the name and location of the output file
    wells_analyzed = []
    tracking_well = []
    return wrmxpress_command_split, output_folder, output_file, command_message, wells, volume, platename, wells_analyzed, tracking_well

def tracking_wrmXpress_run(
    output_folder,
    output_file,
    wrmxpress_command_split,
    volume,
    platename,
    wells,
    wells_analyzed,
    tracking_well,
    set_progress
    ):
    """
    The purpose of this function is to run wrmXpress for tracking and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - wrmxpress_command_split : list : List of wrmXpress commands
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - wells : list : List of well names
        - wells_analyzed : list : List of wells analyzed
        - tracking_well : list : List of tracking wells
        - set_progress : function : Function to set the progress
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
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
                tracks_file_path = Path(volume, 'output', 'thumbs', f'{platename}_tracks.png')

                while not os.path.exists(tracks_file_path):
                    time.sleep(1)

                # create figure from file path
                fig_1 = create_figure_from_filepath(tracks_file_path)
                docker_output_formatted = ''.join(docker_output)

                print('wrmXpress is finished')
                docker_output.append('wrmXpress is finished')
                docker_output_formatted = ''.join(docker_output)
                return fig_1, False, False, f'', f'```{docker_output_formatted}```'
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

                set_progress((str(len(wells_analyzed)), str(2*len(wells)), fig, f'```{current_well_path}```' ,f'```{docker_output_formatted}```'))
            
            elif 'Tracking well' in line:
                # find the well that is being analyzed
                current_well = line.split(' ')[-1].split('.')[0]
                # add the well to the list of wells analyzed if it is not already there
                if current_well not in tracking_well:
                    tracking_well.append(current_well)
                
                # obtain file path to current well
                current_well_path = Path(volume, 'input', platename, 'TimePoint_1', f'{platename}_{tracking_well[-1]}.TIF')

                # ensure file path exists
                while not os.path.exists(current_well_path):
                    time.sleep(1)
                
                # create figure from file path
                fig = create_figure_from_filepath(current_well_path)
                docker_output_formatted = ''.join(docker_output)

                set_progress((str(len(tracking_well)+ len(wells_analyzed)), str(2*len(wells)), fig, f'```{current_well_path}```' ,f'```{docker_output_formatted}```'))

def preamble_to_run_wrmXpress_non_tracking(store):
    """
    The purpose of this function is to prepare the wrmXpress command, output folder, output file,
    command message, wells, volume, platename, motility, segment, cellprofiler, and cellprofilepipeline.
    ===============================================================================
    Arguments:
        - store : dict : A dictionary containing the store
    ===============================================================================
    Returns:
        - wrmxpress_command_split : list : List of wrmXpress commands
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - command_message : str : A command message
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
    ===============================================================================
    """
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    print('Running wrmXpress.')

    # necessary file paths
    img_dir = Path(volume, platename)
    input_dir = Path(volume, 'input')
    platename_input_dir = Path(input_dir, platename)
    plate_base = platename.split("_", 1)[0]
    htd_file = Path(img_dir, f'{plate_base}.HTD')
    full_yaml = Path(volume, platename + '.yml')

    update_yaml_file(
            full_yaml,
            full_yaml,
            {'wells': ['All']}
        )

        # clean and create directories
    clean_and_create_directories(
            input_path=Path(volume, 'input', platename), 
            work_path=Path(volume, 'work', platename),
            output_path=Path(volume, 'output')
        )

    copy_files_to_input_directory(
            platename_input_dir=platename_input_dir,
            htd_file=htd_file,
            img_dir=img_dir,
            plate_base=plate_base,
            wells=wells,
            platename=platename
        )

        # Command message
    command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

    wrmxpress_command = f'python -u wrmXpress/wrapper.py {volume}/{platename}.yml {platename}'
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_folder = Path(volume, 'work', platename)
    output_file = Path(volume, 'work', platename, f"{platename}_run.log")  # Specify the name and location of the output file
    return wrmxpress_command_split, output_folder, output_file, command_message, wells, volume, platename, plate_base

def motility_or_segment_run(
        output_folder,
        output_file,
        wrmxpress_command_split,
        wells,
        volume,
        platename,
        plate_base,
        set_progress
):
    """
    The purpose of this function is to run wrmXpress for motility or segment and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - wrmxpress_command_split : list : List of wrmXpress commands
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
        - set_progress : function : Function to set the progress
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    while not os.path.exists(output_folder):
                time.sleep(1)
    with open(output_file, "w") as file:
            
        process = subprocess.Popen(
                    wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Create an empty list to store the docker output
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)

        for line in iter(process.stdout.readline, b''):
                    # Add the line to docker_output for further processing
            docker_output.append(line)
            file.write(line)
            file.flush()
            # Break the loop if 'Generating' is in the line
            if "Generating" in line:
                        break

            # Process the line if 'Running' is in the line
            if "Running" in line:
                well_running = line.split(" ")[-1]
                if well_running not in wells_analyzed:
                    # Remove the '\n' from the well_running
                    well_running = well_running.replace('\n', '')
                    wells_analyzed.append(well_running)

                    img_path = Path(
                                volume, f'{platename}/TimePoint_1/{plate_base}_{wells_analyzed[-1]}.TIF')
                    fig = create_figure_from_filepath(img_path)

                    docker_output_formatted = ''.join(docker_output) 
                    set_progress((
                                str(len(wells_analyzed)),
                                str(wells_to_be_analyzed),
                                fig,
                                f'```{img_path}```',
                                f'```{docker_output_formatted}```'
                            ))
                

        # get the platename (default) file in output dir that have .png extension
        output_path = Path(volume, 'output', 'thumbs', platename + '.png')
        while not os.path.exists(output_path):
                    time.sleep(1)

        # create a figure for the output
        fig_1 = create_figure_from_filepath(output_path) 
                
        print('wrmXpress has finished.')
        docker_output.append('wrmXpress has finished.')
        docker_output_formatted = ''.join(docker_output) 
                
                    
        # Return the figure, False, False, and an empty string
        return fig_1, False, False, f'', f'```{docker_output_formatted}```'

def fecundity_run(
        output_folder,
        output_file,
        wrmxpress_command_split,
        wells,
        volume,
        platename,
        plate_base,
        set_progress
):
    """
    The purpose of this function is to run wrmXpress for motility or segment and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - wrmxpress_command_split : list : List of wrmXpress commands
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
        - set_progress : function : Function to set the progress
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    while not os.path.exists(output_folder):
        time.sleep(1)
    
    with open(output_file, "w") as file:
        process = subprocess.Popen(wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)

        for line in iter(process.stdout.readline, ''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            if "Generating" in line:
                break

            if "Running" in line:
                well_running = line.split(" ")[-1].strip()  # Use strip() to remove '\n'
                if well_running not in wells_analyzed:
                    wells_analyzed.append(well_running)
                    well_base_path = Path(volume, f"{platename}/TimePoint_1/{plate_base}_{well_running}")
                    # Use rglob with case-insensitive pattern matching for .TIF and .tif
                    file_paths = list(well_base_path.parent.rglob(well_base_path.name + '*[._][tT][iI][fF]'))
                    
                    # Sort the matching files to find the one with the lowest suffix number
                    if file_paths:
                        file_paths_sorted = sorted(file_paths, key=lambda x: x.stem)
                        # Select the first file (with the lowest number) if multiple matches are found
                        img_path = file_paths_sorted[0]
                    else:
                        # Fallback if no matching files are found
                        img_path = well_base_path.with_suffix('.TIF')  # Default to .TIF if no files found

                    fig = create_figure_from_filepath(img_path)
                    
                    docker_output_formatted = ''.join(docker_output)
                    set_progress((
                        str(len(wells_analyzed)),
                        str(wells_to_be_analyzed),
                        fig,
                        f'```{img_path}```',
                        f'```{docker_output_formatted}```'
                    ))

        output_path = Path(volume, 'output', 'thumbs', platename + '.png')
        while not os.path.exists(output_path):
            time.sleep(1)

        fig_1 = create_figure_from_filepath(output_path)
                
        print('wrmXpress has finished.')
        docker_output.append('wrmXpress has finished.')
        docker_output_formatted = ''.join(docker_output)
                
        return fig_1, False, False, '', f'```{docker_output_formatted}```'
    
def cellprofile_wormsize_run(output_folder, output_file, wrmxpress_command_split,
                             wells, volume, platename, plate_base, set_progress
                             ):
    """
    The purpose of this function is to run wrmXpress for worm size and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - wrmxpress_command_split : list : List of wrmXpress commands
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
        - set_progress : function : Function to set the progress
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    while not os.path.exists(output_folder):
        time.sleep(1)
        
    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)
        progress = 0
        total_progress = wells_to_be_analyzed
        
        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()
            
            if 'Generating w1 thumbnails' in line:
                output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                while not os.path.exists(output_path):
                    time.sleep(1)
                
                fig_1 = create_figure_from_filepath(output_path)
                print('wrmXpress has finished.')
                docker_output.append('wrmXpress has finished.')
                docker_output_formatted = ''.join(docker_output)
                return fig_1, False, False, f'', f'```{docker_output_formatted}```'
            
            elif 'Image #' in line:
                csv_file_path = Path(volume, 'input', f'image_paths_wormsize_intensity_cellpose.csv')
                while not os.path.exists(csv_file_path):
                    time.sleep(1)
                
                read_csv = pd.read_csv(csv_file_path)
                well_column = read_csv['Metadata_Well']
                
                image_number_pattern = re.search(r'Image # (\d+)', line)
                if image_number_pattern:
                    image_number = int(image_number_pattern.group(1))
                    well_id = well_column.iloc[image_number - 1]
                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}.TIF')

                    if img_path.exists():
                        fig = create_figure_from_filepath(img_path)
                        progress += 1
                        docker_output_formatted = ''.join(docker_output)
                        set_progress(((image_number), str(total_progress), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
            
def cellprofile_wormsize_intesity_cellpose_run(
    output_folder, output_file, wrmxpress_command_split,
    wells, volume, platename, plate_base, set_progress
):
    """
    The purpose of this function is to run wrmXpress for worm size and intensity using CellPose and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - wrmxpress_command_split : list : List of wrmXpress commands
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
        - set_progress : function : Function to set the progress
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    while not os.path.exists(output_folder):
        time.sleep(1)
        
    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)
        progress = 0
        total_progress = 2 * wells_to_be_analyzed
        
        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()
            
            if 'Generating w1 thumbnails' in line:
                output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                while not os.path.exists(output_path):
                    time.sleep(1)
                
                fig_1 = create_figure_from_filepath(output_path)
                print('wrmXpress has finished.')
                docker_output.append('wrmXpress has finished.')
                docker_output_formatted = ''.join(docker_output)
                return fig_1, False, False, f'', f'```{docker_output_formatted}```'
            
            elif 'Image #' in line:
                csv_file_path = Path(volume, 'input', f'image_paths_wormsize_intensity_cellpose.csv')
                while not os.path.exists(csv_file_path):
                    time.sleep(1)
                
                read_csv = pd.read_csv(csv_file_path)
                well_column = read_csv['Metadata_Well']
                
                image_number_pattern = re.search(r'Image # (\d+)', line)
                if image_number_pattern:
                    image_number = int(image_number_pattern.group(1))
                    well_id = well_column.iloc[image_number - 1]
                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}.TIF')
                    if img_path.exists():
                        fig = create_figure_from_filepath(img_path)
                        progress += 1
                        docker_output_formatted = ''.join(docker_output)
                        set_progress((str(len(wells) + image_number), str(total_progress), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
            
            elif "[INFO]" in line and "%" in line:
                info_parts = line.split('/')
                info_well_analyzed = info_parts[0].split(' ')[-1]
                info_total_wells = info_parts[1].split(' ')[0]
                
                if info_well_analyzed == info_total_wells:
                    current_well = wells[int(info_well_analyzed)-1]
                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{current_well}.TIF')
                    if os.path.exists(img_path):
                        fig = create_figure_from_filepath(img_path)
                        docker_output_formatted = ''.join(docker_output)
                        set_progress((str(progress), str(total_progress), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
                else:
                    current_well = wells[int(info_well_analyzed)]
                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{current_well}.TIF')
                    if os.path.exists(img_path):
                        fig = create_figure_from_filepath(img_path, 'gray')
                        docker_output_formatted = ''.join(docker_output)
                        progress += 1
                        set_progress((str(progress), str(total_progress), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))

def cellprofile_mf_celltox_run(output_folder, output_file, wrmxpress_command_split,
                           wells, volume, platename, plate_base, set_progress
                           ):
    """
    The purpose of this function is to run wrmXpress for motility, fecundity, and celltox and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - wrmxpress_command_split : list : List of wrmXpress commands
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
        - set_progress : function : Function to set the progress
        - cellprofilepipeline : str : CellProfiler pipeline
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    while not os.path.exists(output_folder):
        time.sleep(1)
    
    with open(output_file, "w") as file:
        process = subprocess.Popen(wrmxpress_command_split, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)

        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            csv_file_path = Path(volume, 'input', f'image_paths_mf_celltox.csv')
            while not os.path.exists(csv_file_path):
                time.sleep(1)

            read_csv = pd.read_csv(csv_file_path)
            well_column = read_csv['Metadata_Well']
            
            if 'Generating w1 thumbnails' in line:
                output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                while not os.path.exists(output_path):
                    time.sleep(1)
                
                fig_1 = create_figure_from_filepath(output_path)
                
                print('wrmXpress has finished.')
                docker_output.append('wrmXpress has finished.')
                docker_output_formatted = ''.join(docker_output) 
                return fig_1, False, False, '', f'```{docker_output_formatted}```'
            
            elif 'Image #' in line:
                image_number_pattern = re.search(r'Image # (\d+)', line)
                if image_number_pattern:
                    image_number = int(image_number_pattern.group(1))
                    well_id = well_column.iloc[image_number - 1]

                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}_s1.TIF')
                    if img_path.exists():
                        fig = create_figure_from_filepath(img_path)
                        docker_output_formatted = ''.join(docker_output) 
                        set_progress((str(image_number), str(len(wells)), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))

def cellprofile_feeding_run(
    output_folder, output_file, wrmxpress_command_split,
    wells, volume, platename, plate_base, set_progress
    
):
    """
    The purpose of this function is to run wrmXpress for feeding and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - output_folder : str : Path to the output folder
        - output_file : str : Path to the output file
        - wrmxpress_command_split : list : List of wrmXpress commands
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
        - set_progress : function : Function to set the progress
        - cellprofilepipeline : str : CellProfiler pipeline
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    while not os.path.exists(output_folder):
        time.sleep(1)
    
    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)

        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            csv_file_path = Path(volume, 'input', f'image_paths_feeding.csv')
            while not os.path.exists(csv_file_path):
                time.sleep(1)

            read_csv = pd.read_csv(csv_file_path)
            well_column = read_csv['Metadata_Well']
            
            if 'Generating w1 thumbnails' in line:
                output_path = Path(volume, 'output', 'thumbs', platename + "_w1" + '.png')
                while not os.path.exists(output_path):
                    time.sleep(1)

                fig_1 = create_figure_from_filepath(output_path)
                print('wrmXpress has finished.')
                docker_output.append('wrmXpress has finished.')
                docker_output_formatted = ''.join(docker_output) 
                return fig_1, False, False, '', f'```{docker_output_formatted}```'

            elif 'Image #' in line:
                image_number_pattern = re.search(r'Image # (\d+)', line)
                if image_number_pattern:
                    image_number = int(image_number_pattern.group(1))
                    well_id = well_column.iloc[image_number - 1]

                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}_w1.TIF')
                    if img_path.exists():
                        fig = create_figure_from_filepath(img_path)
                        docker_output_formatted = ''.join(docker_output) 
                        set_progress((str(image_number), str(len(wells)), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))
