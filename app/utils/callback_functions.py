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
from skimage import exposure

########################################################################
####                                                                ####
####                          Functions                             ####
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
        else:
            output_path.mkdir(parents=True, exist_ok=True)

def copy_files_to_input_directory(
        platename_input_dir, 
        htd_file, 
        img_dir, 
        plate_base, 
        wells, 
        platename, 
        file_types=None):
    """
    The purpose of this function is to copy the input files to the input directory.
    ===============================================================================
    Arguments:
        - platename_input_dir : str : Path to the input directory
        - htd_file : str : Path to the .HTD file
        - img_dir : str : Path to the directory containing the images
        - plate_base : str : Base name of the plate
        - wells : list : List of well names
        - file_types : list : List of file extensions to consider. Example: ['.tif', '.avi']
    ===============================================================================
    Returns:
        - None
    """
    if file_types is None:
        file_types = ['.tif', '.avi', '.TIF']  # Default file types

    # Ensure wells is a list
    wells = wells if isinstance(wells, list) else [wells]
    
    if htd_file:
        shutil.copy(htd_file, platename_input_dir)
        
    try:
        time_points = [item for item in os.listdir(img_dir) if os.path.isdir(Path(img_dir, item))] if htd_file else [None]
        for time_point in time_points:
            for well in wells:
                for file_type in file_types:
                    pattern = f'{plate_base}_{well}*' if htd_file else f'{platename}_{well}*'
                    search_pattern = Path(img_dir, time_point if time_point else '', pattern + file_type)
                    for file_path in glob.glob(str(search_pattern)):
                        dest_dir = Path(platename_input_dir, time_point) if time_point else platename_input_dir
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy(file_path, dest_dir)
    except Exception as e:
        print(f"Error copying files to input directory: {e}")   

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
        motilityrun = 'no'
        conversionrun = 'no'
        segmentrun = 'no'
        cellprofilerrun = 'yes'
        diagnosticdx = 'yes'
        fecundity = 'no'
        trackingrun = 'no'
        cellprofilerpipeline = 'feeding'
        save_video ='no'
        rescale_multiplier = 0.0
        wavelength = None


    return motilityrun, conversionrun, segmentrun, cellprofilerrun, diagnosticdx, fecundity, trackingrun, cellprofilerpipeline, save_video, rescale_multiplier, wavelength

def create_figure_from_url(image_url, scale='gray'):
    """
    This function creates a Plotly figure from the input image URL.
    ===============================================================================
    Arguments:
        - image_url : str : URL to the image file
    ===============================================================================
    Returns:
        - fig : plotly.graph_objs._figure.Figure : A Plotly figure
    """
    from urllib.request import urlopen

    try:
        img = np.array(Image.open(urlopen(image_url)))

    except Exception as e:
        try:
            img = tiff.imread(urlopen(image_url))
            
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
            print(f"Error opening {image_url} with tifffile and PIL: {e}")
            return None
        
    # Now img is a numpy array, we can create a figure directly with plotly
    fig = px.imshow(img, color_continuous_scale=scale)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig
