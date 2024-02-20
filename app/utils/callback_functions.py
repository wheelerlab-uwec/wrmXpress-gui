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
        if len(wellselection) == 96: # If all wells are selected
            wellselection = ['All'] # Set wellselection to 'All'
        else: # If not all wells are selected
            wellselection = wellselection # Set wellselection to the input list
    elif isinstance(wellselection, str): # If wellselection is a string
        wellselection = [wellselection] # Set wellselection to a list containing the input string

    if multiwellrows is None: # If multiwellrows is None
        multiwellrows = 0 # Set multiwellrows to 0
    if multiwellcols is None: # If multiwellcols is None
        multiwellcols = 0 # Set multiwellcols to 0
    if conversionrescalemultiplier is None: # If conversionrescalemultiplier is None
        conversionrescalemultiplier = 0 # Set conversionrescalemultiplier to 0

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