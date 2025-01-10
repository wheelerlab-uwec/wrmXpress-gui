# In[1]: Imports

import pandas as pd
from pathlib import Path
import os
import subprocess
import time
import shlex
import re

from app.utils.callback_functions import (
    update_yaml_file,
    clean_and_create_directories,
    copy_files_to_input_directory,
    create_figure_from_filepath,
)
from app.utils.wrmxpress_gui_obj import WrmXpressGui

# In[2]: Main Callback Function


def callback(set_progress, store, wrmXpress_gui_obj):
    """
    This function is used for the callback function in the app.py file. The
    purpose of this function is to run the wrmXpress pipeline based on the
    pipeline selection and return the figure, open status, and command message.
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
                None,
            )

        # obtain the necessary data from the store
        # pipeline_selection = store["wrmXpress_gui_obj"]["pipeline_selection"]
        
        return run_wrmXpress_analysis(store, set_progress, wrmXpress_gui_obj)
    
        # TODO: # Update this if avi is selected and above method doesnt work
        
        # if store['file_structure'] == 'avi':
        #     return run_avi_wrmXpress_analysis(store, set_progress, wrmXpress_gui_obj)

        # elif store['file_structure'] == 'imagexpress':
        #     return run_wrmXpress_analysis(store, set_progress, wrmXpress_gui_obj)
        # Check if the submit button has been clicked

        # TODO: What if multiple pipelines are selected?
        """
        if "motility" in pipeline_selection:
            return motility_or_segment_run(store, set_progress, wrmXpress_gui_obj)

        elif "segmentation" in pipeline_selection:
            return fecundity_run(store, set_progress, wrmXpress_gui_obj)

        # TODO: lets get motility working first

        elif "tracking" in pipeline_selection:
            return tracking_wrmXpress_run(store, set_progress)

        elif "cellprofiler" in pipeline_selection:
            cell_profile_pipeline = store["wrmXpress_gui_obj"][
                "cellprofiler_pipeline_selection"
            ]

            if cell_profile_pipeline == "wormsize_intensity_cellpose":
                return cellprofiler_wormsize_intesity_cellpose_run(store, set_progress)

            elif cell_profile_pipeline == "mf_celltox":
                return cellprofiler_mf_celltox_run(store, set_progress)

            elif cell_profile_pipeline == "feeding":
                return cellprofiler_feeding_run(store, set_progress)

            elif cell_profile_pipeline == "wormsize":
                return cellprofiler_wormsize_run(store, set_progress)
        """
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
            None,
        )

def run_wrmXpress_analysis(store, set_progress, wrmXpress_gui_obj):
    """
    The purpose of this function is to run the wrmXpress pipeline for imagexpress formatted files,
    regardless of the pipeline selection.
    """
    if store['file_structure'] == 'imagexpress':
        new_store = preamble_run_wrmXpress_imagexpress_selection(store)
    
    elif store['file_structure'] == 'avi':
        new_store = preamble_run_wrmXpress_avi_selection(store)

    # while not os.path.exists(new_store["output_folder"]):
    #     time.sleep(1)

    with open(new_store["output_file"], "w") as file:
        process = subprocess.Popen(
            new_store["wrmxpress_command_split"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("Running wrmXpress.")

        docker_output = []

        # Process all lines from the subprocess
        for line in iter(process.stdout.readline, ""):
            docker_output.append(line)
            file.write(line)
            file.flush()
            
            try:
                if len(re.findall(r"\b" + "|".join(new_store["wells"]) + r"\b", line)) == 1:
                    updated_running_wells(set_progress, line, store, docker_output, wrmXpress_gui_obj)

                
            except Exception as e:
                print(f"Error: {e}")
                continue

            if wrmXpress_gui_obj.set_progress_running:
                docker_output_formatted = "".join(docker_output)
                set_progress(
                    (
                        wrmXpress_gui_obj.set_progress_current_number,
                        wrmXpress_gui_obj.set_progress_total_number,
                        wrmXpress_gui_obj.set_progress_figure,
                        f"```{wrmXpress_gui_obj.set_progress_image_path}```",
                        f"```{docker_output_formatted}```",
                    )
                )
        # Ensure all output is processed and the subprocess has finished
        process.communicate()

        if process.returncode == 0:
            print("wrmXpress process successful.")
            wrmXpress_gui_obj.check_for_output_files()

            if wrmXpress_gui_obj.output_files_exist:
                return updated_thumbnail_generation(wrmXpress_gui_obj, docker_output)

            # TODO: Implement thumbnail generation
            return None

        else:
            print("wrmXpress process failed.")
            wrmXpress_gui_obj.check_for_output_files()
            if wrmXpress_gui_obj.output_files_exist:
                return updated_thumbnail_generation(wrmXpress_gui_obj, docker_output)

            # TODO: Implement failure handling
            return None


def updated_running_wells(set_progress, line, store, docker_output, wrmXpress_gui_obj):

    well_being_analyzed, progress = line.split(" ")
    current_number, total_number = progress.split("/")
    plate_base = store["platename"].split("_", 1)[0]
    well_base_path = Path(
        store["wrmXpress_gui_obj"]["mounted_volume"],
        f"{store['wrmXpress_gui_obj']['plate_name']}/TimePoint_1/{plate_base}_{well_being_analyzed}",
    )
    # Use rglob with case-insensitive pattern matching for .TIF and .tif
    file_paths = list(
        well_base_path.parent.rglob(well_base_path.name + "*[._][tT][iI][fF]")
    )
    # Sort the matching files to find the one with the lowest suffix number
    if file_paths:
        file_paths_sorted = sorted(file_paths, key=lambda x: x.stem)
        # Select the first file (with the lowest number) if multiple matches are found
        img_path = file_paths_sorted[0]

    else:
        # Fallback if no matching files are found
        img_path = well_base_path.with_suffix(".TIF")

    if img_path.exists():
        fig = create_figure_from_filepath(img_path)
        docker_output_formatted = "".join(docker_output)

        set_progress(
            (
                str(current_number),
                str(total_number),
                fig,
                f"```{str(img_path)}```",
                f"```{docker_output_formatted}```",
            )
        )

        wrmXpress_gui_obj.set_processing_arguments(
            current_number, 
            total_number, 
            fig, 
            img_path
        )


def preamble_run_wrmXpress_avi_selection(store):
    """
    The purpose of this function is to prepare the necessary files and directories for wrmXpress for avi files.
    """
    volume = store["mount"]
    platename = store["platename"]
    wells = store["wells"]

    # necessary file paths
    img_dir = Path(volume, platename)
    input_dir = Path(volume, "input")
    platename_input_dir = Path(input_dir, platename)
    full_yaml = Path(volume, platename + ".yml")

    update_yaml_file(
        full_yaml,
        full_yaml,
        {"wells": store["wrmXpress_gui_obj"]["well_selection_list"]},
    )

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
    command_message = (
        f"```python /root/wrmXpress/wrapper.py {platename}.yml {platename}```"
    )

    wrmxpress_command = (
        f"python -u /root/wrmXpress/wrapper.py {volume}/{platename}.yml {platename}"
    )
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_folder = Path(volume, "work", platename)
    output_file = Path(
        volume, "work", f"{platename}_run.log"
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

    update_yaml_file(
        full_yaml,
        full_yaml,
        {"wells": store["wrmXpress_gui_obj"]["well_selection_list"]},
    )

    # clean and create directories
    clean_and_create_directories(
        input_path=Path(volume, "input", platename),
        work_path=Path(
            volume, "work"
        ),  # TODO: update this with the correct directory of pipeline selection
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
    command_message = (
        f"```python /root/wrmXpress/wrapper.py {platename}.yml {platename}```"
    )

    wrmxpress_command = (
        f"python -u /root/wrmXpress/wrapper.py {volume}/{platename}.yml {platename}"
    )
    wrmxpress_command_split = shlex.split(wrmxpress_command)
    output_folder = Path(volume, "work", platename)
    output_file = Path(
        volume, "work", f"{platename}_run.log"
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


# In[3]: Helper Functions

def tracking_wrmXpress_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for tracking and return the figure, open status, and command message.
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
            None,
        )


def motility_or_segment_run(store, set_progress, wrmXpress_gui_obj):
    """
    The purpose of this function is to run wrmXpress for motility and segment and return the figure, open status, and command message.
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(store)
            return run_wrmXpress_avi_selection_motility(new_store, set_progress)

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)
            return run_wrmXpress_imagexpress_selection_motility(new_store, set_progress, store, wrmXpress_gui_obj)

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
            None,
        )


def fecundity_run(store, set_progress, wrmXpress_gui_obj):
    """
    The purpose of this function is to run wrmXpress for fecundity and return the figure, open status, and command message.
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(
                store
            )  # Including this information for now
            # however we do not currently allow for avi and fecundity to be run together

        elif file_structure == "imagexpress":
            new_store = preamble_run_wrmXpress_imagexpress_selection(store)

        wrmxpress_command_split = new_store["wrmxpress_command_split"]
        output_folder = new_store["output_folder"]
        output_file = new_store["output_file"]
        wells = new_store["wells"]
        volume = new_store["volume"]
        platename = new_store["platename"]
        plate_base = platename.split("_", 1)[0]

        # Should try and figure out an alternative to this
        # potential brick mechanism for the user
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
            # wells_analyzed = []

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                # check if any of the wells in well_selection_list are being analyzed
                # the line must contain only one of the wells in the selection list, if contains more disregard it
                # the line looks something like "{well} {number}/{total number of wells}"
                if len(re.findall(r"\b" + "|".join(wells) + r"\b", line)) == 1:

                    updated_running_wells(
                        set_progress, 
                        line, 
                        store, 
                        docker_output
                        )
                # if "Running" in line:

                #     process_running_wells(
                #         line,
                #         wells_analyzed,
                #         wells,
                #         volume,
                #         platename,
                #         plate_base,
                #         set_progress,
                #         docker_output,
                #     )

            process.wait()

            if process.returncode == 0:

                print("wrmXpress process successful.")  

                # check for output files
                wrmXpress_gui_obj.check_for_output_files()

                if wrmXpress_gui_obj.output_files_exist:
                    return updated_thumbnail_generation(wrmXpress_gui_obj, docker_output)
                
                # TODO: Implement thumbnail generation
                return handle_thumbnail_generation(
                    volume, platename, docker_output, output_file, pipeline="segmentation"
                )

            else:
                print("wrmXpress process failed.")
                wrmXpress_gui_obj.check_for_output_files()
                
                if wrmXpress_gui_obj.output_files_exist:
                    return updated_thumbnail_generation(wrmXpress_gui_obj, docker_output)
                
                # TODO: Implement failure handling
                return handle_failure(docker_output, output_file)

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
            None,
        )


def cellprofiler_wormsize_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for wormsize and return the figure, open status, and command message.
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(
                store
            )  # Including this information for now
            # however we do not currently allow for avi and wormsize to be run together

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

        # Should try and figure out an alternative to this
        # potential brick mechanism for the user
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

            wells_analyzed = []

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                if "Image #" in line:

                    process_img_number(
                        line,
                        wells,
                        volume,
                        platename,
                        plate_base,
                        pipeline_selection,
                        set_progress,
                        docker_output,
                        wells_analyzed,
                    )
            process.wait()

            if process.returncode == 0:

                return handle_thumbnail_generation(
                    volume, platename, docker_output, output_file
                )

            else:
                print("wrmXpress process failed.")
                return handle_failure(docker_output, output_file)

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
            None,
        )


def cellprofiler_wormsize_intesity_cellpose_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for wormsize_intensity_cellpose and return the figure, open status, and command message.
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(
                store
            )  # Including this information for now
            # however we do not currently allow for avi and wormsize_intensity_cellpose to be run together

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

        # Should try and figure out an alternative to this
        # potential brick mechanism for the user
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
            info_and_percent_wells = []
            wells_analyzed = []

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                if "Image #" in line:

                    process_img_number(
                        line,
                        wells,
                        volume,
                        platename,
                        plate_base,
                        pipeline_selection,
                        set_progress,
                        docker_output,
                        wells_analyzed,
                        additional_wells=info_and_percent_wells,
                        multiplier=2,
                    )

                elif "[INFO]" in line and "%" in line:

                    process_info_and_percent(
                        line,
                        wells,
                        volume,
                        platename,
                        plate_base,
                        set_progress,
                        docker_output,
                        info_and_percent_wells,
                        multiplier=2,
                    )

            process.wait()

            if process.returncode == 0:

                return handle_thumbnail_generation(
                    volume, platename, docker_output, output_file
                )

            else:
                print("wrmXpress process failed.")
                return handle_failure(docker_output, output_file)
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
            None,
        )


def cellprofiler_mf_celltox_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for mf_celltox and return the figure, open status, and command message.
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(
                store
            )  # Including this information for now
            # however we do not currently allow for avi and mf_celltox to be run together

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

        # Should try and figure out an alternative to this
        # potential brick mechanism for the user
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
            wells_analyzed = []

            print("Running wrmXpress.")

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                csv_file_path = Path(
                    volume, "input", f"image_paths_{pipeline_selection}.csv"
                )
                while not os.path.exists(csv_file_path):
                    time.sleep(1)

                if "Image #" in line:

                    process_img_number(
                        line,
                        wells,
                        volume,
                        platename,
                        plate_base,
                        pipeline_selection,
                        set_progress,
                        docker_output,
                        wells_analyzed,
                        multiplier=1,
                        additional_wells=[],
                    )

            process.wait()

            if process.returncode == 0:

                return handle_thumbnail_generation(
                    volume, platename, docker_output, output_file
                )

            else:
                print("wrmXpress process failed.")
                return handle_failure(docker_output, output_file)
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
            None,
        )


def cellprofiler_feeding_run(store, set_progress):
    """
    The purpose of this function is to run wrmXpress for feeding and return the figure, open status, and command message.
    """
    try:
        file_structure = store["file_structure"]

        if file_structure == "avi":
            new_store = preamble_run_wrmXpress_avi_selection(
                store
            )  # Including this information for now
            # however we do not currently allow for avi and feeding to be run together

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

        # Should try and figure out an alternative to this
        # potential brick mechanism for the user
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
            wells_analyzed = []

            print("Running wrmXpress.")

            for line in iter(process.stdout.readline, ""):
                docker_output.append(line)
                file.write(line)
                file.flush()

                csv_file_path = Path(
                    volume, "input", f"image_paths_{pipeline_selection}.csv"
                )
                while not os.path.exists(csv_file_path):
                    time.sleep(1)

                if "Image #" in line:

                    process_img_number(
                        line,
                        wells,
                        volume,
                        platename,
                        plate_base,
                        pipeline_selection,
                        set_progress,
                        docker_output,
                        wells_analyzed,
                    )

            process.wait()

            if process.returncode == 0:

                return handle_thumbnail_generation(
                    volume, platename, docker_output, output_file
                )

            else:
                print("wrmXpress process failed.")
                return handle_failure(docker_output, output_file)

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
            None,
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

    # Should try and figure out an alternative to this
    # potential brick mechanism for the user
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
        reconfigure_wells = []

        for line in iter(process.stdout.readline, ""):
            # Add the line to docker_output for further processing
            docker_output.append(line)
            file.write(line)
            file.flush()

            if "Reconfiguring" in line:

                process_reconfiguring_wells(
                    line,
                    reconfigure_wells,
                    wells,
                    volume,
                    platename,
                    platename,
                    set_progress,
                    docker_output,
                    multiplier=2,
                )

            elif "Tracking well" in line or "Running well" in line:

                process_tracking_wells(
                    line,
                    wells_analyzed,
                    wells,
                    volume,
                    platename,
                    set_progress,
                    docker_output,
                    additional_wells=reconfigure_wells,
                    multiplier=2,
                )

        process.wait()

        output_file = Path(volume, "output", "thumbs", f"{platename}_tracks.png")

        if process.returncode == 0:

            return handle_thumbnail_generation(
                volume, platename, docker_output, output_file
            )

        else:
            print("wrmXpress process failed.")
            return handle_failure(docker_output, output_file)


def run_wrmXpress_imagexpress_selection_tracking(new_store, set_progress):
    wrmxpress_command_split = new_store["wrmxpress_command_split"]
    output_folder = new_store["output_folder"]
    log_file = new_store["output_file"]  # Log file for subprocess output
    wells = new_store["wells"]
    volume = new_store["volume"]
    platename = new_store["platename"]
    tracking_well = new_store["tracking_well"]

    # Should try and figure out an alternative to this
    # potential brick mechanism for the user
    while not os.path.exists(output_folder):
        time.sleep(1)

    with open(log_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("Running wrmXpress.")
        docker_output = []

        # Real-time processing of subprocess output
        for line in iter(process.stdout.readline, ""):
            docker_output.append(line)
            file.write(line)
            file.flush()

            if "Tracking well" in line or "Running well" in line:
                process_tracking_wells(
                    line,
                    tracking_well,
                    wells,
                    volume,
                    platename,
                    set_progress,
                    docker_output,
                )

        # Wait for the subprocess to complete its execution
        process.wait()  # This replaces communicate() when output is processed line by line

        if process.returncode == 0:
            return handle_thumbnail_generation(
                volume, platename, docker_output, log_file
            )
        else:
            return handle_failure(docker_output, log_file)


def run_wrmXpress_avi_selection_motility(new_store, set_progress):
    wrmxpress_command_split = new_store["wrmxpress_command_split"]
    output_folder = new_store["output_folder"]
    log_file_path = new_store["output_file"]  # Rename for clarity
    wells = new_store["wells"]
    volume = new_store["volume"]
    platename = new_store["platename"]
    plate_base = platename.split("_", 1)[0]

    # Should try and figure out an alternative to this
    # potential brick mechanism for the user
    while not os.path.exists(output_folder):
        time.sleep(1)

    with open(log_file_path, "w") as log_file:  # Use 'log_file' for clarity
        process = subprocess.Popen(
            wrmxpress_command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("Running wrmXpress.")

        docker_output = []
        wells_analyzed = []
        reconfiguring_well = []

        # Handle the output line by line
        for line in iter(process.stdout.readline, ""):

            docker_output.append(line)
            log_file.write(line)
            log_file.flush()

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
                    multiplier=2,
                )
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
                    multiplier=2,
                    other_pipeline_wells=reconfiguring_well,
                )

        process.wait()  # Ensure the subprocess has finished

        if process.returncode == 0:
            return handle_thumbnail_generation(
                volume, platename, docker_output, log_file
            )
        else:
            return handle_failure(docker_output, log_file_path)


def run_wrmXpress_imagexpress_selection_motility(new_store, set_progress, store, wrmXpress_gui_obj):
    wrmxpress_command_split = new_store["wrmxpress_command_split"]
    output_folder = new_store["output_folder"]
    output_file = new_store["output_file"]
    wells = new_store["wells"]
    volume = new_store["volume"]
    platename = new_store["platename"]
    # plate_base = platename.split("_", 1)[0]

    # Should try and figure out an alternative to this
    # potential brick mechanism for the user
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
        # wells_analyzed = []

        # Process all output from the subprocess
        for line in iter(process.stdout.readline, ""):
            docker_output.append(line)
            file.write(line)
            file.flush()

            # check if any of the wells in well_selection_list are being analyzed
            # the line must contain only one of the wells in the selection list, if contains more disregard it
            # the line looks something like "{well} {number}/{total number of wells}"
            if len(re.findall(r"\b" + "|".join(wells) + r"\b", line)) == 1:

                updated_running_wells(
                    set_progress,
                    line, 
                    store, 
                    docker_output
                )

            # Process 'Running' lines to update progress
            # if "Running" in line:
            #     process_running_wells(
            #         line,
            #         wells_analyzed,
            #         wells,
            #         volume,
            #         platename,
            #         plate_base,
            #         set_progress,
            #         docker_output,
            #     )

        # Wait for the subprocess to complete its execution
        process.communicate()  # Ensure all output has been processed and subprocess has finished

        if process.returncode == 0:
            wrmXpress_gui_obj.check_for_output_files()
            if wrmXpress_gui_obj.output_files_exist:
                return updated_thumbnail_generation(wrmXpress_gui_obj, docker_output)

            # TODO: Implement thumbnail generation, finish this when backend is finished
            return handle_thumbnail_generation(
                volume, platename, docker_output, output_file
            )

        else:

            print("wrmXpress has failed.")

            wrmXpress_gui_obj.check_for_output_files()
            if wrmXpress_gui_obj.output_files_exist:
                return updated_thumbnail_generation(wrmXpress_gui_obj, docker_output)

            # TODO: Implement failure handling
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
    multiplier=1,
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
    # Should try and figure out an alternative to this
    # potential brick mechanism for the user
    while not os.path.exists(current_well_path):
        time.sleep(1)

    # create figure from file path
    fig = create_figure_from_filepath(current_well_path)
    docker_output_formatted = "".join(docker_output)
    set_progress(
        (
            str(len(reconfiguring_well)),
            str(multiplier * len(wells)),
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
    multiplier=1,
    other_pipeline_wells=[],
):
    well_running = line.split(" ")[-1].strip()
    if well_running not in wells_analyzed:
        wells_analyzed.append(well_running)
        well_base_path = Path(
            volume,
            f"{platename}/TimePoint_1/{plate_base}_{well_running}",
        )
        # Use rglob with case-insensitive pattern matching for .TIF and .tif
        file_paths = list(
            well_base_path.parent.rglob(well_base_path.name + "*[._][tT][iI][fF]")
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

        if img_path.exists():
            fig = create_figure_from_filepath(img_path)
            docker_output_formatted = "".join(docker_output)

            set_progress(
                (
                    len(wells_analyzed) + len(other_pipeline_wells),
                    multiplier * len(wells),
                    fig,
                    f"```{str(img_path)}```",
                    f"```{docker_output_formatted}```",
                )
            )


def process_tracking_wells(
    line,
    tracking_well,
    wells,
    volume,
    platename,
    set_progress,
    docker_output,
    additional_wells=[],
    multiplier=1,
):
    if "Tracking well" in line:
        # find the well that is being analyzed
        current_well = line.split(" ")[-1].split(".")[0]
    elif "Running well" in line:
        # find the well that is being analyzed
        current_well = line.split(" ")[-1].strip()

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

    # Should try and figure out an alternative to this
    # potential brick mechanism for the user
    while not os.path.exists(current_well_path):
        time.sleep(1)

    # create figure from file path
    fig = create_figure_from_filepath(current_well_path)
    docker_output_formatted = "".join(docker_output)
    set_progress(
        (
            str(len(tracking_well) + len(additional_wells)),
            str(multiplier * len(wells)),
            fig,
            f"```{current_well_path}```",
            f"```{docker_output_formatted}```",
        )
    )


def process_img_number(
    line,
    wells,
    volume,
    platename,
    plate_base,
    pipeline_selection,
    set_progress,
    docker_output,
    wells_analyzed,
    additional_wells=[],
    multiplier=1,
):

    if len(additional_wells) != 0:
        additional_wells = wells

    csv_file_path = Path(volume, "input", f"image_paths_{pipeline_selection}.csv")

    # Should try and figure out an alternative to this
    # potential brick mechanism for the user
    while not os.path.exists(csv_file_path):
        time.sleep(1)

    read_csv = pd.read_csv(csv_file_path)
    well_column = read_csv["Metadata_Well"]
    image_number_pattern = re.search(r"Image # (\d+)", line)

    if image_number_pattern:
        image_number_pattern
        image_number = int(image_number_pattern.group(1))
        well_id = well_column.iloc[image_number - 1]
        well_base_path = Path(
            volume,
            f"{platename}/TimePoint_1/{plate_base}_{well_id}",
        )

        if well_id not in wells_analyzed:
            wells_analyzed.append(well_id)

        # Use rglob with case-insensitive pattern matching for .TIF and .tif
        file_paths = list(
            well_base_path.parent.rglob(well_base_path.name + "*[._][tT][iI][fF]")
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

        if img_path.exists():
            fig = create_figure_from_filepath(img_path)
            docker_output_formatted = "".join(docker_output)

            set_progress(
                (
                    (len(wells_analyzed) + len(additional_wells)),
                    str(multiplier * len(wells)),
                    fig,
                    f"```{img_path}```",
                    f"```{docker_output_formatted}```",
                )
            )


def process_info_and_percent(
    line,
    wells,
    volume,
    platename,
    plate_base,
    set_progress,
    docker_output,
    info_and_percent_wells,
    multiplier=1,
):
    info_parts = line.split("/")
    info_well_analyzed = info_parts[0].split(" ")[-1]
    info_total_wells = info_parts[1].split(" ")[0]

    if info_well_analyzed == info_total_wells:
        current_well = wells[int(info_well_analyzed) - 1]
        img_path = Path(
            volume,
            f"input/{platename}/TimePoint_1/{plate_base}_{current_well}.TIF",
        )

        info_and_percent_wells.append(current_well)

        if os.path.exists(img_path):
            fig = create_figure_from_filepath(img_path)
            docker_output_formatted = "".join(docker_output)

            set_progress(
                (
                    str(info_well_analyzed),
                    str(multiplier * int(info_total_wells)),
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
            set_progress(
                (
                    str(info_well_analyzed),
                    str(int(info_total_wells) * multiplier),
                    fig,
                    f"```{img_path}```",
                    f"```{docker_output_formatted}```",
                )
            )

def updated_thumbnail_generation(wrmXpress_gui_obj, docker_output):

    # TODO: Implement way to specify the figure to be returned rather than just the first one
    wrmXpress_gui_obj.sort_output_files()
    output_figure_path = wrmXpress_gui_obj.output_files[0]
    fig_1 = create_figure_from_filepath(output_figure_path)
    docker_output.append("Thumbnail generation completed successfully.")
    docker_output_formatted = "".join(docker_output)
    return (
        fig_1,
        False,
        False,
        "",
        f"```{docker_output_formatted}```",
        f"```{output_figure_path}```",
    )

def handle_thumbnail_generation(volume, platename, docker_output, output_file, pipeline=""):
    
    output_path_base = Path(volume, "output", pipeline)
    print('output_path_base', output_path_base)
    file_paths = list(
        output_path_base.parent.rglob(output_path_base.name + "*[._][pP][nN][gG]")
    )

    # Sort the matching files to find the one with the lowest suffix number
    if file_paths:
        file_paths_sorted = sorted(file_paths, key=lambda x: x.stem)
        # Select the first file (with the lowest number) if multiple matches are found
        output_path = file_paths_sorted[0]

    else:
        # Fallback if no matching files are found
        output_path = output_path_base.with_suffix(
            ".png"
        )  # Default to .TIF if no files found

    if os.path.exists(output_path):
        print("wrmXpress finished.")
        fig_1 = create_figure_from_filepath(output_path)
        docker_output.append("Thumbnail generation completed successfully.")
        docker_output_formatted = "".join(docker_output)
        return (
            fig_1,
            False,
            False,
            "",
            f"```{docker_output_formatted}```",
            f"```{output_path}```",
        )

    else:

        error_message = f"Thumbnail generation failed, please check the {output_file}."
        docker_output_formatted = "".join(docker_output)
        return (
            None,
            True,
            True,
            f"{error_message}",
            f"```{docker_output_formatted}```",
            None,
        )


def handle_failure(docker_output, output_file):
    error_message = f"wrmXpress has failed, please check the {output_file} for more information. Then clear the `work` directory and try again."
    docker_output_formatted = "".join(docker_output)
    return (
        None,
        True,
        True,
        f"{error_message}",
        f"```{docker_output_formatted}```",
        None,
    )
