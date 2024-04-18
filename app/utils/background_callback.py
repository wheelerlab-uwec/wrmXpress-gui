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

from app.utils.callback_functions import create_figure_from_filepath
from app.utils.callback_functions import (
    update_yaml_file,
    clean_and_create_directories,
    copy_files_to_input_directory,
)

########################################################################
####                                                                ####
####                       Function                                 ####
####                                                                ####
########################################################################


def callback(set_progress, n_clicks, store):
    """
    This function is used for the callback function in the app.py file. The
    purpose of this function is to run the wrmXpress pipeline based on the
    pipeline selection and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - set_progress : function : The function to set the progress
            +- see app.py for more information
        - n_clicks : int : The number of clicks from the submit button on the run page
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
    ===============================================================================
    Returns:
        - functions : function : The function to run the wrmXpress pipeline depending on the pipeline selection
            +- these funcitons are defined in this file, see below for more details
    ===============================================================================
    """
    try:

        # Check if store is empty
        if not store:
            return (
                {},
                True,
                True,
                "No configuration found. Please go to the configuration page to set up the analysis.",
                "No configuration found. Please go to the configuration page to set up the analysis.",
            )

        # obtain the necessary data from the store
        pipeline_selection = store["pipeline_selection"]

        # Check if the submit button has been clicked
        if n_clicks:
            if pipeline_selection == "tracking":

                return tracking_wrmXpress_run(store, set_progress)

            elif pipeline_selection == "motility":

                return motility_or_segment_run(store, set_progress)

            elif pipeline_selection == "fecundity":

                return fecundity_run(store, set_progress)

            elif pipeline_selection == "wormsize_intensity_cellpose":

                return cellprofile_wormsize_intesity_cellpose_run(store, set_progress)

            elif pipeline_selection == "mf_celltox":

                return cellprofile_mf_celltox_run(store, set_progress)

            elif pipeline_selection == "feeding":

                return cellprofile_feeding_run(store, set_progress)

            elif pipeline_selection == "wormsize":

                return cellprofile_wormsize_run(store, set_progress)

    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


########################################################################
####                                                                ####
####                       app.py functions                         ####
####                                                                ####
########################################################################


def preamble_run_wrmXpress_avi_selection(store):
    """
    The purpose of this function is to prepare the necessary files and directories for wrmXpress for avi files.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
    ===============================================================================
    Returns:
        - new_store : dict : The updated store data
            +- wrmxpress_command_split : list : wrmXpress command
            +- output_folder : str : Path to the output folder
            +- output_file : str : Path to the output file
            +- command_message : str : A command message for the user
            +- wells : list : List of wells
            +- volume : str : Path to the volume
            +- platename : str : Name of the plate
            +- wells_analyzed : list : List of wells analyzed
            +- tracking_well : list : List of tracking wells
    ===============================================================================
    """
    volume = store["mount"]
    platename = store["platename"]
    wells = store["wells"]

    # necessary file paths
    img_dir = Path(volume, platename)
    input_dir = Path(volume, "input")
    platename_input_dir = Path(input_dir, platename)
    full_yaml = Path(volume, platename + ".yml")

    update_yaml_file(full_yaml, full_yaml, {"wells": ["All"]})

    # clean and create directories
    clean_and_create_directories(
        input_path=Path(volume, "input", platename),
        work_path=Path(volume, "work", platename),
        output_path=Path(volume, "output"),
    )

    copy_files_to_input_directory(
        platename_input_dir=platename_input_dir,
        htd_file=None,
        img_dir=img_dir,
        wells=wells,
        plate_base=None,
        platename=platename,
    )

    # Command message
    command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

    wrmxpress_command = (
        f"python -u wrmXpress/wrapper.py {volume}/{platename}.yml {platename}"
    )
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_folder = Path(volume, "work", platename)
    output_file = Path(
        volume, "work", platename, f"{platename}_run.log"
    )  # Specify the name and location of the output file
    wells_analyzed = []
    tracking_well = []

    new_store = {
        "wrmxpress_command_split": wrmxpress_command_split,
        "output_folder": output_folder,
        "output_file": output_file,
        "command_message": command_message,
        "wells": wells,
        "volume": volume,
        "platename": platename,
        "wells_analyzed": wells_analyzed,
        "tracking_well": tracking_well,
    }
    return new_store


def preamble_run_wrmXpress_imagexpress_selection(store):
    """
    The purpose of this function is to prepare the necessary files and directories for wrmXpress for imagexpress formatted files.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
    ===============================================================================
    Returns:
        - new_store : dict : The updated store data
            +- wrmxpress_command_split : list : wrmXpress command
            +- output_folder : str : Path to the output folder
            +- output_file : str : Path to the output file
            +- command_message : str : A command message for the user
            +- wells : list : List of wells
            +- volume : str : Path to the volume
            +- platename : str : Name of the plate
            +- wells_analyzed : list : List of wells analyzed
            +- tracking_well : list : List of tracking wells
    ===============================================================================
    """
    volume = store["mount"]
    platename = store["platename"]
    wells = store["wells"]
    plate_base = platename.split("_", 1)[0]

    # necessary file paths
    img_dir = Path(volume, platename)
    input_dir = Path(volume, "input")
    platename_input_dir = Path(input_dir, platename)
    full_yaml = Path(volume, platename + ".yml")

    update_yaml_file(full_yaml, full_yaml, {"wells": ["All"]})

    # clean and create directories
    clean_and_create_directories(
        input_path=Path(volume, "input", platename),
        work_path=Path(volume, "work", platename),
        output_path=Path(volume, "output"),
    )

    htd_file = Path(img_dir, f"{plate_base}.HTD")

    copy_files_to_input_directory(
        platename_input_dir=platename_input_dir,
        htd_file=htd_file,
        img_dir=img_dir,
        wells=wells,
        plate_base=plate_base,
        platename=platename,
    )
    # Command message
    command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

    wrmxpress_command = (
        f"python -u wrmXpress/wrapper.py {volume}/{platename}.yml {platename}"
    )
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_folder = Path(volume, "work", platename)
    output_file = Path(
        volume, "work", platename, f"{platename}_run.log"
    )  # Specify the name and location of the output file
    wells_analyzed = []
    tracking_well = []

    new_store = {
        "wrmxpress_command_split": wrmxpress_command_split,
        "output_folder": output_folder,
        "output_file": output_file,
        "command_message": command_message,
        "wells": wells,
        "volume": volume,
        "platename": platename,
        "wells_analyzed": wells_analyzed,
        "tracking_well": tracking_well,
    }
    return new_store


def tracking_wrmXpress_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for tracking and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
        - set_progress : function : Function to set the progress
    ===============================================================================
    set_progress: for more information see app.py
        - progress bar value : int : The progress bar value
        - progress bar max : int : The progress bar max
        - image analysis preview : dict : The image analysis preview
        - progress message run page for analysis : str : The progress message run page for analysis
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)
            return run_wrmXpress_avi_selection_tracking(new_store, set_progress)
        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)
            return run_wrmXpress_imagexpress_selection_tracking(new_store, set_progress)
    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


def motility_or_segment_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for motility and segment and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
        - set_progress : function : Function to set the progress
    ===============================================================================
    set_progress: for more information see app.py
        - progress bar value : int : The progress bar value
        - progress bar max : int : The progress bar max
        - image analysis preview : dict : The image analysis preview
        - progress message run page for analysis : str : The progress message run page for analysis
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)
            return run_wrmXpress_avi_selection_motility(new_store, set_progress)

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)
            return run_wrmXpress_imagexpress_selection_motility(new_store, set_progress)

    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


def fecundity_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for fecundity and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
        - set_progress : function : Function to set the progress
    ===============================================================================
    set_progress: for more information see app.py
        - progress bar value : int : The progress bar value
        - progress bar max : int : The progress bar max
        - image analysis preview : dict : The image analysis preview
        - progress message run page for analysis : str : The progress message run page for analysis
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_folder = new_store["output_folder"]
        output_file = new_store["output_file"]
        wells = new_store["wells"]
        volume = new_store["volume"]
        platename = new_store["platename"]
        plate_base = platename.split("_", 1)[0]

        while not os.path.exists(output_folder):
            time.sleep(1)

        with open(output_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            print("Running wrmXpress.")

            docker_output = []
            wells_analyzed = []
            wells_to_be_analyzed = len(wells)

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                if "Generating w1 thumbnails" in line:

                    output_path = Path(volume, "output", "thumbs", platename + ".png")
                    while not os.path.exists(output_path):
                        time.sleep(1)

                    fig_1 = create_figure_from_filepath(output_path)

                    print("wrmXpress has finished.")
                    docker_output.append("wrmXpress has finished.")
                    docker_output_formatted = "".join(docker_output)

                    return fig_1, False, False, "", f"```{docker_output_formatted}```"

                elif "Running" in line:
                    well_running = line.split(" ")[
                        -1
                    ].strip()  # Use strip() to remove '\n'
                    if well_running not in wells_analyzed:
                        wells_analyzed.append(well_running)
                        well_base_path = Path(
                            volume,
                            f"{platename}/TimePoint_1/{plate_base}_{well_running}",
                        )
                        # Use rglob with case-insensitive pattern matching for .TIF and .tif
                        file_paths = list(
                            well_base_path.parent.rglob(
                                well_base_path.name + "*[._][tT][iI][fF]"
                            )
                        )

                        # Sort the matching files to find the one with the lowest suffix number
                        if file_paths:
                            file_paths_sorted = sorted(file_paths, key=lambda x: x.stem)
                            # Select the first file (with the lowest number) if multiple matches are found
                            img_path = file_paths_sorted[0]
                        else:
                            # Fallback if no matching files are found
                            img_path = well_base_path.with_suffix(
                                ".TIF"
                            )  # Default to .TIF if no files found

                        fig = create_figure_from_filepath(img_path)

                        docker_output_formatted = "".join(docker_output)
                        set_progress(
                            (
                                str(len(wells_analyzed)),
                                str(wells_to_be_analyzed),
                                fig,
                                f"```{img_path}```",
                                f"```{docker_output_formatted}```",
                            )
                        )
    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


def cellprofile_wormsize_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for wormsize and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
        - set_progress : function : Function to set the progress
    ===============================================================================
    set_progress: for more information see app.py
        - progress bar value : int : The progress bar value
        - progress bar max : int : The progress bar max
        - image analysis preview : dict : The image analysis preview
        - progress message run page for analysis : str : The progress message run page for analysis
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_folder = new_store["output_folder"]
        output_file = new_store["output_file"]
        wells = new_store["wells"]
        volume = new_store["volume"]
        platename = new_store["platename"]
        plate_base = platename.split("_", 1)[0]
        pipeline_selection = store["pipeline_selection"]

        while not os.path.exists(output_folder):
            time.sleep(1)

        with open(output_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            docker_output = []

            print("Running wrmXpress.")

            wells_to_be_analyzed = len(wells)
            progress = 0
            total_progress = wells_to_be_analyzed

            for line in iter(process.stdout.readline, b""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                if "Generating w1 thumbnails" in line:
                    output_path = Path(volume, "output", "thumbs", platename + ".png")
                    while not os.path.exists(output_path):
                        time.sleep(1)

                    fig_1 = create_figure_from_filepath(output_path)
                    print("wrmXpress has finished.")
                    docker_output.append("wrmXpress has finished.")
                    docker_output_formatted = "".join(docker_output)
                    return fig_1, False, False, f"", f"```{docker_output_formatted}```"

                elif "Image #" in line:
                    csv_file_path = Path(
                        volume, "input", f"image_paths_{pipeline_selection}.csv"
                    )
                    while not os.path.exists(csv_file_path):
                        time.sleep(1)

                    read_csv = pd.read_csv(csv_file_path)
                    well_column = read_csv["Metadata_Well"]

                    image_number_pattern = re.search(r"Image # (\d+)", line)
                    if image_number_pattern:
                        image_number_pattern
                        image_number = int(image_number_pattern.group(1))
                        well_id = well_column.iloc[image_number - 1]
                        img_path = Path(
                            volume,
                            f"input/{platename}/TimePoint_1/{plate_base}_{well_id}.TIF",
                        )

                        if img_path.exists():
                            fig = create_figure_from_filepath(img_path)
                            progress += 1
                            docker_output_formatted = "".join(docker_output)
                            set_progress(
                                (
                                    (image_number),
                                    str(total_progress),
                                    fig,
                                    f"```{img_path}```",
                                    f"```{docker_output_formatted}```",
                                )
                            )
    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


def cellprofile_wormsize_intesity_cellpose_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for wormsize_intensity_cellpose and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
        - set_progress : function : Function to set the progress
    ===============================================================================
    set_progress: for more information see app.py
        - progress bar value : int : The progress bar value
        - progress bar max : int : The progress bar max
        - image analysis preview : dict : The image analysis preview
        - progress message run page for analysis : str : The progress message run page for analysis
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_folder = new_store["output_folder"]
        output_file = new_store["output_file"]
        wells = new_store["wells"]
        volume = new_store["volume"]
        platename = new_store["platename"]
        plate_base = platename.split("_", 1)[0]
        pipeline_selection = store["pipeline_selection"]

        while not os.path.exists(output_folder):
            time.sleep(1)

        with open(output_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            print("Running wrmXpress.")

            docker_output = []
            wells_to_be_analyzed = len(wells)
            progress = 0
            total_progress = 2 * wells_to_be_analyzed

            for line in iter(process.stdout.readline, b""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                if "Generating w1 thumbnails" in line:
                    output_path = Path(volume, "output", "thumbs", platename + ".png")
                    while not os.path.exists(output_path):
                        time.sleep(1)

                    fig_1 = create_figure_from_filepath(output_path)
                    print("wrmXpress has finished.")
                    docker_output.append("wrmXpress has finished.")
                    docker_output_formatted = "".join(docker_output)
                    return fig_1, False, False, f"", f"```{docker_output_formatted}```"

                elif "Image #" in line:
                    csv_file_path = Path(
                        volume, "input", f"image_paths_{pipeline_selection}.csv"
                    )
                    while not os.path.exists(csv_file_path):
                        time.sleep(1)

                    read_csv = pd.read_csv(csv_file_path)
                    well_column = read_csv["Metadata_Well"]

                    image_number_pattern = re.search(r"Image # (\d+)", line)
                    if image_number_pattern:
                        image_number = int(image_number_pattern.group(1))
                        well_id = well_column.iloc[image_number - 1]
                        img_path = Path(
                            volume,
                            f"input/{platename}/TimePoint_1/{plate_base}_{well_id}.TIF",
                        )
                        if img_path.exists():
                            fig = create_figure_from_filepath(img_path)
                            progress += 1
                            docker_output_formatted = "".join(docker_output)
                            set_progress(
                                (
                                    str(len(wells) + image_number),
                                    str(total_progress),
                                    fig,
                                    f"```{img_path}```",
                                    f"```{docker_output_formatted}```",
                                )
                            )

                elif "[INFO]" in line and "%" in line:
                    info_parts = line.split("/")
                    info_well_analyzed = info_parts[0].split(" ")[-1]
                    info_total_wells = info_parts[1].split(" ")[0]

                    if info_well_analyzed == info_total_wells:
                        current_well = wells[int(info_well_analyzed) - 1]
                        img_path = Path(
                            volume,
                            f"input/{platename}/TimePoint_1/{plate_base}_{current_well}.TIF",
                        )
                        if os.path.exists(img_path):
                            fig = create_figure_from_filepath(img_path)
                            docker_output_formatted = "".join(docker_output)
                            set_progress(
                                (
                                    str(progress),
                                    str(total_progress),
                                    fig,
                                    f"```{img_path}```",
                                    f"```{docker_output_formatted}```",
                                )
                            )
                    else:
                        current_well = wells[int(info_well_analyzed)]
                        img_path = Path(
                            volume,
                            f"input/{platename}/TimePoint_1/{plate_base}_{current_well}.TIF",
                        )
                        if os.path.exists(img_path):
                            fig = create_figure_from_filepath(img_path, "gray")
                            docker_output_formatted = "".join(docker_output)
                            progress += 1
                            set_progress(
                                (
                                    str(progress),
                                    str(total_progress),
                                    fig,
                                    f"```{img_path}```",
                                    f"```{docker_output_formatted}```",
                                )
                            )
    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


def cellprofile_mf_celltox_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for mf_celltox and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
        - set_progress : function : Function to set the progress
    ===============================================================================
    set_progress: for more information see app.py
        - progress bar value : int : The progress bar value
        - progress bar max : int : The progress bar max
        - image analysis preview : dict : The image analysis preview
        - progress message run page for analysis : str : The progress message run page for analysis
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_folder = new_store["output_folder"]
        output_file = new_store["output_file"]
        wells = new_store["wells"]
        volume = new_store["volume"]
        platename = new_store["platename"]
        plate_base = platename.split("_", 1)[0]
        pipeline_selection = store["pipeline_selection"]

        while not os.path.exists(output_folder):
            time.sleep(1)

        with open(output_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            docker_output = []

            print("Running wrmXpress.")

            for line in iter(process.stdout.readline, b""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                csv_file_path = Path(
                    volume, "input", f"image_paths_{pipeline_selection}.csv"
                )
                while not os.path.exists(csv_file_path):
                    time.sleep(1)

                read_csv = pd.read_csv(csv_file_path)
                well_column = read_csv["Metadata_Well"]

                if "Generating w1 thumbnails" in line:
                    output_path = Path(volume, "output", "thumbs", platename + ".png")
                    while not os.path.exists(output_path):
                        time.sleep(1)

                    fig_1 = create_figure_from_filepath(output_path)

                    print("wrmXpress has finished.")
                    docker_output.append("wrmXpress has finished.")
                    docker_output_formatted = "".join(docker_output)
                    return fig_1, False, False, "", f"```{docker_output_formatted}```"

                elif "Image #" in line:
                    image_number_pattern = re.search(r"Image # (\d+)", line)
                    if image_number_pattern:

                        image_number = int(image_number_pattern.group(1))
                        try:
                            well_id = well_column.iloc[image_number - 1]
                        except IndexError:
                            well_id = well_column.iloc[0]

                        img_path = Path(
                            volume,
                            f"input/{platename}/TimePoint_1/{plate_base}_{well_id}_s1.TIF",
                        )
                        if img_path.exists():
                            fig = create_figure_from_filepath(img_path)
                            docker_output_formatted = "".join(docker_output)
                            set_progress(
                                (
                                    str(image_number),
                                    str(len(wells)),
                                    fig,
                                    f"```{img_path}```",
                                    f"```{docker_output_formatted}```",
                                )
                            )
    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


def cellprofile_feeding_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for feeding and return the figure, open status, and command message.
    ===============================================================================
    Arguments:
        - store : dict : The store data
            +- this data is generated from the configure page. see app/pages/configure.py for more details
        - set_progress : function : Function to set the progress
    ===============================================================================
    set_progress: for more information see app.py
        - progress bar value : int : The progress bar value
        - progress bar max : int : The progress bar max
        - image analysis preview : dict : The image analysis preview
        - progress message run page for analysis : str : The progress message run page for analysis
    ===============================================================================
    Returns:
        - fig : matplotlib.figure.Figure : A figure
        - open_status : bool : Open status of the alerts
        - command_message : str : A command message
    ===============================================================================
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_folder = new_store["output_folder"]
        output_file = new_store["output_file"]
        wells = new_store["wells"]
        volume = new_store["volume"]
        platename = new_store["platename"]
        plate_base = platename.split("_", 1)[0]
        pipeline_selection = store["pipeline_selection"]

        while not os.path.exists(output_folder):
            time.sleep(1)

        with open(output_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            docker_output = []

            print("Running wrmXpress.")

            for line in iter(process.stdout.readline, b""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                csv_file_path = Path(
                    volume, "input", f"image_paths_{pipeline_selection}.csv"
                )
                while not os.path.exists(csv_file_path):
                    time.sleep(1)

                read_csv = pd.read_csv(csv_file_path)
                well_column = read_csv["Metadata_Well"]

                if "Generating w1 thumbnails" in line:
                    output_path = Path(
                        volume, "output", "thumbs", platename + "_w1" + ".png"
                    )
                    while not os.path.exists(output_path):
                        time.sleep(1)

                    fig_1 = create_figure_from_filepath(output_path)
                    print("wrmXpress has finished.")
                    docker_output.append("wrmXpress has finished.")
                    docker_output_formatted = "".join(docker_output)
                    return fig_1, False, False, "", f"```{docker_output_formatted}```"

                elif "Image #" in line:
                    image_number_pattern = re.search(r"Image # (\d+)", line)
                    if image_number_pattern:
                        image_number = int(image_number_pattern.group(1))
                        well_id = well_column.iloc[image_number - 1]

                        img_path = Path(
                            volume,
                            f"input/{platename}/TimePoint_1/{plate_base}_{well_id}_w1.TIF",
                        )
                        if img_path.exists():
                            fig = create_figure_from_filepath(img_path)
                            docker_output_formatted = "".join(docker_output)
                            set_progress(
                                (
                                    str(image_number),
                                    str(len(wells)),
                                    fig,
                                    f"```{img_path}```",
                                    f"```{docker_output_formatted}```",
                                )
                            )
    except Exception as e:
        # Log the error to your output file or a dedicated log file
        error_message = f"An error occurred: {str(e)}"

        # Return an error indication to the callback
        return (
            {},
            True,
            True,
            "An error has occurred. Please see the log file for more information.",
            f"```{error_message}```",
        )


def run_wrmXpress_avi_selection_tracking(new_store, set_progress):
    wrmxpress_command_split = new_store["wrmxpress_command_split"]
    output_folder = new_store["output_folder"]
    output_file = new_store["output_file"]
    wells = new_store["wells"]
    volume = new_store["volume"]
    platename = new_store["platename"]
    wells_analyzed = new_store["wells_analyzed"]
    tracking_well = new_store["tracking_well"]

    while not os.path.exists(output_folder):
        time.sleep(1)
    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("Running wrmXpress.")
        # Create an empty list to store the docker output
        docker_output = []
        for line in iter(process.stdout.readline, b""):
            # Add the line to docker_output for further processing
            docker_output.append(line)
            file.write(line)
            file.flush()
            if "Generating w1 thumbnails" in line:
                tracks_file_path = Path(
                    volume, "output", "thumbs", f"{platename}_tracks.png"
                )
                while not os.path.exists(tracks_file_path):
                    time.sleep(1)
                # create figure from file path
                fig_1 = create_figure_from_filepath(tracks_file_path)
                docker_output_formatted = "".join(docker_output)
                print("wrmXpress is finished")
                docker_output.append("wrmXpress is finished")
                docker_output_formatted = "".join(docker_output)
                return fig_1, False, False, f"", f"```{docker_output_formatted}```"

            elif "Reconfiguring" in line:
                # find the well that is being analyzed
                current_well = line.split(".")[0].split("_")[-1]
                # add the well to the list of wells analyzed if it is not already there
                if current_well not in wells_analyzed:
                    wells_analyzed.append(current_well)
                # obtain file path to current well
                current_well_path = Path(
                    volume,
                    "input",
                    platename,
                    "TimePoint_1",
                    f"{platename}_{wells_analyzed[-1]}.TIF",
                )
                # ensure file path exists
                while not os.path.exists(current_well_path):
                    time.sleep(1)
                # create figure from file path
                fig = create_figure_from_filepath(current_well_path)
                docker_output_formatted = "".join(docker_output)
                set_progress(
                    (
                        str(len(wells_analyzed)),
                        str(2 * len(wells)),
                        fig,
                        f"```{current_well_path}```",
                        f"```{docker_output_formatted}```",
                    )
                )

            elif "Tracking well" in line:
                # find the well that is being analyzed
                current_well = line.split(" ")[-1].split(".")[0]
                # add the well to the list of wells analyzed if it is not already there
                if current_well not in tracking_well:
                    tracking_well.append(current_well)

                # obtain file path to current well
                current_well_path = Path(
                    volume,
                    "input",
                    platename,
                    "TimePoint_1",
                    f"{platename}_{tracking_well[-1]}.TIF",
                )
                # ensure file path exists
                while not os.path.exists(current_well_path):
                    time.sleep(1)

                # create figure from file path
                fig = create_figure_from_filepath(current_well_path)
                docker_output_formatted = "".join(docker_output)
                set_progress(
                    (
                        str(len(tracking_well) + len(wells_analyzed)),
                        str(2 * len(wells)),
                        fig,
                        f"```{current_well_path}```",
                        f"```{docker_output_formatted}```",
                    )
                )


def run_wrmXpress_imagexpress_selection_tracking(new_store, set_progress):
    wrmxpress_command_split = new_store["wrmxpress_command_split"]
    output_folder = new_store["output_folder"]
    output_file = new_store["output_file"]
    wells = new_store["wells"]
    volume = new_store["volume"]
    platename = new_store["platename"]
    tracking_well = new_store["tracking_well"]

    while not os.path.exists(output_folder):
        time.sleep(1)
    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("Running wrmXpress.")
        # Create an empty list to store the docker output
        docker_output = []
        for line in iter(process.stdout.readline, b""):
            # Add the line to docker_output for further processing
            docker_output.append(line)
            file.write(line)
            file.flush()
            if "Generating w1 thumbnails" in line:
                tracks_file_path = Path(
                    volume, "output", "thumbs", f"{platename}_tracks.png"
                )
                while not os.path.exists(tracks_file_path):
                    time.sleep(1)
                # create figure from file path
                fig_1 = create_figure_from_filepath(tracks_file_path)
                docker_output_formatted = "".join(docker_output)
                print("wrmXpress is finished")
                docker_output.append("wrmXpress is finished")
                docker_output_formatted = "".join(docker_output)
                return fig_1, False, False, f"", f"```{docker_output_formatted}```"

            elif "Tracking well" in line:
                # find the well that is being analyzed
                current_well = line.split(" ")[-1].split(".")[0]
                # add the well to the list of wells analyzed if it is not already there
                if current_well not in tracking_well:
                    tracking_well.append(current_well)

                # obtain file path to current well
                current_well_path = Path(
                    volume,
                    "input",
                    platename,
                    "TimePoint_1",
                    f"{platename}_{tracking_well[-1]}.TIF",
                )
                # ensure file path exists
                while not os.path.exists(current_well_path):
                    time.sleep(1)

                # create figure from file path
                fig = create_figure_from_filepath(current_well_path)
                docker_output_formatted = "".join(docker_output)
                set_progress(
                    (
                        str(len(tracking_well)),
                        str(len(wells)),
                        fig,
                        f"```{current_well_path}```",
                        f"```{docker_output_formatted}```",
                    )
                )


def run_wrmXpress_avi_selection_motility(new_store, set_progress):
    wrmxpress_command_split = new_store["wrmxpress_command_split"]
    output_folder = new_store["output_folder"]
    output_file = new_store["output_file"]
    wells = new_store["wells"]
    volume = new_store["volume"]
    platename = new_store["platename"]
    plate_base = platename.split("_", 1)[0]

    while not os.path.exists(output_folder):
        time.sleep(1)

    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("Running wrmXpress.")

        # Create an empty list to store the docker output
        docker_output = []
        wells_analyzed = []
        reconfiguring_well = []
        wells_to_be_analyzed = len(wells)

        for line in iter(process.stdout.readline, b""):
            # Add the line to docker_output for further processing
            docker_output.append(line)
            file.write(line)
            file.flush()

            # Process the line if 'Reconfiguring' is in the line
            if "Reconfiguring" in line:
                process_reconfiguring_wells(
                    line,
                    reconfiguring_well,
                    wells,
                    volume,
                    platename,
                    plate_base,
                    set_progress,
                    docker_output,
                )
            # Process the line if 'Running' is in the line
            elif "Running" in line:
                process_running_wells(
                    line,
                    wells_analyzed,
                    wells,
                    volume,
                    platename,
                    plate_base,
                    set_progress,
                    docker_output,
                )

        process.communicate()  # Ensure all output has been processed and subprocess has finished

        if process.returncode == 0:
            print("wrmXpress process completed.")

            output_file = Path(volume, "output", "thumbs", platename + ".png")

            if os.path.exists(output_file):
                fig_1 = create_figure_from_filepath(output_file)
                docker_output.append("Thumbnail generation completed successfully.")
                docker_output_formatted = "".join(docker_output)
                return fig_1, False, False, "", f"```{docker_output_formatted}```"
            else:
                error_message = (
                    f"There has been an error, please check the {output_file}."
                )
                docker_output_formatted = "".join(docker_output)
                return (
                    None,
                    True,
                    True,
                    f"```{error_message}```",
                    f"```{docker_output_formatted}```",
                )

        else:
            print("wrmXpress has failed.")
            return handle_failure(docker_output, output_file)


def run_wrmXpress_imagexpress_selection_motility(new_store, set_progress):
    wrmxpress_command_split = new_store["wrmxpress_command_split"]
    output_folder = new_store["output_folder"]
    output_file = new_store["output_file"]
    wells = new_store["wells"]
    volume = new_store["volume"]
    platename = new_store["platename"]
    plate_base = platename.split("_", 1)[0]

    while not os.path.exists(output_folder):
        time.sleep(1)

    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("Running wrmXpress.")

        docker_output = []
        wells_analyzed = []

        # Process all output from the subprocess
        for line in iter(process.stdout.readline, ""):
            docker_output.append(line)
            file.write(line)
            file.flush()
            # Process 'Running' lines to update progress
            if "Running" in line:
                process_running_wells(
                    line,
                    wells_analyzed,
                    wells,
                    volume,
                    platename,
                    plate_base,
                    set_progress,
                    docker_output,
                )

        # Wait for the subprocess to complete its execution
        process.communicate()  # Ensure all output has been processed and subprocess has finished

        if process.returncode == 0:
            print("wrmXpress process completed.")

            output_file = Path(volume, "output", "thumbs", platename + ".png")

            if os.path.exists(output_file):
                fig_1 = create_figure_from_filepath(output_file)
                docker_output.append("Thumbnail generation completed successfully.")
                docker_output_formatted = "".join(docker_output)
                return fig_1, False, False, "", f"```{docker_output_formatted}```"
            else:
                error_message = (
                    f"There has been an error, please check the {output_file}."
                )
                docker_output_formatted = "".join(docker_output)
                return (
                    None,
                    True,
                    True,
                    f"```{error_message}```",
                    f"```{docker_output_formatted}```",
                )

        else:
            print("wrmXpress has failed.")
            return handle_failure(docker_output, output_file)


def process_reconfiguring_wells(
    line,
    reconfiguring_well,
    wells,
    volume,
    platename,
    plate_base,
    set_progress,
    docker_output,
):
    # find the well that is being analyzed
    current_well = line.split(".")[0].split("_")[-1]
    # add the well to the list of wells analyzed if it is not already there
    if current_well not in reconfiguring_well:
        reconfiguring_well.append(current_well)
    # obtain file path to current well
    current_well_path = Path(
        volume,
        "input",
        platename,
        "TimePoint_1",
        f"{platename}_{reconfiguring_well[-1]}.TIF",
    )
    # ensure file path exists
    while not os.path.exists(current_well_path):
        time.sleep(1)
    # create figure from file path
    fig = create_figure_from_filepath(current_well_path)
    docker_output_formatted = "".join(docker_output)
    set_progress(
        (
            str(len(reconfiguring_well)),
            str(2 * len(wells)),
            fig,
            f"```{current_well_path}```",
            f"```{docker_output_formatted}```",
        )
    )


def process_running_wells(
    line,
    wells_analyzed,
    wells,
    volume,
    platename,
    plate_base,
    set_progress,
    docker_output,
):
    well_running = line.split(" ")[-1].strip()
    if well_running not in wells_analyzed:
        wells_analyzed.append(well_running)
        img_path = Path(
            volume, f"input/{platename}/TimePoint_1/{plate_base}_{well_running}.TIF"
        )
        if img_path.exists():
            fig = create_figure_from_filepath(img_path)
            docker_output_formatted = "".join(docker_output)
            set_progress(
                (
                    len(wells_analyzed),
                    len(wells),
                    fig,
                    f"```{str(img_path)}```",
                    f"```{docker_output_formatted}```",
                )
            )


def handle_thumbnail_generation(volume, platename, docker_output, output_file):
    output_path = Path(volume, "output", "thumbs", platename + ".png")
    if os.path.exists(output_path):
        fig_1 = create_figure_from_filepath(output_path)
        docker_output.append("Thumbnail generation completed successfully.")
        docker_output_formatted = "".join(docker_output)
        return fig_1, False, False, "", f"```{docker_output_formatted}```"
    else:
        error_message = f"Thumbnail generation failed, please check the {output_file}."
        docker_output_formatted = "".join(docker_output)
        return (
            None,
            True,
            True,
            f"```{error_message}```",
            f"```{docker_output_formatted}```",
        )


def handle_failure(docker_output, output_file):
    error_message = (
        f"wrmXpress has failed, please check the {output_file} for more information."
    )
    docker_output_formatted = "".join(docker_output)
    return (
        None,
        True,
        True,
        f"```{error_message}```",
        f"```{docker_output_formatted}```",
    )


########################################################################
####                                                                ####
####                   old/unused functions                         ####
####                                                                ####
########################################################################


""" 
def preamble_to_run_wrmXpress_tracking(store):
    '''
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

    '''
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

def preamble_to_run_wrmXpress_non_tracking(store):
    '''
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
    '''
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

"""
