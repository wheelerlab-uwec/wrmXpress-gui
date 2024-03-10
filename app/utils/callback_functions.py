########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import pandas as pd
from pathlib import Path
import os
import signal
import subprocess
import shutil
import numpy as np
from PIL import Image
import plotly.express as px
import yaml

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
        motilityrun,
        conversionrun,
        conversionscalevideo,
        conversionrescalemultiplier,
        segmentrun,
        wavelength,
        cellprofilerrun,
        cellprofilerpipeline,
        diagnosticdx,
        wellselection,
        volume):
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
    if conversionrescalemultiplier is None:  # If conversionrescalemultiplier is None
        conversionrescalemultiplier = 0  # Set conversionrescalemultiplier to 0

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
                "save_video": conversionscalevideo,
                "rescale_multiplier": float(conversionrescalemultiplier)
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
                                 output_path = False
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
                                  wells
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
    # Copy .HTD file into platename input dir
    shutil.copy(htd_file, platename_input_dir)

    # Iterate through each time point and copy images into new dirs
    time_points = [item for item in os.listdir(img_dir) if os.path.isdir(
        Path(img_dir, item))]

    for time_point in time_points:
        time_point_dir = Path(platename_input_dir, time_point)
        time_point_dir.mkdir(parents=True, exist_ok=True)
        if isinstance(wells, list):
            for well in wells:
                print(well)
                well_path = Path(img_dir,
                                time_point, f'{plate_base}_{well}.TIF')
                shutil.copy(well_path, time_point_dir)
        else:
            well_path = Path(img_dir,
                            time_point, f'{plate_base}_{wells}.TIF')
            shutil.copy(well_path, time_point_dir)

def create_figure_from_filepath(img_path,
                                scale = 'gray'):
    """
    This function creates a figure from the input file path.
    ===============================================================================
    Arguments:
        - img_path : str : Path to the image file
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
    """
    img = np.array(Image.open(img_path))
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