# In[1]: Imports

import pandas as pd
from pathlib import Path
import os
import signal
import shutil
import numpy as np
from PIL import Image
import warnings
import plotly.express as px
import yaml
import glob
import imageio
import cv2
import tifffile as tiff
from skimage import exposure
from zenodo_get import zenodo_get
import subprocess
import time

# In[2]: Helper functions


def create_df_from_inputs(_rows, _cols):
    """
    This function creates a dataframe from the input rows and columns.
    """
    rows_total = list("ABCDEFGHIJKLMNOP")  # List of letters A-P
    rows = rows_total[: int(_rows)]  # List of letters A-_rows
    columns = [
        str(num).zfill(2) for num in range(1, int(_cols) + 1)
    ]  # List of numbers 01-_cols
    data = [[row + col for col in columns] for row in rows]  # List of lists of strings
    df = pd.DataFrame(data, columns=columns, index=rows)  # Create dataframe
    return df  # Return dataframe


def create_na_df_from_inputs(_rows, _cols):
    """
    This function creates an NA dataframe from the input rows and columns.
    """
    rows_total = list("ABCDEFGHIJKLMNOP")  # List of letters A-P
    rows = rows_total[: int(_rows)]  # List of letters A-_rows
    columns = [
        str(num).zfill(2) for num in range(1, int(_cols) + 1)
    ]  # List of numbers 01-_cols
    empty_data = [["NA" for _ in columns] for _ in rows]  # List of lists of None
    df = pd.DataFrame(empty_data, columns=columns, index=rows)  # Create dataframe
    return df  # Return dataframe


def eval_bool(v):
    """
    This function evaluates a boolean value from a string.
    """
    return str(v).lower() in ("yes", "true", "t", "1")


def get_default_value(param, default_value):
    """Helper function to return the default value if the param is None."""
    return param if param is not None else default_value


def prep_yaml(store_data):

    # Check if wellselection is a list or a string
    if isinstance(store_data["wrmXpress_gui_obj"]["well_selection_list"], list):
        if (
            len(store_data["wrmXpress_gui_obj"]["well_selection_list"]) == 96
        ):  # If all wells are selected
            store_data["wrmXpress_gui_obj"]["well_selection_list"] = [
                "All"
            ]  # Set wellselection to 'All'
        else:  # If not all wells are selected
            store_data["wrmXpress_gui_obj"]["well_selection_list"] = store_data[
                "wrmXpress_gui_obj"
            ][
                "well_selection_list"
            ]  # Set wellselection to the input list
    elif isinstance(
        store_data["wrmXpress_gui_obj"]["well_selection_list"], str
    ):  # If wellselection is a string
        # Set wellselection to a list containing the input string
        store_data["wrmXpress_gui_obj"]["well_selection_list"] = [
            store_data["wrmXpress_gui_obj"]["well_selection_list"]
        ]

    if store_data["wrmXpress_gui_obj"]["multi_well_row"] is None:
        store_data["wrmXpress_gui_obj"]["multi_well_row"] = 1  # Default multiwellrows
    if store_data["wrmXpress_gui_obj"]["multi_well_col"] is None:
        store_data["wrmXpress_gui_obj"]["multi_well_col"] = 1  # Default multiwellcols

    # Default xsites and ysites
    xsites = get_default_value(store_data["wrmXpress_gui_obj"]["x_sites"], "NA")
    ysites = get_default_value(store_data["wrmXpress_gui_obj"]["y_sites"], "NA")

    # Mask diameter handling
    if store_data["wrmXpress_gui_obj"]["mask"] == "circular":
        circlediameter = get_default_value(
            store_data["wrmXpress_gui_obj"]["mask_diameter"], "NA"
        )
        squarediameter = "NA"
    elif store_data["wrmXpress_gui_obj"]["mask"] == "square":
        circlediameter = "NA"
        squarediameter = get_default_value(
            store_data["wrmXpress_gui_obj"]["mask_diameter"], "NA"
        )
    else:
        circlediameter = squarediameter = "NA"
    well_row = (
        store_data["wrmXpress_gui_obj"]["well_row"]
        if store_data["wrmXpress_gui_obj"]["well_row"] is not None
        else 8
    )

    well_col = (
        store_data["wrmXpress_gui_obj"]["well_col"]
        if store_data["wrmXpress_gui_obj"]["well_col"] is not None
        else 12
    )

    # Evaluate staticdx and videodx conditions
    staticdx_dict = (
        {
            "run": eval_bool(store_data["wrmXpress_gui_obj"]["static_dx"][0]),
            "rescale_multiplier": (
                store_data["wrmXpress_gui_obj"]["static_dx_rescale"]
                if store_data["wrmXpress_gui_obj"]["static_dx_rescale"] is not None
                else 1.0
            ),
        }
        if len(store_data["wrmXpress_gui_obj"]["static_dx"]) == 1
        else {
            "run": False,
            "rescale_multiplier": 1.0,
        }
    )

    videodx_dict = (
        {
            "run": False,
            "format": "avi",
            "rescale_multiplier": 0.5,
        }
        if len(store_data["wrmXpress_gui_obj"]["video_dx"]) == 0
        else {
            "run": eval_bool(store_data["wrmXpress_gui_obj"]["video_dx"][0]),
            "format": get_default_value(
                store_data["wrmXpress_gui_obj"]["video_dx_format"], "avi"
            ),
            "rescale_multiplier": (
                store_data["wrmXpress_gui_obj"]["video_dx_rescale"]
                if store_data["wrmXpress_gui_obj"]["video_dx_rescale"] is not None
                else 0.5
            ),
        }
    )

    # Dictionary for motilityrun, segmentation, cellprofiler, etc.
    motilityrun_dict = (
        {
            "run": True,
            "wavelengths": [store_data["wrmXpress_gui_obj"]["wavelengths"]],
            "pyrScale": get_default_value(
                store_data["wrmXpress_gui_obj"]["pyrscale"], 0.5
            ),
            "levels": get_default_value(store_data["wrmXpress_gui_obj"]["levels"], 5),
            "winsize": get_default_value(
                store_data["wrmXpress_gui_obj"]["winsize"], 20
            ),
            "iterations": get_default_value(
                store_data["wrmXpress_gui_obj"]["iterations"], 7
            ),
            "poly_n": get_default_value(store_data["wrmXpress_gui_obj"]["poly_n"], 5),
            "poly_sigma": get_default_value(
                store_data["wrmXpress_gui_obj"]["poly_sigma"], 1.1
            ),
            "flags": get_default_value(store_data["wrmXpress_gui_obj"]["flags"], 0),
            "flow": "farneback",
        }
        if store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "motility"
        else {
            "run": False,
            "wavelengths": ["All"],
            "flow": "farneback",
            "pyrScale": 0.5,
            "levels": 5,
            "winsize": 20,
            "iterations": 7,
            "poly_n": 5,
            "poly_sigma": 1.1,
            "flags": 0,
        }
    )

    if (
        store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "segmentation"
        and store_data["wrmXpress_gui_obj"]["type_segmentation"]
        == "python"
    ):
        segmentation_dict = {
            "run": True,
            "model": get_default_value(
                store_data["wrmXpress_gui_obj"]["cellpose_model_segmentation"],
                "20220830_all",
            ),
            "model_type": get_default_value(
                store_data["wrmXpress_gui_obj"]["type_segmentation"],
                "cellpose",
            ),
            "sigma": get_default_value(
                store_data["wrmXpress_gui_obj"]["python_model_sigma"], 0.25
            ),
            "wavelengths": [
                get_default_value(
                    store_data["wrmXpress_gui_obj"]["wavelengths_segmentation"], "All"
                )
            ],
        }

    else:
        segmentation_dict = (
            {
                "run": True,
                "model": get_default_value(
                    store_data["wrmXpress_gui_obj"]["cellpose_model_segmentation"],
                    "20220830_all",
                ),
                "model_type": get_default_value(
                    store_data["wrmXpress_gui_obj"]["type_segmentation"],
                    "cellpose",
                ),
                "sigma": 0.25,
                "wavelengths": [
                    get_default_value(
                        store_data["wrmXpress_gui_obj"]["wavelengths_segmentation"],
                        "All",
                    )
                ],
            }
            if store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "segmentation"
            else {
                "run": False,
                "model": "20220830_all",
                "model_type": "cellpose",
                "sigma": 0.25,
                "wavelengths": ["All"],
            }
        )

    cellprofiler_dict = (
        {
            "run": True,
            "cellpose_model": get_default_value(
                store_data["wrmXpress_gui_obj"]["cellpose_model_cellprofiler"],
                "20220830_all",
            ),
            "cellpose_wavelength": get_default_value(
                store_data["wrmXpress_gui_obj"]["wavelengths_cellprofiler"], "All"
            ),
            "pipeline": get_default_value(
                store_data["wrmXpress_gui_obj"]["cellprofiler_pipeline_selection"],
                "wormsize_intensity_cellpose",
            ),
        }
        if store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "cellprofiler"
        else {
            "run": False,
            "cellpose_model": "20220830_all",
            "cellpose_wavelength": "All",
            "pipeline": "wormsize_intensity_cellpose",
        }
    )

    trackingrun_dict = (
        {
            "run": True,
            "wavelengths": get_default_value(
                store_data["wrmXpress_gui_obj"]["wavelengths_tracking"], ["All"]
            ),
            "diameter": get_default_value(
                store_data["wrmXpress_gui_obj"]["tracking_diameter"], 35
            ),
            "minmass": get_default_value(
                store_data["wrmXpress_gui_obj"]["tracking_minmass"], 1200
            ),
            "noisesize": get_default_value(
                store_data["wrmXpress_gui_obj"]["tracking_noisesize"], 2
            ),
            "search_range": get_default_value(
                store_data["wrmXpress_gui_obj"]["tracking_searchrange"], 45
            ),
            "memory": get_default_value(
                store_data["wrmXpress_gui_obj"]["tracking_memory"], 25
            ),
            "adaptive_stop": get_default_value(
                store_data["wrmXpress_gui_obj"]["tracking_adaptivestop"], 30
            ),
        }
        if store_data["wrmXpress_gui_obj"]["pipeline_selection"] == "tracking"
        else {
            "run": False,
            "wavelengths": ["All"],
            "diameter": 35,
            "minmass": 1200,
            "noisesize": 2,
            "search_range": 45,
            "memory": 25,
            "adaptive_stop": 30,
        }
    )

    if store_data["wrmXpress_gui_obj"]["imaging_mode"] == "single-well":
        store_data["wrmXpress_gui_obj"]["multi_well_row"] = 1
        store_data["wrmXpress_gui_obj"]["multi_well_col"] = 1
        store_data["wrmXpress_gui_obj"]["multi_well_detection"] = "grid"
        xsites = "NA"
        ysites = "NA"
        store_data["wrmXpress_gui_obj"]["stitch_switch"] = False

    elif store_data["wrmXpress_gui_obj"]["imaging_mode"] == "multi-well":
        store_data["wrmXpress_gui_obj"]["multi_well_detection"] = "grid"
        store_data["wrmXpress_gui_obj"]["stitch_switch"] = False
        xsites = "NA"
        ysites = "NA"

    elif store_data["wrmXpress_gui_obj"]["imaging_mode"] == "multi-site":
        store_data["wrmXpress_gui_obj"]["multi_well_detection"] = "grid"
        store_data["wrmXpress_gui_obj"]["multi_well_row"] = 1
        store_data["wrmXpress_gui_obj"]["multi_well_col"] = 1
        store_data["wrmXpress_gui_obj"]["stitch_switch"] = (
            False if store_data["wrmXpress_gui_obj"]["stitch_switch"] == None else True
        )

    # Final YAML dictionary construction
    yaml_dict = {
        "imaging_mode": [store_data["wrmXpress_gui_obj"]["imaging_mode"]],
        "file_structure": [store_data["wrmXpress_gui_obj"]["file_structure"]],
        "well-row": well_row,
        "well-col": well_col,
        "multi-well-row": int(store_data["wrmXpress_gui_obj"]["multi_well_row"]),
        "multi-well-col": int(store_data["wrmXpress_gui_obj"]["multi_well_col"]),
        "multi-well-detection": store_data["wrmXpress_gui_obj"]["multi_well_detection"],
        "x-sites": xsites,
        "y-sites": ysites,
        "stitch": store_data["wrmXpress_gui_obj"]["stitch_switch"],
        "circle_diameter": circlediameter,
        "square_side": squarediameter,
        "pipelines": {
            "statix_dx": staticdx_dict,
            "video-dx": videodx_dict,
            "optical_flow": motilityrun_dict,
            "segmentation": segmentation_dict,
            "cellprofiler": cellprofiler_dict,
            "tracking": trackingrun_dict,
        },
        "wells": store_data["wrmXpress_gui_obj"]["well_selection_list"],
        "directories": {
            "work": [
                str(Path(store_data["wrmXpress_gui_obj"]["mounted_volume"], "work"))
            ],
            "input": [
                str(Path(store_data["wrmXpress_gui_obj"]["mounted_volume"], "input"))
            ],
            "output": [
                str(Path(store_data["wrmXpress_gui_obj"]["mounted_volume"], "output"))
            ],
        },
    }

    return yaml_dict


def get_diameters(mask, maskdiameter, circlediameter=None, squarediameter=None):
    """Get the diameters for the mask type."""
    if mask == "circular":
        circlediameter = circlediameter if circlediameter is not None else maskdiameter
        squarediameter = "NA"
    elif mask == "square":
        circlediameter = "NA"
        squarediameter = squarediameter if squarediameter is not None else maskdiameter
    elif mask == "NA":
        circlediameter = "NA"
        squarediameter = "NA"
    return circlediameter, squarediameter


def send_ctrl_c(pid):
    """
    Sends a SIGINT signal to the process with the given PID.
    """

    try:
        os.killpg(os.getpgid(pid), signal.SIGINT)
        print("Control + C", "wrmxpress analysis cancelled")
    except ProcessLookupError:
        print("Process with PID", pid, "not found.")


def clean_and_create_directories(input_path, work_path, output_path=False):
    """
    The purpose of this function is to clean and create the input, work, and output directories.
    That is to say, it will delete the contents of the input, work, and output directories (if they exist)
    and then recreate them.
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
                    print("Failed to delete %s because %s" % (file_path, e))
        else:
            output_path.mkdir(parents=True, exist_ok=True)


def copy_files_to_input_directory(
    platename_input_dir,
    htd_file,
    img_dir,
    plate_base,
    wells,
    platename,
    file_structure,
    file_types=None,
):
    """
    The purpose of this function is to copy the input files to the input directory.
    """
    if file_types is None:
        file_types = [".tif", ".avi", ".TIF"]  # Default file types

    # Ensure wells is a list
    wells = wells if isinstance(wells, list) else [wells]

    if htd_file:
        shutil.copy(htd_file, platename_input_dir)

    try:
        if file_structure == "imagexpress":
            time_points = (
                [
                    item
                    for item in os.listdir(img_dir)
                    if os.path.isdir(Path(img_dir, item))
                ]
                if htd_file
                else [None]
            )
            for time_point in time_points:
                for well in wells:
                    for file_type in file_types:
                        pattern = (
                            f"{plate_base}_{well}*"
                            if htd_file
                            else f"{platename}_{well}*"
                        )
                        search_pattern = Path(
                            img_dir,
                            time_point if time_point else "",
                            pattern + file_type,
                        )
                        for file_path in glob.glob(str(search_pattern)):
                            dest_dir = (
                                Path(platename_input_dir, time_point)
                                if time_point
                                else platename_input_dir
                            )
                            dest_dir.mkdir(parents=True, exist_ok=True)
                            shutil.copy(file_path, dest_dir)
        elif file_structure == "avi":
            # One AVI for a whole plate
            if Path(img_dir, f"{plate_base}.avi").exists():
                dest_dir = platename_input_dir
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy(Path(img_dir, f"{plate_base}.avi"), dest_dir)
            # One AVI per well
            else:
                for well in wells:
                    for file_type in file_types:
                        pattern = (
                                f"{plate_base}_{well}*"
                                if htd_file
                                else f"{platename}_{well}*"
                            )
                        search_pattern = Path(
                                img_dir,
                                pattern + file_type,
                            )
                        for file_path in glob.glob(str(search_pattern)):
                                dest_dir = (
                                    Path(platename_input_dir)
                                )
                                dest_dir.mkdir(parents=True, exist_ok=True)
                                shutil.copy(file_path, dest_dir)
    except Exception as e:
        print(f"Error copying files to input directory: {e}")


def create_figure_from_filepath(img_path, scale="gray", max_pixels=178956970):
    """
    This function creates a figure from the input file path.
    If the image size exceeds `max_pixels`, it is resized.
    """

    img = None
    img_extension = Path(img_path).suffix.lower()

    warnings.filterwarnings("ignore", category=Image.DecompressionBombWarning)
    Image.MAX_IMAGE_PIXELS = 1000000000  # Increase the limit to 1 billion pixels

    # Try opening the image with PIL

    try:
        img = Image.open(img_path)
        # Calculate thumbnail size to limit memory use but maintain aspect ratio
        if img.width * img.height > max_pixels:
            scale = (max_pixels / (img.width * img.height)) ** 0.5
            thumbnail_size = (int(img.width * scale), int(img.height * scale))
            img.thumbnail(thumbnail_size, Image.LANCZOS)
        img = np.array(img)
    except Exception as e:
        print(f"Error opening {img_path} with PIL: {e}")

    # Try opening with OpenCV if PIL fails
    if img is None and img_extension not in [".tif", ".tiff"]:
        try:
            img = cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)  # Read image as-is
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        except Exception as e:
            print(f"Error opening {img_path} with OpenCV: {e}")

    # Try opening with imageio if OpenCV fails
    # if img is None:
    #     try:
    #         img = np.array(imageio.imread(img_path))
    #     except Exception as e:
    #         print(f"Error opening {img_path} with imageio: {e}")

    # Try opening with tifffile if all else fails
    if img is None:
        try:
            img = tiff.imread(img_path)
            # Handle 3D shape if necessary
            if len(img.shape) == 3 and img.shape[2] == 2:
                img = img[:, :, 0]
            if img.dtype != np.uint8:
                img = exposure.rescale_intensity(img, out_range=(0, 255)).astype(
                    np.uint8
                )
        except Exception as e:
            print(f"Error opening {img_path} with tifffile: {e}")
            return None

    # Check image size and resize if necessary
    total_pixels = img.shape[0] * img.shape[1]
    if total_pixels > max_pixels:
        scaling_factor = (max_pixels / total_pixels) ** 0.5
        new_size = (
            int(img.shape[1] * scaling_factor),
            int(img.shape[0] * scaling_factor),
        )
        print(f"Resizing image to {new_size} due to size {total_pixels} > {max_pixels}")
        img = np.array(Image.fromarray(img).resize(new_size, Image.ANTIALIAS))

    # Proceed with creating the figure using plotly
    fig = px.imshow(img, color_continuous_scale=scale)
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig


def update_yaml_file(input_full_yaml, output_full_yaml, updates):
    """
    This function updates the YAML file with the specified updates.
    """
    # reading in yaml file
    with open(input_full_yaml, "r") as file:
        data = yaml.safe_load(file)

    # replace the YAML config option with ['All'] as a workaround for wrmXpress bug
    # instead, we'll copy the selected files to input and analyze all of them
    # Update data based on the updates dict
    for key, value in updates.items():
        data[key] = value

    with open(output_full_yaml, "w") as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)


def zenodo_get_id(selected_plates):
    # Zenodo record ID (DOI can be used for reference but Zenodo ID is used for fetching)
    zenodo_record_id = "12760651"  # Replace with your Zenodo record ID

    downloads_path = Path("/home/", "downloads")
    downloads_path.mkdir(parents=True, exist_ok=True)

    # Change the working directory to Downloads
    os.chdir(downloads_path)

    # Loop over selected plates and download specific files
    for plate in selected_plates:
        # Construct the glob pattern for each plate
        if plate == "20220527-p02-KTR" or plate == "20220622-p02-KTR":
            file_pattern = f"{plate}.avi"
        else:
            file_pattern = f"{plate}.zip"

        print(f"Attempting to download file: {file_pattern}")  # For debugging purposes

        try:
            # Run zenodo_get with glob pattern to download the specific file
            subprocess.run(
                [
                    "zenodo_get",
                    zenodo_record_id,  # Use the record ID
                    "-g",
                    file_pattern,  # Use the glob pattern to specify the file
                ],
                check=True,  # This ensures an error is raised if the command fails
            )

        except subprocess.CalledProcessError as e:
            print(f"Error downloading {plate}: {str(e)}")

    return "Download complete!"


def construct_img_path(volume, selection, plate_base, wells, wavelength):
    """Construct the image path based on selection."""
    if selection == "straightened_worms":
        return Path(
            f"{volume}/output/cellprofiler/img/{plate_base}_{wells[0]}_{wavelength}.tiff"
        )
    selection_normalized = "_".join(selection.lower().split())
    base_path = Path(
        f"{volume}/output/{selection_normalized}/{plate_base}_{wavelength}"
    )
    # Attempt to find a valid file with supported extensions
    return next(base_path.parent.glob(f"{base_path.stem}.*"), None)


def wait_for_file(file_path, timeout=30, interval=1):
    """
    Waits for the specified file to be created, checking at given intervals.

    Parameters:
    - file_path (Path): The path of the file to wait for.
    - timeout (int): Maximum time in seconds to wait.
    - interval (int): Time interval in seconds between checks.

    Returns:
    - bool: True if file is found, False if timeout occurs.
    """
    start_time = time.time()
    while not file_path.exists():
        if time.time() - start_time > timeout:
            # print(f"Timeout: {file_path} not found after {timeout} seconds.")
            return False
        time.sleep(interval)
    return True
