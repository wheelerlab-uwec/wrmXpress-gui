########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import pandas as pd
from pathlib import Path
import os
import signal
import shutil
import numpy as np
from PIL import Image
import plotly.express as px
import yaml
import plotly.express as px
import glob
import tifffile as tiff
from skimage import exposure
import pandas as pd
from pathlib import Path
import os
import subprocess
import time
import shlex
import re

from app.utils.callback_functions import create_df_from_inputs, update_yaml_file, clean_and_create_directories
from app.utils.callback_functions import copy_files_to_input_directory, create_figure_from_filepath

########################################################################
####                                                                ####
####                          Functions                             ####
####                                                                ####
########################################################################

def preview_callback_functions(
    store
):
        """
        This function is used to preview the analysis of the selected options.
        ======================================================================
        Arguments:
            - motility_selection : str : Motility selection
            - segment_selection : str : Segment selection
            - fecundity_selection : str : Fecundity selection
            - selection : str : Selection
            - cellprofiler : str : Cell profiler
            - cellprofilepipeline : str : Cell profile pipeline
            - platename : str : Plate name
            - volume : str : Volume
            - wells : str : Wells
            - plate_base : str : Plate base
        ======================================================================
        Returns:
            - function : function : Function to preview the analysis
                -- These functions are defined in app/utils/callback_functions.py
                -- and specified in what lines they are defined in the file
        ======================================================================

        """
        pipeline_selection = store['pipeline_selection']

        if pipeline_selection == 'motility':
            return motility_segment_fecundity_preview(store)
        
        elif pipeline_selection == 'fecundity':
            return motility_segment_fecundity_preview(store)
        
        elif pipeline_selection == 'tracking':
            return tracking_wrmXpress_preview(store)
        
        elif pipeline_selection == 'wormsize':
            return cellprofile_wormsize_preview(
                store
            )
        
        elif pipeline_selection == 'wormsize_intensity_cellpose':
            return cellprofile_wormsize_intensity_cellpose_preview(
                store
            )
        
        elif pipeline_selection == 'mf_celltox':
            return cellprofile_mf_celltox_preview(
                store
            )
        
        elif pipeline_selection == 'feeding':
            return cellprofile_feeding_preview(
                store
            )
            
########################################################################
####                                                                ####
####                   preview.py functions                         ####
####                                                                ####
########################################################################

def preamble_to_run_wrmXpress_preview(
       platename,
       volume, 
       wells 
):
    """
    This function prepares the wrmXpress command, output preview log file, command message, and first well.
    ===============================================================================
    Arguments:
        - platename : str : Name of the plate
        - volume : str : Path to the volume
        - wells : list : List of well names
    ===============================================================================
    Returns:
        - wrmxpress_command_split : list : List of wrmXpress commands
        - output_preview_log_file : str : Path to the output preview log file
        - command_message : str : A command message
        - first_well : str : The first well in the list of wells
    ===============================================================================
    
    """
     # defining the yaml file path (same as the filepath from configure.py)
    preview_yaml_platename = '.' + platename + '.yml'
    preview_yaml_platenmaefull_yaml = Path(volume, preview_yaml_platename)
    full_yaml = Path(volume, platename + '.yml')

    update_yaml_file(
                full_yaml, 
                preview_yaml_platenmaefull_yaml,
                {'wells': ['All']}
            )
            
    if wells == 'All':
            first_well = "A01"
    else:
            first_well = wells[0]


        # Checking if input folder exists, and if not, create it,
        # then subsequently copy the images into this folder
        # Input and platename input folder paths
        # necessary file paths
    img_dir = Path(volume, platename)
    input_dir = Path(volume, 'input')
    platename_input_dir = Path(input_dir, platename)
    plate_base = platename.split("_", 1)[0]
    htd_file = Path(img_dir, f'{plate_base}.HTD')

    # Clean and create directories
    clean_and_create_directories(
                input_path=Path(volume, 'input', platename),
                work_path=Path(volume, 'work', platename)
    )
            
            # Copy files to input directory
    copy_files_to_input_directory(
                platename_input_dir=platename_input_dir,
                htd_file=htd_file,
                img_dir=img_dir,    
                plate_base=plate_base,
                wells = first_well,
                platename=platename
            )

        # Command message
    command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

    wrmxpress_command = f'python wrmXpress/wrapper.py {volume}/.{platename}.yml {platename}'
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_preview_log_file = Path(volume, 'input', platename, f'{platename}_preview.log')
    return wrmxpress_command_split, output_preview_log_file, command_message, first_well

def motility_segment_fecundity_preview(store):
    """
    This function is used to preview the analysis of the selected options from
    the configuration page, including motility, segment, and fecundity. This function
    will run wrmXpress and return the path to the image, the figure, and the open status
    if the first well has not already been analyzed.
    ===============================================================================
    Arguments:
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - wells : list : List of well names
        - selection : str : Selection
    ===============================================================================
    Returns:
        - path : str : Path to the image
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
        - open_status : bool : Open status of the alerts
    ===============================================================================
    """
    # Obtain the store data
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    pipeline_selection = store['pipeline_selection']
    selection = ['motility', 'segment']
    file_structure = store['file_structure']
    # Check to see if first well already exists, if it does insert the img
    # rather than running wrmXpress again
    first_well_path = Path(volume, 'work', f'{platename}/{wells[0]}/img/{platename}_{wells[0]}.png')

    # Check if the first well path exists
    if os.path.exists(first_well_path):
        # Checking the selection and changing the scale accordingly
        if selection == 'motility':
            scale = 'inferno'
        else:
            scale = 'gray'

        # Open the image and create a figure
        fig = create_figure_from_filepath(first_well_path, scale=scale)

        # Return the path and the figure and the open status of the alerts
        return f"```{first_well_path}```", fig, False, f'', False
    if file_structure == 'imagexpress':
        wrmxpress_command_split, output_preview_log_file, command_message, first_well = preamble_to_run_wrmXpress_preview(
            platename=platename, volume=volume, wells=wells
        )
    elif file_structure == 'avi':

        # modify this to work for avi files
        wrmxpress_command_split, output_preview_log_file, command_message, first_well = preamble_to_run_wrmXpress_preview(
            platename=platename, volume=volume, wells=wells
        )

    with open(output_preview_log_file, 'w') as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []

        print('Running wrmXpress.')
        docker_output.append('Running wrmXpress.')

        while not os.path.exists(Path(volume, 'input')):
            time.sleep(1)

        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()
            
            # Assumes IX-like file structure
            img_path = Path(volume, 'work', f'{platename}/{first_well}/img/{platename}_{first_well}.png')

            # Wait for the image to be created
            while not os.path.exists(img_path):
                time.sleep(1)

            # Checking the selection and changing the scale accordingly
            if selection == 'motility':
                scale = 'inferno'
            else:
                scale = 'gray'

            # Open the image and create a figure
            fig = create_figure_from_filepath(img_path, scale=scale)
            
            if 'Generating w1 thumbnails' in line:
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f'', False

def cellprofile_wormsize_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including worm size. This function will run wrmXpress and return
    the path to the image, the figure, and the open status if the first well has not already been analyzed.
    ===============================================================================
    Arguments:
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
    ===============================================================================
    Returns:
        - path : str : Path to the image
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
        - open_status : bool : Open status of the alerts
    ===============================================================================
    """
    # Obtain the store data
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    pipeline_selection = store['pipeline_selection']
    first_well = wells[0]
    # Assumes IX-like file structure
    first_well_path = Path(volume, f'output/straightened_worms/{plate_base}_{first_well}.tiff')

    # Check if the first well path exists
    if os.path.exists(first_well_path):
        # Open the image and create a figure
        fig = create_figure_from_filepath(first_well_path)

        # Return the path and the figure and the open status of the alerts
        return f"```{first_well_path}```", fig, False, f'', False

    wrmxpress_command_split, output_preview_log_file, command_message, first_well = preamble_to_run_wrmXpress_preview(
        platename=platename,
        volume=volume,
        wells=wells
    )
    with open(output_preview_log_file, 'w') as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []

        while not os.path.exists(Path(volume, 'input')):
            time.sleep(1)

        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            if 'Generating w1 thumbnails' in line:
                # Assumes IX-like file structure
                file_path = Path(volume, f'output/straightened_worms/{plate_base}_{first_well}.tiff')
                # Open the image and create a figure
                fig = create_figure_from_filepath(file_path)

                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f'', False

def cellprofile_wormsize_intensity_cellpose_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including worm size and intensity using CellPose. This function
    will run wrmXpress and return the path to the image, the figure, and the open status if the first well has not already been analyzed.
    ===============================================================================
    Arguments:
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
    ===============================================================================
    Returns:
        - path : str : Path to the image
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
        - open_status : bool : Open status of the alerts
    ===============================================================================
    """
    # Obtain the store data
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    pipeline_selection = store['pipeline_selection']
    
    output_folder = Path(volume, 'input', platename)
    output_preview_log_file = Path(output_folder, f'{platename}_preview.log')

    # Assumes the first well in the list is the one to check
    first_well = wells[0]
    
    # Check to see if first well already exists, if it does insert the img
    # rather than running wrmXpress again
    first_well_path = Path(volume, f'output/straightened_worms/{plate_base}_{first_well}.tiff')
    if os.path.exists(first_well_path):
        # Open the image and create a figure
        fig = create_figure_from_filepath(first_well_path)

        # Return the path and the figure and the open status of the alerts
        return f"```{first_well_path}```", fig, False, f'', False

    wrmxpress_command_split, output_preview_log_file, command_message, first_well = preamble_to_run_wrmXpress_preview(
        platename=platename,
        volume=volume,
        wells=wells
    )
    with open(output_preview_log_file, 'w') as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []

        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            img_path = Path(volume, f'output/straightened_worms/{plate_base}_{first_well}.tiff')

            # Wait for the image to be created
            while not os.path.exists(img_path):
                time.sleep(1)

            # Open the image and create a figure
            fig = create_figure_from_filepath(img_path)

            if 'Generating w1 thumbnails' in line:
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f'', False
            
def cellprofile_mf_celltox_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including motility, fecundity, and celltox. This function
    will run wrmXpress and return the path to the image, the figure, and the open status if the first well has not already been analyzed.
    ===============================================================================
    Arguments:
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
    ===============================================================================
    Returns:
        - path : str : Path to the image
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
        - open_status : bool : Open status of the alerts
    =============================================================================== 
    """
    # Obtain the store data
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    pipeline_selection = store['pipeline_selection']
    
    output_folder = Path(volume, 'input', platename)
    output_preview_log_file = Path(output_folder, f'{platename}_preview.log')

    first_well = wells[0]  # Assuming first_well is defined here as the first item in wells

    # Check to see if first well already exists, if it does insert the img
    # rather than running wrmXpress again
    first_well_path = Path(volume, 'work', platename, first_well, 'img', f'{platename}_{first_well}.png')
    if os.path.exists(first_well_path):
        # Open the image and create a figure
        fig = create_figure_from_filepath(first_well_path)

        # Return the path and the figure and the open status of the alerts
        return f"```{first_well_path}```", fig, False, f'', False

    wrmxpress_command_split, output_preview_log_file, command_message, first_well = preamble_to_run_wrmXpress_preview(
        platename=platename,
        volume=volume,
        wells=wells
    )
    with open(output_preview_log_file, 'w') as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []

        while not os.path.exists(output_folder):
            time.sleep(1)

        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            img_path = Path(volume, 'work', platename, first_well, 'img', f'{platename}_{first_well}.png')

            # Wait for the image to be created
            while not os.path.exists(img_path):
                time.sleep(1)

            # Open the image and create a figure
            fig = create_figure_from_filepath(img_path)

            if 'Generating w1 thumbnails' in line:
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f'', False

def cellprofile_feeding_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including feeding. This function will run wrmXpress and return
    the path to the image, the figure, and the open status if the first well has not already been analyzed.
    ===============================================================================
    Arguments:
        - wells : list : List of well names
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - plate_base : str : Base name of the plate
    ===============================================================================
    Returns:
        - path : str : Path to the image
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
        - open_status : bool : Open status of the alerts
    ===============================================================================
    """
    # Obtain the store data
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    pipeline_selection = store['pipeline_selection']

    output_folder = Path(volume, 'input', platename)
    output_preview_log_file = Path(output_folder, f'{platename}_preview.log')

    first_well = wells[0]  # Assuming first_well is the first item in wells list

    # Check to see if first well already exists, if it does insert the img
    # rather than running wrmXpress again
    first_well_path = Path(volume, f'output/straightened_worms/{plate_base}-{first_well}.tiff')
    if os.path.exists(first_well_path):
        # Open the image and create a figure
        fig = create_figure_from_filepath(first_well_path)

        # Return the path and the figure and the open status of the alerts
        return f"```{first_well_path}```", fig, False, f'', False

    wrmxpress_command_split, output_preview_log_file, command_message, first_well = preamble_to_run_wrmXpress_preview(
        platename=platename,
        volume=volume,
        wells=wells
    )

    with open(output_preview_log_file, 'w') as file:
        process = subprocess.Popen(
            wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []

        while not os.path.exists(output_folder):
            time.sleep(1)

        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            if 'Generating w1 thumbnails' in line:
                # Wait for the image to be created
                while not os.path.exists(first_well_path):
                    time.sleep(1)

                # Open the image and create a figure
                fig = create_figure_from_filepath(first_well_path)

                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f'', False

def tracking_wrmXpress_preview(
        store
):
    """
    This function is used to preview the analysis of the selected options from
    the configuration page, including motility, segment, and fecundity. This function
    will run wrmXpress and return the path to the image, the figure, and the open status
    if the first well has not already been analyzed.
    ===============================================================================
    Arguments:
        - volume : str : Path to the volume
        - platename : str : Name of the plate
        - wells : list : List of well names
        - selection : str : Selection
    ===============================================================================
    Returns:
        - path : str : Path to the image
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
        - open_status : bool : Open status of the alerts
    ===============================================================================
    """
    # Obtain the store data
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]
    pipeline_selection = store['pipeline_selection']
    selection = ['motility', 'segment']

    # check to see if the first well has already been analyzed
    first_well_path = Path(volume, 'work', f'{platename}/{wells[0]}/img/{platename}_{wells[0]}_tracks.png')

    # Check if the first well path exists
    if os.path.exists(first_well_path):
        # Open the image and create a figure
        fig = create_figure_from_filepath(first_well_path)

        # Return the path and the figure and the open status of the alerts
        return f"```{first_well_path}```", fig, False, f'', False
    
    # if the first well does not exist, run wrmXpress
    wrmxpress_command_split, output_folder, output_file, command_message, wells, volume, platename, wells_analyzed, tracking_well = preamble_to_run_wrmXpress_preview_tracking(
        volume, platename, wells
    )

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
                first_well_path = Path(volume, 'work', f'{platename}/{wells[0]}/img/{platename}_{wells[0]}_tracks.png')

                while not os.path.exists(first_well_path):
                    time.sleep(1)

                # create figure from file path
                fig_1 = create_figure_from_filepath(first_well_path)
                docker_output_formatted = ''.join(docker_output)

                print('wrmXpress is finished')
                docker_output.append('wrmXpress is finished')
                docker_output_formatted = ''.join(docker_output)
                return command_message, fig_1, False, f'', False

def preamble_to_run_wrmXpress_preview_tracking(volume, platename, wells):
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
    htd_file = Path(img_dir, f'{platename}.HTD')
    if not os.path.exists(htd_file):
        copy_files_to_input_directory(
                platename_input_dir=platename_input_dir,
                htd_file= None,
                img_dir=img_dir,
                wells=wells[0],
                plate_base=None,
                platename=platename
            )
    elif os.path.exists(htd_file):
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
    output_file = Path(volume, 'work', platename, f"{platename}_preview.log")  # Specify the name and location of the output file
    wells_analyzed = []
    tracking_well = []
    return wrmxpress_command_split, output_folder, output_file, command_message, wells, volume, platename, wells_analyzed, tracking_well
