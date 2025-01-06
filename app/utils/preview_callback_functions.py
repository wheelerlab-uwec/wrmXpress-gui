########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

from pathlib import Path
import os
import subprocess
import time
import shlex

from app.utils.callback_functions import (
    copy_files_to_input_directory,
    create_figure_from_filepath,
    clean_and_create_directories,
    update_yaml_file,
)

########################################################################
####                                                                ####
####                          Functions                             ####
####                                                                ####
########################################################################


def preview_callback_functions(store):
    """
    This function is used to preview the analysis of the selected options.

    """

    pipeline_selection = store["wrmXpress_gui_obj"]["pipeline_selection"]

    if pipeline_selection == "motility":
        return motility_segment_fecundity_preview(store)

    elif pipeline_selection == "segmentation":
        return motility_segment_fecundity_preview(store)

    elif pipeline_selection == "tracking":
        return tracking_wrmXpress_preview(store)

    elif pipeline_selection == "cellprofiler":
        pipeline_selection = store["wrmXpress_gui_obj"][
            "cellprofiler_pipeline_selection"
        ]

        if pipeline_selection == "wormsize":
            return cellprofiler_wormsize_preview(store)

        elif pipeline_selection == "wormsize_intensity_cellpose":
            return cellprofiler_wormsize_intensity_cellpose_preview(store)

        elif pipeline_selection == "mf_celltox":
            return cellprofiler_mf_celltox_preview(store)

        elif pipeline_selection == "feeding":
            return cellprofiler_feeding_preview(store)


########################################################################
####                                                                ####
####                   preview.py functions                         ####
####                                                                ####
########################################################################


def preamble_preview_imgxpress_selection(store):
    """
    This function prepares the wrmXpress command, output preview log file, command message, and first well.
    """
    # Obtain the store data
    volume = store["mount"]
    platename = store["platename"]
    wells = store["wells"]

    # defining the yaml file path (same as the filepath from configure.py)
    preview_yaml_platename = "." + platename + ".yml"
    preview_yaml_platenmaefull_yaml = Path(volume, preview_yaml_platename)
    full_yaml = Path(volume, platename + ".yml")

    update_yaml_file(full_yaml, preview_yaml_platenmaefull_yaml, {"wells": ["All"]})

    if wells == "All":
        first_well = "A01"
    else:
        first_well = wells[0]

    img_dir = Path(volume, platename)
    input_dir = Path(volume, "input")
    platename_input_dir = Path(input_dir, platename)
    plate_base = platename.split("_", 1)[0]
    htd_file = Path(img_dir, f"{plate_base}.HTD")

    # Clean and create directories
    clean_and_create_directories(
        input_path=Path(volume, "input", platename),
        work_path=Path(volume, "work", platename),
        output_path=Path(volume, "output"),
    )

    # Copy files to input directory
    copy_files_to_input_directory(
        platename_input_dir=platename_input_dir,
        htd_file=htd_file,
        img_dir=img_dir,
        plate_base=plate_base,
        wells=first_well,
        platename=platename,
    )

    # Command message
    command_message = f"```python /root/wrmXpress/wrapper.py {platename}.yml {platename}```"

    wrmxpress_command = (
        f"python /root/wrmXpress/wrapper.py {volume}/.{platename}.yml {platename}"
    )
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_preview_log_file = Path(
        volume, "work", platename, f"{platename}_preview.log"
    )

    new_store = {
        "wrmxpress_command_split": wrmxpress_command_split,
        "output_preview_log_file": output_preview_log_file,
        "command_message": command_message,
        "first_well": first_well,
    }
    return new_store


def preamble_preview_avi_selection(store):
    """
    The purpose of this function is to prepare the wrmXpress command, output folder, output file,
    command message, wells, volume, platename, motility, segment, cellprofiler, and cellprofilepipeline.

    """
    # Obtain the store data
    volume = store["mount"]
    platename = store["platename"]
    wells = store["wells"]

    # necessary file paths
    img_dir = Path(volume, platename)
    input_dir = Path(volume, "input")
    platename_input_dir = Path(input_dir, platename)

    # defining the yaml file path (same as the filepath from configure.py)
    preview_yaml_platename = "." + platename + ".yml"
    preview_yaml_platenmaefull_yaml = Path(volume, preview_yaml_platename)
    full_yaml = Path(volume, platename + ".yml")

    if wells == "All":
        first_well = "A01"
    else:
        first_well = wells[0]

    update_yaml_file(full_yaml, preview_yaml_platenmaefull_yaml, {"wells": ["All"]})

    # clean and create directories
    clean_and_create_directories(
        input_path=Path(volume, "input", platename),
        work_path=Path(volume, "work", platename),
    )

    copy_files_to_input_directory(
        platename_input_dir=platename_input_dir,
        htd_file=None,
        img_dir=img_dir,
        wells=first_well,
        plate_base=None,
        platename=platename,
    )

    # Command message
    command_message = f"```python /root/wrmXpress/wrapper.py {platename}.yml {platename}```"

    wrmxpress_command = (
        f"python /root/wrmXpress/wrapper.py {volume}/.{platename}.yml {platename}"
    )
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_preview_log_file = Path(
        volume, "work", platename, f"{platename}_preview.log"
    )

    new_store = {
        "wrmxpress_command_split": wrmxpress_command_split,
        "output_preview_log_file": output_preview_log_file,
        "command_message": command_message,
        "first_well": first_well,
    }

    return new_store


def motility_segment_fecundity_preview(store):
    """
    This function is used to preview the analysis of the selected options from
    the configuration page, including motility, segment, and fecundity. This function
    will run wrmXpress and return the path to the image, the figure, and the open status
    if the first well has not already been analyzed.
    """
    try:
        # Obtain the store data
        volume = store["mount"]
        platename = store["platename"]
        wells = store["wells"]
        file_structure = store["file_structure"]
        # Check to see if first well already exists, if it does insert the img
        # rather than running wrmXpress again
        first_well_path = Path(
            volume, "work", f"{platename}/{wells[0]}/img/{platename}_{wells[0]}.png"
        )

        # Check if the first well path exists
        if os.path.exists(first_well_path):

            # Open the image and create a figure
            fig = create_figure_from_filepath(first_well_path)

            # Return the path and the figure and the open status of the alerts
            return f"```{first_well_path}```", fig, False, f"", False

        if file_structure == "imagexpress":

            new_store = preamble_preview_imgxpress_selection(store)
        elif file_structure == "avi":

            # if the first well does not exist, run wrmXpress
            new_store = preamble_preview_avi_selection(
                store  # need to change function to accept this argument
            )

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_preview_log_file = new_store["output_preview_log_file"]
        command_message = new_store["command_message"]
        first_well = new_store["first_well"]

        with open(output_preview_log_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            docker_output = []

            print("Running wrmXpress.")
            docker_output.append("Running wrmXpress.")

            # Should try and figure out an alternative to this
            # potential brick mechanism for the user
            while not os.path.exists(Path(volume, "input")):
                time.sleep(1)

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

            process.communicate()
            if process.returncode == 0:
                # Assumes IX-like file structure
                img_path = Path(
                    volume,
                    "work",
                    f"{platename}/{first_well}/img/{platename}_{first_well}.png",
                )

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)
                print("wrmXpress is finished")
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f"", False

            else:
                return (
                    command_message,
                    None,
                    True,
                    f"wrmXpress has failed, please check the {output_preview_log_file} for more information.",
                    True,
                )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (
            error_message,
            None,
            True,
            "An error has occurred. Please see the log file for more information.",
            True,
        )


def cellprofiler_wormsize_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including worm size. This function will run wrmXpress and return
    the path to the image, the figure, and the open status if the first well has not already been analyzed.
    """
    try:
        # Obtain the store data
        volume = store["mount"]
        platename = store["platename"]
        wells = store["wells"]
        plate_base = platename.split("_", 1)[0]
        first_well = wells[0]
        # Assumes IX-like file structure
        first_well_path = Path(
            volume, f"output/straightened_worms/{plate_base}_{first_well}.tiff"
        )

        # Check if the first well path exists
        if os.path.exists(first_well_path):
            # Open the image and create a figure
            fig = create_figure_from_filepath(first_well_path)

            # Return the path and the figure and the open status of the alerts
            return f"```{first_well_path}```", fig, False, f"", False

        new_store = preamble_preview_imgxpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_preview_log_file = new_store["output_preview_log_file"]
        command_message = new_store["command_message"]
        first_well = new_store["first_well"]

        with open(output_preview_log_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            print("Running wrmXpress.")
            docker_output = []

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

            process.wait()

            if process.returncode == 0:

                file_path = Path(
                    volume, f"output/straightened_worms/{plate_base}_{first_well}.tiff"
                )
                # Open the image and create a figure
                fig = create_figure_from_filepath(file_path)
                print("wrmXpress is finished")
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f"", False

            else:
                return (
                    command_message,
                    None,
                    True,
                    f"wrmXpress has failed, please check the {output_preview_log_file} for more information.",
                    True,
                )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (
            error_message,
            None,
            True,
            "An error has occurred. Please see the log file for more information.",
            True,
        )


def cellprofiler_wormsize_intensity_cellpose_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including worm size and intensity using CellPose. This function
    will run wrmXpress and return the path to the image, the figure, and the open status if the first well has not already been analyzed.
    """
    try:
        # Obtain the store data
        volume = store["mount"]
        platename = store["platename"]
        wells = store["wells"]
        plate_base = platename.split("_", 1)[0]

        # Assumes the first well in the list is the one to check
        first_well = wells[0]

        # Check to see if first well already exists, if it does insert the img
        # rather than running wrmXpress again
        first_well_path = Path(
            volume, f"output/straightened_worms/{plate_base}_{first_well}.tiff"
        )
        if os.path.exists(first_well_path):
            # Open the image and create a figure
            fig = create_figure_from_filepath(first_well_path)

            # Return the path and the figure and the open status of the alerts
            return f"```{first_well_path}```", fig, False, f"", False

        new_store = preamble_preview_imgxpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_preview_log_file = new_store["output_preview_log_file"]
        command_message = new_store["command_message"]
        first_well = new_store["first_well"]

        with open(output_preview_log_file, "w") as file:

            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            print("Running wrmXpress.")

            docker_output = []

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

            process.wait()

            if process.returncode == 0:

                img_path = Path(
                    volume, f"output/straightened_worms/{plate_base}_{first_well}.tiff"
                )
                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)
                print("wrmXpress is finished")
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f"", False

            else:
                return (
                    command_message,
                    None,
                    True,
                    f"wrmXpress has failed, please check the {output_preview_log_file} for more information.",
                    True,
                )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (
            error_message,
            None,
            True,
            "An error has occurred. Please see the log file for more information.",
            True,
        )


def cellprofiler_mf_celltox_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including motility, fecundity, and celltox. This function
    will run wrmXpress and return the path to the image, the figure, and the open status if the first well has not already been analyzed.
    """
    try:
        # Obtain the store data
        volume = store["mount"]
        platename = store["platename"]
        wells = store["wells"]

        first_well = wells[
            0
        ]  # Assuming first_well is defined here as the first item in wells

        # Check to see if first well already exists, if it does insert the img
        # rather than running wrmXpress again
        first_well_path = Path(
            volume,
            "work",
            platename,
            first_well,
            "img",
            f"{platename}_{first_well}.png",
        )

        if os.path.exists(first_well_path):
            # Open the image and create a figure
            fig = create_figure_from_filepath(first_well_path)

            # Return the path and the figure and the open status of the alerts
            return f"```{first_well_path}```", fig, False, f"", False

        new_store = preamble_preview_imgxpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_preview_log_file = new_store["output_preview_log_file"]
        command_message = new_store["command_message"]
        first_well = new_store["first_well"]

        with open(output_preview_log_file, "w") as file:

            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            print("Running wrmXpress.")

            docker_output = []

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

            process.wait()

            if process.returncode == 0:

                img_path = Path(
                    volume,
                    "work",
                    platename,
                    first_well,
                    "img",
                    f"{platename}_{first_well}.png",
                )

                # Open the image and create a figure
                fig = create_figure_from_filepath(img_path)
                print("wrmXpress is finished")
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f"", False

            else:
                return (
                    command_message,
                    None,
                    True,
                    f"wrmXpress has failed, please check the {output_preview_log_file} for more information.",
                    True,
                )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (
            error_message,
            None,
            True,
            "An error has occurred. Please see the log file for more information.",
            True,
        )


def cellprofiler_feeding_preview(store):
    """
    The purpose of this function is to preview the analysis of the selected options from
    the configuration page, including feeding. This function will run wrmXpress and return
    the path to the image, the figure, and the open status if the first well has not already been analyzed.
    """
    try:
        # Obtain the store data
        volume = store["mount"]
        platename = store["platename"]
        wells = store["wells"]
        plate_base = platename.split("_", 1)[0]

        first_well = wells[0]  # Assuming first_well is the first item in wells list

        # Check to see if first well already exists, if it does insert the img
        # rather than running wrmXpress again
        first_well_path = Path(
            volume, f"output/straightened_worms/{plate_base}-{first_well}.tiff"
        )

        if os.path.exists(first_well_path):
            # Open the image and create a figure
            fig = create_figure_from_filepath(first_well_path)

            # Return the path and the figure and the open status of the alerts
            return f"```{first_well_path}```", fig, False, f"", False

        new_store = preamble_preview_imgxpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_preview_log_file = new_store["output_preview_log_file"]
        command_message = new_store["command_message"]
        first_well = new_store["first_well"]

        with open(output_preview_log_file, "w") as file:

            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            print("Running wrmXpress.")

            docker_output = []

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

            process.wait()

            if process.returncode == 0:

                # Open the image and create a figure
                fig = create_figure_from_filepath(first_well_path)
                print("wrmXpress is finished")
                # Return the command message, the figure, and the open status of the alerts
                return command_message, fig, False, f"", False

            else:
                return (
                    command_message,
                    None,
                    True,
                    f"wrmXpress has failed, please check the {output_preview_log_file} for more information.",
                    True,
                )
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (
            error_message,
            None,
            True,
            "An error has occurred. Please see the log file for more information.",
            True,
        )


def tracking_wrmXpress_preview(store):
    """
    This function is used to preview the analysis of the selected options from
    the configuration page, including motility, segment, and fecundity. This function
    will run wrmXpress and return the path to the image, the figure, and the open status
    if the first well has not already been analyzed.
    """
    try:
        # Obtain the store data
        volume = store["mount"]
        platename = store["platename"]
        wells = store["wells"]
        file_structure = store["file_structure"]

        # check to see if the first well has already been analyzed
        first_well_path = Path(
            volume,
            "work",
            f"{platename}/{wells[0]}/img/{platename}_{wells[0]}_tracks.png",
        )

        # Check if the first well path exists
        if os.path.exists(first_well_path):
            # Open the image and create a figure
            fig = create_figure_from_filepath(first_well_path)

            # Return the path and the figure and the open status of the alerts
            return f"```{first_well_path}```", fig, False, f"", False

        if file_structure == "imagexpress":
            new_store = preamble_preview_imgxpress_selection(store=store)

        elif file_structure == "avi":
            # if the first well does not exist, run wrmXpress
            new_store = preamble_preview_avi_selection(store=store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_preview_log_file = new_store["output_preview_log_file"]
        command_message = new_store["command_message"]
        first_well = new_store["first_well"]

        with open(output_preview_log_file, "w") as file:
            process = subprocess.Popen(
                wrmxpress_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            print("Running wrmXpress.")

            # Create an empty list to store the docker output
            docker_output = []

            for line in iter(process.stdout.readline, ""):
                # Add the line to docker_output for further processing
                docker_output.append(line)
                file.write(line)
                file.flush()

            process.wait()

            if process.returncode == 0:

                first_well_path = Path(
                    volume,
                    "work",
                    f"{platename}/{wells[0]}/img/{platename}_{first_well}_tracks.png",
                )

                # create figure from file path
                fig_1 = create_figure_from_filepath(first_well_path)
                print("wrmXpress is finished")
                return command_message, fig_1, False, f"", False

            else:
                return (
                    command_message,
                    None,
                    True,
                    f"wrmXpress has failed, please check the {output_preview_log_file} for more information.",
                    True,
                )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (
            error_message,
            None,
            True,
            "An error has occurred. Please see the log file for more information.",
            True,
        )
