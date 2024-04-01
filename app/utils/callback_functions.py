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

########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################

def create_df_from_inputs(_rows, _cols):
    """
    This function creates a dataframe from the input rows and columns.
    ===============================================================================
    Arguments:
        - _rows : int : Number of rows in the dataframe
        - _cols : int : Number of columns in the dataframe
    ===============================================================================
    Returns:
        - df : pd.DataFrame : A dataframe with the specified number of rows and columns
    """
    rows_total = list("ABCDEFGHIJKLMNOP")  # List of letters A-P
    rows = rows_total[:int(_rows)]  # List of letters A-_rows
    columns = [str(num).zfill(2) for num in range(
        1, int(_cols) + 1)]  # List of numbers 01-_cols
    data = [[row + col for col in columns]
            for row in rows]  # List of lists of strings
    df = pd.DataFrame(data, columns=columns, index=rows)  # Create dataframe
    return df  # Return dataframe

def create_empty_df_from_inputs(_rows, _cols):
    """
    This function creates an empty dataframe from the input rows and columns.
    ===============================================================================
    Arguments:
        - _rows : int : Number of rows in the dataframe
        - _cols : int : Number of columns in the dataframe
    ===============================================================================
    Returns:
        - df : pd.DataFrame : An empty dataframe with the specified number of rows and columns
    """
    rows_total = list("ABCDEFGHIJKLMNOP")  # List of letters A-P
    rows = rows_total[:int(_rows)]  # List of letters A-_rows
    columns = [str(num).zfill(2) for num in range(
        1, int(_cols) + 1)]  # List of numbers 01-_cols
    empty_data = [[None for _ in columns]
                  for _ in rows]  # List of lists of None
    df = pd.DataFrame(empty_data, columns=columns,
                      index=rows)  # Create dataframe
    return df  # Return dataframe

def create_na_df_from_inputs(_rows, _cols):
    """
    This function creates an NA dataframe from the input rows and columns.
    ===============================================================================
    Arguments:
        - _rows : int : Number of rows in the dataframe
        - _cols : int : Number of columns in the dataframe
    ===============================================================================
    Returns:
        - df : pd.DataFrame : An NA dataframe with the specified number of rows and columns
    """
    rows_total = list("ABCDEFGHIJKLMNOP")  # List of letters A-P
    rows = rows_total[:int(_rows)]  # List of letters A-_rows
    columns = [str(num).zfill(2) for num in range(
        1, int(_cols) + 1)]  # List of numbers 01-_cols
    empty_data = [['NA' for _ in columns]
                  for _ in rows]  # List of lists of None
    df = pd.DataFrame(empty_data, columns=columns,
                      index=rows)  # Create dataframe
    return df  # Return dataframe

def eval_bool(v):
    """
    This function evaluates a boolean value from a string.
      ===============================================================================
      Arguments:
          - v : str : A string that represents a boolean value
      ===============================================================================
      Returns:
          - bool : A boolean value
    """
    return str(v).lower() in ("yes", "true", "t", "1", "True")

def prep_yaml(
        imagingmode,
        filestructure,
        multiwellrows,
        multiwellcols,
        multiwelldetection,
        species,
        stages,
        wellselection,
        volume,
        pipeline
        ):
    """
    This function prepares a dictionary for the YAML file.
    ===============================================================================
    Arguments:
        - imagingmode : str : Imaging mode
        - filestructure : str : File structure
        - multiwellrows : int : Number of rows in multi-well plate
        - multiwellcols : int : Number of columns in multi-well plate
        - multiwelldetection : str : Multi-well detection
        - species : str : Species
        - stages : str : Stages
        - motilityrun : str : Motility run
        - conversionrun : str : Conversion run
        - conversionscalevideo : str : Conversion scale video
        - conversionrescalemultiplier : str : Conversion rescale multiplier
        - segmentrun : str : Segment run
        - wavelength : str : Wavelength
        - cellprofilerrun : str : CellProfiler run
        - cellprofilerpipeline : str : CellProfiler pipeline
        - diagnosticdx : str : Diagnostic DX
        - wellselection : str : Well selection
    ===============================================================================
    Returns:
        - yaml_dict : dict : A dictionary for the YAML file
    """
    # Check if wellselection is a list or a string
    if isinstance(wellselection, list):
        if len(wellselection) == 96:  # If all wells are selected
            wellselection = ['All']  # Set wellselection to 'All'
        else:  # If not all wells are selected
            wellselection = wellselection  # Set wellselection to the input list
    elif isinstance(wellselection, str):  # If wellselection is a string
        # Set wellselection to a list containing the input string
        wellselection = [wellselection]

    if multiwellrows is None:  # If multiwellrows is None
        multiwellrows = 0  # Set multiwellrows to 0
    if multiwellcols is None:  # If multiwellcols is None
        multiwellcols = 0  # Set multiwellcols to 0
    #if conversionrescalemultiplier is None:  # If conversionrescalemultiplier is None
    #    conversionrescalemultiplier = 0  # Set conversionrescalemultiplier to 0

    [
        motilityrun, 
        conversionrun,
        segmentrun, 
        cellprofilerrun, 
        diagnosticdx, 
        fecundity, 
        trackingrun, 
        cellprofilerpipeline, 
        save_video, 
        rescale_multiplier,
        wavelength
     ] = formatting_module_for_yaml(pipeline)
    # Create a dictionary for the YAML file in the required format
    yaml_dict = {
        "imaging_mode": [imagingmode],
        "file_structure": [filestructure],
        "multi-well-rows": int(multiwellrows),
        "multi-well-cols": int(multiwellcols),
        "multi-well-detection": [multiwelldetection],
        "species": [species],
        "stages": [stages],
        "modules": {
            "motility": {"run": eval_bool(motilityrun)},
            "convert": {
                "run": eval_bool(conversionrun),
                "save_video": eval_bool(save_video),
                "rescale_multiplier": float(rescale_multiplier)
            },
            "segment": {
                "run": eval_bool(segmentrun),
                "wavelength": [wavelength]
            },
            "cellprofiler": {
                "run": eval_bool(cellprofilerrun),
                "pipeline": [cellprofilerpipeline]
            },
            "dx": {
                "run": eval_bool(diagnosticdx)
            },
            'fecundity': {
                "run": eval_bool(fecundity)
            },
            'tracking': {
                    'run': eval_bool(trackingrun)
                }
            
        },
        "wells": wellselection,
        "directories": {
            "work": [str(Path(volume, 'work'))],
            "input": [str(Path(volume, 'input'))],
            "output": [str(Path(volume, 'output'))]
        }
    }

    # Return the dictionary
    return yaml_dict

def send_ctrl_c(pid):
    """
    Sends a SIGINT signal to the process with the given PID.
    ===============================================================================
    Arguments:
        - pid : int : Process ID
    ===============================================================================
    Returns:
        - None
    """

    try:
        os.killpg(os.getpgid(pid), signal.SIGINT)
        print('Control + C', 'wrmxpress analysis cancelled')
    except ProcessLookupError:
        print("Process with PID", pid, "not found.")

def clean_and_create_directories(input_path,
                                 work_path,
                                 output_path=False
                                 ):
    """
    The purpose of this function is to clean and create the input, work, and output directories.
    That is to say, it will delete the contents of the input, work, and output directories (if they exist)
    and then recreate them.
    ===============================================================================
    Arguments:
        - input_path : str : Path to the input directory
        - work_path : str : Path to the work directory
        - output_path : str : Path to the output directory
    ===============================================================================
    Returns:
        - None
    """
    # wipe previous runs
    if os.path.exists(work_path):
        shutil.rmtree(work_path)
        work_path.mkdir(parents=True, exist_ok=True)
    else:
        work_path.mkdir(parents=True, exist_ok=True)

    if os.path.exists(input_path):
        shutil.rmtree(input_path)
        input_path.mkdir(parents=True, exist_ok=True)
    else:
        input_path.mkdir(parents=True, exist_ok=True)
    if output_path != False:
        # wipe contents of output (different logic because backend doesn't put all output in a platename dir)
        if os.path.exists(output_path):
            for filename in os.listdir(output_path):
                file_path = os.path.join(output_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s because %s' % (file_path, e))

def copy_files_to_input_directory(platename_input_dir,
                                  htd_file,
                                  img_dir,
                                  plate_base,
                                  wells,
                                  platename
                                  ):
    """
    The purpose of this function is to copy the input files to the input directory.
    ===============================================================================
    Arguments:
        - platename_input_dir : str : Path to the input directory
        - htd_file : str : Path to the .HTD file
        - img_dir : str : Path to the directory containing the images
        - plate_base : str : Base name of the plate
        - wells : list : List of well names
    ===============================================================================
    Returns:
        - None
    """
    if htd_file is not None:
        # Copy .HTD file into platename input dir
        shutil.copy(htd_file, platename_input_dir)

        # Iterate through each time point and copy images into new dirs
        time_points = [item for item in os.listdir(img_dir) if os.path.isdir(Path(img_dir, item))]

        for time_point in time_points:
            time_point_dir = Path(platename_input_dir, time_point)
            time_point_dir.mkdir(parents=True, exist_ok=True)
            
            for well in wells if isinstance(wells, list) else [wells]:
                # Use glob to find all files that match the pattern, accounting for potential extensions
                well_files_pattern = Path(img_dir, time_point, f'{plate_base}_{well}*.TIF')
                well_files = glob.glob(str(well_files_pattern))
                
                for file_path in well_files:
                    shutil.copy(file_path, time_point_dir)
    else:
        for well in wells if isinstance(wells, list) else [wells]:
            # Use glob to find all files that match the pattern, accounting for potential extensions
            well_files_pattern = Path(img_dir, f'{platename}_{well}*.avi')
            well_files = glob.glob(str(well_files_pattern))
            
            for file_path in well_files:
                shutil.copy(file_path, platename_input_dir)

def create_figure_from_filepath(img_path,
                                scale='gray'):
    """
    This function creates a figure from the input file path.
    ===============================================================================
    Arguments:
        - img_path : str : Path to the image file
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
    """

    try:
        # Attempt to open with PIL first
        img = np.array(Image.open(img_path))
    except Exception as e:
        print(f"Error opening {img_path} with PIL, trying with tifffile: {e}")
        try:
            img = tiff.imread(img_path)
            
            # Check if the image is not in a compatible shape
            if len(img.shape) == 3 and img.shape[2] == 2:
                # Assuming we can just take the first channel for visualization
                img = img[:, :, 0]
            
            # Rescale pixel values from 0 to 255 if necessary
            if img.dtype != np.uint8:
                img = exposure.rescale_intensity(img, out_range=(0, 255)).astype(np.uint8)

            # Resize the image if necessary, here it is skipped but you can use transform.rescale as before
            # img = transform.rescale(img, 0.5, anti_aliasing=True, multichannel=False)
            # img = (img * 255).astype(np.uint8)

        except Exception as e:
            print(f"Error opening {img_path} with tifffile: {e}")
            return None

    # Proceed with creating the figure using plotly
    fig = px.imshow(img, color_continuous_scale=scale)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig

def update_yaml_file(input_full_yaml, output_full_yaml, updates):
    """
    This function updates the YAML file with the specified updates.
    ===============================================================================
    Arguments:
        - full_yaml : str : Path to the YAML file
        - updates : dict : Dictionary of updates
    ===============================================================================
    Returns:
        - None
    """
    # reading in yaml file
    with open(input_full_yaml, 'r') as file:
        data = yaml.safe_load(file)

    # replace the YAML config option with ['All'] as a workaround for wrmXpress bug
    # instead, we'll copy the selected files to input and analyze all of them
    # Update data based on the updates dict
    for key, value in updates.items():
        data[key] = value

    with open(output_full_yaml, 'w') as yaml_file:
        yaml.dump(data, yaml_file,
                  default_flow_style=False)

def convert_tiff_to_tif(input_file, output_file):
    """
    This function was developed for the conversion of a .tiff file to a .TIF file.
    However, this can be used for other file types as well. 
    ===============================================================================
    Arguments:
        - input_file : str : Path to the .tiff file
        - output_file : str : Path to the .TIF file
    ===============================================================================
    Returns:
        - None    
    """
    # Open the .tiff file
    with Image.open(input_file) as img:
        # Save the image as .TIF
        img.save(output_file)

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

def motility_segment_fecundity_preview(volume, platename, wells, selection):
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

def cellprofile_wormsize_preview(wells, volume, platename, plate_base):
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
    first_well = wells[0]
    print(first_well)
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

def cellprofile_wormsize_intensity_cellpose_preview(wells, volume, platename, plate_base):
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
            
def cellprofile_mf_celltox_preview(wells, volume, platename, plate_base):
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

def cellprofile_feeding_preview(wells, volume, platename, plate_base):
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
        - motility : str : Motility
        - segment : str : Segment
        - cellprofiler : str : CellProfiler
        - cellprofilepipeline : str : CellProfiler pipeline
        - wells_analyzed : list : List of wells analyzed
        - tracking_well : list : List of tracking wells
    ===============================================================================

    """
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    motility = store["motility"]
    segment = store["segment"]
    cellprofiler = store["cellprofiler"]
    cellprofilepipeline = store["cellprofilepipeline"]
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

    copy_files_to_input_directory(
            platename_input_dir=platename_input_dir,
            htd_file= None,
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
    return wrmxpress_command_split, output_folder, output_file, command_message, wells, volume, platename, motility, segment, cellprofiler, cellprofilepipeline, wells_analyzed, tracking_well

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
        - motility : str : Motility
        - segment : str : Segment
        - cellprofiler : str : CellProfiler
        - cellprofilepipeline : str : CellProfiler pipeline
    ===============================================================================
    """
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]
    motility = store["motility"]
    segment = store["segment"]
    cellprofiler = store["cellprofiler"]
    cellprofilepipeline = store["cellprofilepipeline"]
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
    return wrmxpress_command_split, output_folder, output_file, command_message, wells, volume, platename, plate_base, motility, segment, cellprofiler, cellprofilepipeline

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
    
def cellprofile_wormsize_run(output_folder, output_file, wrmxpress_command_split,
                             wells, volume, platename, plate_base, set_progress,
                             cellprofilepipeline):
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
        - cellprofilepipeline : str : CellProfiler pipeline
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    # Ensure the output folder exists
    while not os.path.exists(output_folder):
        time.sleep(1)
    
    # Open the output file and begin the subprocess
    with open(output_file, "w") as file:
        process = subprocess.Popen(wrmxpress_command_split, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)

        # Read and process output from the subprocess
        for line in iter(process.stdout.readline, b''):
            docker_output.append(line)
            file.write(line)
            file.flush()

            # Load the CSV file to find out which well is being analyzed
            csv_file_path = Path(volume, 'input', f'image_paths_{cellprofilepipeline}.csv')
            while not os.path.exists(csv_file_path):
                time.sleep(1)
            
            read_csv = pd.read_csv(csv_file_path)
            well_column = read_csv['Metadata_Well']  # Find the well column
            
            if 'Execution halted' in line:
                output_path = Path(volume, 'output', 'thumbs', platename + '.png')
                while not os.path.exists(output_path):
                    time.sleep(1)

                # Create a figure for the output
                fig_1 = create_figure_from_filepath(output_path)
                
                print('wrmXpress has finished.')
                docker_output.append('wrmXpress has finished.')
                docker_output_formatted = ''.join(docker_output) 
                return fig_1, False, False, '', f'```{docker_output_formatted}```'

            # Check for the 'Image #' pattern to update progress
            elif 'Image #' in line:
                image_number_pattern = re.search(r'Image # (\d+)', line)
                if image_number_pattern:
                    image_number = int(image_number_pattern.group(1))
                    well_id = well_column.iloc[image_number - 1]  # Adjust for zero indexing

                    # Construct the image path
                    img_path = Path(volume, f'input/{platename}/TimePoint_1/{plate_base}_{well_id}.TIF')
                    if img_path.exists():
                        # Load and display the image
                        fig = create_figure_from_filepath(img_path)
                        docker_output_formatted = ''.join(docker_output) 
                        
                        # Update progress
                        set_progress((str(image_number), str(wells_to_be_analyzed), fig, f'```{img_path}```', f'```{docker_output_formatted}```'))

def cellprofile_wormsize_intesity_cellpose_run(
    output_folder, output_file, wrmxpress_command_split,
    wells, volume, platename, plate_base, set_progress,
    cellprofilepipeline
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
                csv_file_path = Path(volume, 'input', f'image_paths_{cellprofilepipeline}.csv')
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
                           wells, volume, platename, plate_base, set_progress,
                           cellprofilepipeline):
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

            csv_file_path = Path(volume, 'input', f'image_paths_{cellprofilepipeline}.csv')
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
    wells, volume, platename, plate_base, set_progress,
    cellprofilepipeline
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

            csv_file_path = Path(volume, 'input', f'image_paths_{cellprofilepipeline}.csv')
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

def formatting_module_for_yaml(pipeline):
    if pipeline == 'motility':
        motilityrun = 'yes'
        conversionrun = 'no'
        segmentrun = 'yes'
        cellprofilerrun = 'no'
        diagnosticdx = 'yes'
        fecundity = 'no'
        trackingrun = 'no'
        cellprofilerpipeline = None
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None

    elif pipeline == 'fecundity':
        motilityrun = 'no'
        conversionrun = 'no'
        segmentrun = 'no'
        cellprofilerrun = 'no'
        diagnosticdx = 'yes'
        fecundity = 'yes'
        trackingrun = 'no'
        cellprofilerpipeline = None
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None

    elif pipeline == 'tracking':
        motilityrun = 'no'
        conversionrun = 'no'
        segmentrun = 'no'
        cellprofilerrun = 'no'
        diagnosticdx = 'yes'
        fecundity = 'no'
        trackingrun = 'yes'
        cellprofilerpipeline = None
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None

    elif pipeline == 'wormsize':
        motilityrun = 'no'
        conversionrun = 'no'
        segmentrun = 'no'
        cellprofilerrun = 'yes'
        diagnosticdx = 'yes'
        fecundity = 'no'
        trackingrun = 'no'
        cellprofilerpipeline = 'wormsize'
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None

    elif pipeline == 'wormsize_intensity_cellpose':
        motilityrun = 'no'
        conversionrun = 'no'
        segmentrun = 'no'
        cellprofilerrun = 'yes'
        diagnosticdx = 'yes'
        fecundity = 'no'
        trackingrun = 'no'
        cellprofilerpipeline = 'wormsize_intensity_cellpose'
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None

    elif pipeline == 'mf_celltox':
        motilityrun = 'no'
        conversionrun = 'no'
        segmentrun = 'no'
        cellprofilerrun = 'yes'
        diagnosticdx = 'yes'
        fecundity = 'no'
        trackingrun = 'no'
        cellprofilerpipeline = 'mf_celltox'
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None

    elif pipeline == 'feeding':
        motilityrun = 'yes'
        conversionrun = 'no'
        segmentrun = 'yes'
        cellprofilerrun = 'no'
        diagnosticdx = 'yes'
        fecundity = 'yes'
        trackingrun = 'no'
        cellprofilerpipeline = 'feeding'
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None


    return motilityrun, conversionrun, segmentrun, cellprofilerrun, diagnosticdx, fecundity, trackingrun, cellprofilerpipeline, save_video, rescale_multiplier, wavelength