# In[1]: Imports

import json
import os
import yaml
import shlex
import subprocess
import glob
import re
import shutil
from pathlib import Path
from app.utils.callback_functions import (
    get_default_value,
    eval_bool,
    clean_and_create_directories,
    copy_files_to_input_directory,
    create_figure_from_filepath,
)


# In[2]: WrmXpressGui Class
class WrmXpressGui:
    def __init__(
        self,
        file_structure,
        imaging_mode,
        multi_well_row,
        multi_well_col,
        multi_well_detection,
        x_sites,
        y_sites,
        stitch_switch,
        well_col,
        well_row,
        mask,
        mask_diameter,
        pipeline_selection,
        wavelengths,
        pyrscale,
        levels,
        winsize,
        iterations,
        poly_n,
        poly_sigma,
        flags,
        cellpose_model_segmentation,
        type_segmentation,
        python_model_sigma,
        wavelengths_segmentation,
        cellprofiler_pipeline_selection,
        cellpose_model_cellprofiler,
        wavelengths_cellprofiler,
        wavelengths_tracking,
        tracking_diameter,
        tracking_minmass,
        tracking_noisesize,
        tracking_searchrange,
        tracking_memory,
        tracking_adaptivestop,
        static_dx,
        static_dx_rescale,
        video_dx,
        video_dx_format,
        video_dx_rescale,
        mounted_volume,
        plate_name,
        well_selection_list,
    ):
        self.file_structure = file_structure
        self.imaging_mode = imaging_mode
        self.multi_well_row = multi_well_row
        self.multi_well_col = multi_well_col
        self.multi_well_detection = multi_well_detection
        self.x_sites = x_sites
        self.y_sites = y_sites
        self.stitch_switch = stitch_switch
        self.well_col = well_col
        self.well_row = well_row
        self.mask = mask
        self.mask_diameter = mask_diameter
        self.pipeline_selection = pipeline_selection
        self.wavelengths = wavelengths
        self.pyrscale = pyrscale
        self.levels = levels
        self.winsize = winsize
        self.iterations = iterations
        self.poly_n = poly_n
        self.poly_sigma = poly_sigma
        self.flags = flags
        self.cellpose_model_segmentation = cellpose_model_segmentation
        self.type_segmentation = type_segmentation
        self.python_model_sigma = python_model_sigma
        self.wavelengths_segmentation = wavelengths_segmentation
        self.cellprofiler_pipeline_selection = cellprofiler_pipeline_selection
        self.cellpose_model_cellprofiler = cellpose_model_cellprofiler
        self.wavelengths_cellprofiler = wavelengths_cellprofiler
        self.wavelengths_tracking = wavelengths_tracking
        self.tracking_diameter = tracking_diameter
        self.tracking_minmass = tracking_minmass
        self.tracking_noisesize = tracking_noisesize
        self.tracking_searchrange = tracking_searchrange
        self.tracking_memory = tracking_memory
        self.tracking_adaptivestop = tracking_adaptivestop
        self.static_dx = static_dx
        self.static_dx_rescale = static_dx_rescale
        self.video_dx = video_dx
        self.video_dx_format = video_dx_format
        self.video_dx_rescale = video_dx_rescale
        self.mounted_volume = mounted_volume
        self.plate_name = plate_name
        self.well_selection_list = well_selection_list
        self.error_occurred = False
        self.error_messages = []
        self.warning_occurred = False
        self.warning_messages = []
        self.check_cases = [None, "", " "]
        self.output_files = []
        self.output_files_exist = False

        # set progress files
        self.set_progress_running = False
        self.set_progress_current_number = None
        self.set_progress_total_number = None
        self.set_progress_figure = None
        self.set_progress_image_path = ""
        self.set_progress_docker_output = None

        self.preview_first_well_image_filepath = None

    # In[3]: Object Functions to store and retrieve data as dictionary and json for the GUI
    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())

    # In[4]: Validation Functions
    def validate_volume(self):
        if not self.mounted_volume:
            self.error_occurred = True
            self.error_messages.append("No volume selected.")
        else:
            if not os.path.exists(self.mounted_volume):
                self.error_occurred = True
                self.error_messages.append("Volume does not exist.")

    def validate_platename(self):
        if not self.plate_name:
            self.error_occurred = True
            self.error_messages.append("Plate/Folder name is missing.")

    def validate_platename_in_volume(self):
        platename_path = Path(self.mounted_volume, self.plate_name)
        if not os.path.exists(platename_path):
            self.error_occurred = True
            self.error_messages.append("Plate/Folder does not exist in the volume.")

    def validate_well_selection(self):
        if not self.well_selection_list:
            self.error_occurred = True
            self.error_messages.append("No wells selected.")

    def validate_pipeline_selection(self):
        if not self.pipeline_selection:
            self.error_occurred = True
            self.error_messages.append("No pipeline selected.")

    def validate_mask_parameters(self):
        if self.mask in ["circular", "square"] and not self.mask_diameter:
            self.warning_occurred = True
            self.warning_messages.append(
                "Mask diameter was not set. Default value (0) will be used."
            )

    def validate_multi_well_mode(self):
        if self.imaging_mode == "multi-well":
            if not self.multi_well_row:
                self.error_occurred = True
                self.error_messages.append(
                    "The number of rows for the multi-well plate is missing."
                )
            if not self.multi_well_col:
                self.error_occurred = True
                self.error_messages.append(
                    "The number of columns for the multi-well plate is missing."
                )

    def validate_multi_site_mode(self):
        if self.imaging_mode == "multi-site":
            if not self.x_sites:
                self.error_occurred = True
                self.error_messages.append(
                    "The number of x sites for the multi-site plate is missing."
                )
            if not self.y_sites:
                self.error_occurred = True
                self.error_messages.append(
                    "The number of y sites for the multi-site plate is missing."
                )
            if self.file_structure == "avi":
                self.error_occurred = True
                self.error_messages.append(
                    "Multi Site imaging with AVIs is not currently supported."
                )

    def validate_cellprofiler_cellpose_combos(self):
        if (
            "cellprofiler" in self.pipeline_selection
            and self.cellprofiler_pipeline_selection == "wormsize_intensity_cellpose"
            and self.cellpose_model_cellprofiler is None
        ):
            self.error_occurred = True
            self.error_messages.append(
                "A Cellpose model is required for the selected pipeline."
            )

    def validate_pipeline_parameters(self):
        if not self.pipeline_selection:
            self.error_occurred = True
            self.error_messages.append("No pipeline selected.")

        if "motility" in self.pipeline_selection:
            defaults = {
                "pyrscale": 0.5,
                "levels": 5,
                "winsize": 20,
                "iterations": 7,
                "poly_n": 5,
                "poly_sigma": 1.1,
            }
            for param, default in defaults.items():
                if not getattr(self, param):
                    self.warning_occurred = True
                    self.warning_messages.append(
                        f"{param} was not set. Default value ({default}) will be used."
                    )

        if (
            "segmentation" in self.pipeline_selection
            and self.type_segmentation == "python"
            and not self.python_model_sigma
        ):
            self.warning_occurred = True
            self.warning_messages.append(
                "Python model sigma was not set. Default value (0.25) will be used."
            )

        if "tracking" in self.pipeline_selection:

            defaults = {
                "tracking_diameter": 35,
                "tracking_minmass": 1200,
                "tracking_noisesize": 2,
                "tracking_searchrange": 45,
                "tracking_memory": 25,
                "tracking_adaptivestop": 30,
            }
            for param, default in defaults.items():
                if not getattr(self, param):
                    self.warning_occurred = True
                    self.warning_messages.append(
                        f"{param} was not set. Default value ({default}) will be used."
                    )

            try:
                tracking_diameter = (
                    self.tracking_diameter
                    if self.tracking_diameter is not None
                    else defaults["tracking_diameter"]
                )
                tracking_noisesize = (
                    self.tracking_noisesize
                    if self.tracking_noisesize is not None
                    else defaults["tracking_noisesize"]
                )

                if int(tracking_diameter) <= int(tracking_noisesize):
                    self.error_occurred = True
                    self.error_messages.append(
                        "Tracking diameter must be greater than tracking noise size."
                    )
            except TypeError:
                self.error_occurred = True
                self.error_messages.append(
                    "Invalid type for tracking diameter or tracking noise size."
                )

    def validate_avi_pipeline_parameters(self):
        if self.file_structure == "avi" and self.pipeline_selection not in [
            "motility",
            "tracking",
        ]:
            self.error_occurred = True
            self.error_messages.append(
                "Only motility and tracking pipelines are supported for AVI files."
            )

    def validate_imagexpress_mode(self, platename_path):
        if self.file_structure == "imagexpress":
            platename_path = Path(platename_path)

            # Search for .htd and .HTD files
            htd_files = list(platename_path.glob("*.htd"))
            HTD_files = list(platename_path.glob("*.HTD"))

            if not htd_files and not HTD_files:
                self.error_occurred = True
                self.error_messages.append(
                    "No .HTD file found in the Plate/Folder with ImageXpress file structure. You may have selected the wrong file structure."
                )

            # Validate subdirectories
            subdirectories = [x for x in platename_path.iterdir() if x.is_dir()]
            for subdirectory in subdirectories:
                files = list(subdirectory.glob("*"))
                for well in self.well_selection_list:
                    if not any([str(well) in str(file) for file in files]):
                        self.error_occurred = True
                        self.error_messages.append(
                            f"No images found for well {well}. This may result in unexpected errors or results."
                        )

    def validate_static_dx_mode(self):
        if (
            self.static_dx is not None
            and len(self.static_dx) == 1
            and not self.static_dx_rescale
        ):
            self.warning_occurred = True
            self.warning_messages.append(
                "Static DX rescale multiplier is missing, default value (1) will be used."
            )

    def validate_video_dx_mode(self):
        if (
            self.video_dx is not None
            and len(self.video_dx) == 1
            and not self.video_dx_rescale
        ):
            self.warning_occurred = True
            self.warning_messages.append(
                "Video DX rescale multiplier is missing, default value (0.5) will be used."
            )

    def validate_avi_mode(self):
        if self.file_structure == "avi":
            avi_folder_path = Path(self.mounted_volume, self.plate_name)
            # if self.imaging_mode == "single-well":
            #     avi_pattern = f"{self.plate_name}_"
            #     matched_files_avi = list(avi_folder_path.glob(avi_pattern + "*.avi"))

            #     if not matched_files_avi:
            #         self.error_occurred = True
            #         self.error_messages.append(
            #             "No AVI files found in the Plate/Folder."
            #         )

            #     for well in self.well_selection_list:
            #         pattern = f"{self.plate_name}_{well}"
            #         matched_files = list(avi_folder_path.glob(pattern + "*.avi"))
            #         if not matched_files:
            #             self.error_occurred = True
            #             self.error_messages.append(
            #                 f"No images found for well {well}. This may result in unexpected errors or results."
            #             )
            if self.imaging_mode == "multi-well":
                avi = f"{self.plate_name}.avi"
                if not os.path.exists(Path(avi_folder_path, avi)):
                    self.error_occurred = True
                    self.error_messages.append("No AVI file found in the Plate/Folder.")

    def validate_htd_file_cols_and_rows(self):
        """
        Validate that plate dimensions in the HTD file match expected dimensions.
        Populates error_messages and warning_messages as appropriate.
        """
        plate_base = self.plate_name.split("_", 1)[0]
        htd_file = Path(self.mounted_volume, self.plate_name, f"{plate_base}.HTD")

        if not htd_file.exists():
            self.error_occurred = True
            self.error_messages.append(f"HTD file not found: {htd_file}")
            return

        # Read file with multiple encoding attempts
        htd_data = self._read_file_with_multiple_encodings(htd_file)
        if htd_data is None:
            return  # Error already set in _read_file_with_multiple_encodings

        # Parse HTD data using a more robust approach
        plate_info = self._parse_htd_data(htd_data)

        # Validate dimensions against expected values
        self._validate_plate_dimensions(plate_info)

    def _read_file_with_multiple_encodings(self, file_path):
        """Helper method to attempt reading a file with different encodings."""
        encodings = ["utf-8", "utf-16", "iso-8859-1", "latin-1"]

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                self.warning_occurred = True
                self.warning_messages.append(
                    f"Error reading file with {encoding}: {str(e)}"
                )

        self.error_occurred = True
        self.error_messages.append(
            "Failed to read HTD file. Please check the file encoding."
        )
        return None

    def _parse_htd_data(self, htd_content):
        """Parse HTD file content to extract relevant information."""
        plate_info = {
            "x_wells": None,
            "y_wells": None,
            "description": None,
            "plate_type": None,
            "time_points": None,
        }

        # Define patterns for each key we want to extract
        patterns = {
            "x_wells": r'"XWells"\s*,\s*(\d+)',
            "y_wells": r'"YWells"\s*,\s*(\d+)',
            "description": r'"Description"\s*,\s*"([^"]*)"',
            "plate_type": r'"PlateType"\s*,\s*(\d+)',
            "time_points": r'"TimePoints"\s*,\s*(\d+)',
        }

        # Extract each value using regex
        for key, pattern in patterns.items():
            match = re.search(pattern, htd_content)
            if match:
                try:
                    # Convert numeric values to integers
                    if key in ["x_wells", "y_wells", "plate_type", "time_points"]:
                        plate_info[key] = int(match.group(1))
                    else:
                        plate_info[key] = match.group(1)
                except (ValueError, IndexError):
                    self.warning_occurred = True
                    self.warning_messages.append(
                        f"Failed to parse {key} from HTD file."
                    )

        # Check if required values were extracted
        for key in ["x_wells", "y_wells"]:
            if plate_info[key] is None:
                self.warning_occurred = True
                self.warning_messages.append(f"Failed to extract {key} from HTD file.")

        return plate_info

    def _validate_plate_dimensions(self, plate_info):
        """Validate that plate dimensions match expected values."""
        x_wells = plate_info.get("x_wells")
        y_wells = plate_info.get("y_wells")

        # Use default values if necessary
        expected_cols = self.well_col or 12
        expected_rows = self.well_row or 8

        # Validate dimensions if we were able to extract them
        if x_wells is not None and x_wells != expected_cols:
            self.error_occurred = True
            self.error_messages.append(
                f"Number of columns in the HTD file ({x_wells}) does not match "
                f"the number of columns selected ({expected_cols})."
            )

        if y_wells is not None and y_wells != expected_rows:
            self.error_occurred = True
            self.error_messages.append(
                f"Number of rows in the HTD file ({y_wells}) does not match "
                f"the number of rows selected ({expected_rows})."
            )

    def validate(self):
        self.validate_volume()
        self.validate_platename()
        self.validate_platename_in_volume()
        self.validate_well_selection()
        self.validate_mask_parameters()
        self.validate_multi_well_mode()
        self.validate_multi_site_mode()
        self.validate_cellprofiler_cellpose_combos()
        self.validate_pipeline_parameters()
        self.validate_static_dx_mode()
        self.validate_video_dx_mode()

        platename_path = Path(self.mounted_volume, self.plate_name)

        if platename_path:
            if self.file_structure == "imagexpress":
                self.validate_imagexpress_mode(platename_path)
                self.validate_htd_file_cols_and_rows()
            elif self.file_structure == "avi":
                self.validate_avi_mode()

        return (
            self.error_occurred,
            self.error_messages,
            self.warning_occurred,
            self.warning_messages,
        )

    # In[5]: Preparing the yaml file
    def prep_well_instance(self):
        # check if well selection is a list or stirng
        if isinstance(self.well_selection_list, str):
            self.well_selection_list = [self.well_selection_list]

        elif (
            isinstance(self.well_selection_list, list)
            and len(self.well_selection_list) == 96
        ):
            self.well_selection_list = self.well_selection_list

        # if length of well selection is 96, then change to "All"
        if self.well_selection_list is not None and len(self.well_selection_list) == 96:
            self.well_selection_list = ["All"]

    def set_default_multi_well_row_and_col(self):
        self.multi_well_row = get_default_value(self.multi_well_row, 1)
        self.multi_well_col = get_default_value(self.multi_well_col, 1)

    def set_default_x_sites_and_y_sites(self):
        self.x_sites = get_default_value(self.x_sites, "NA")
        self.y_sites = get_default_value(self.y_sites, "NA")

    def set_default_mask_diameter(self):
        if self.mask == "circular":
            self.circle_diameter = get_default_value(self.mask_diameter, 0)
            self.square_diameter = "NA"
        elif self.mask == "square":
            self.square_diameter = get_default_value(self.mask_diameter, 0)
            self.circle_diameter = "NA"
        else:
            self.circle_diameter = "NA"
            self.square_diameter = "NA"

    def set_well_and_column(self):
        self.well_col = get_default_value(self.well_col, 12)
        self.well_row = get_default_value(self.well_row, 8)

    def create_static_dx_dict(self):
        self.static_dx_dict = {
            "run": (
                eval_bool(self.static_dx[0])
                if self.static_dx is not None and len(self.static_dx) == 1
                else False
            ),
            "rescale_multiplier": (
                get_default_value(self.static_dx_rescale, 1)
                if self.static_dx is not None and len(self.static_dx) == 1
                else 1
            ),
        }

    def create_video_dx_dict(self):
        self.video_dx_dict = {
            "run": (
                eval_bool(self.video_dx[0])
                if self.video_dx is not None and len(self.video_dx) == 1
                else False
            ),
            "format": (
                get_default_value(self.video_dx_format, "avi")
                if self.video_dx is not None and len(self.video_dx) == 1
                else "avi"
            ),
            "rescale_multiplier": (
                get_default_value(self.video_dx_rescale, 0.5)
                if self.video_dx is not None and len(self.video_dx) == 1
                else 0.5
            ),
        }

    def modify_params_if_single_well(self):
        if self.imaging_mode == "single-well":
            self.multi_well_row = 1
            self.multi_well_col = 1
            self.x_sites = "NA"
            self.y_sites = "NA"
            # self.well_selection_list = ["All"] # commented out as this might have been the problem
            self.multi_well_detection = "grid"
            self.stitch_switch = False

    def modify_params_if_multi_well(self):
        if self.imaging_mode == "multi-well":
            self.x_sites = "NA"
            self.y_sites = "NA"
            self.multi_well_detection = "grid"
            self.stitch_switch = False

    def modify_params_if_multi_site(self):
        if self.imaging_mode == "multi-site":
            self.multi_well_row = 1
            self.multi_well_col = 1
            # self.well_selection_list = ["All"] # commented out as this might have been the problem
            self.multi_well_detection = "grid"
            self.stitch_switch = get_default_value(self.stitch_switch, False)

    def pre_motility_run_dict(self):
        # Base dictionary with default values
        self.motility_run_dict = {
            "run": False,
            "wavelengths": ["All"],
            "pyrScale": 0.5,
            "levels": 5,
            "winsize": 20,
            "iterations": 7,
            "poly_n": 5,
            "poly_sigma": 1.1,
            "flags": 0,
            "flow": None,
        }

        # Update dictionary if pipeline_selection is "motility"
        if "motility" in self.pipeline_selection:
            self.motility_run_dict.update(
                {
                    "run": True,
                    "wavelengths": [self.wavelengths],
                    "pyrScale": get_default_value(self.pyrscale, 0.5),
                    "levels": get_default_value(self.levels, 5),
                    "winsize": get_default_value(self.winsize, 20),
                    "iterations": get_default_value(self.iterations, 7),
                    "poly_n": get_default_value(self.poly_n, 5),
                    "poly_sigma": get_default_value(self.poly_sigma, 1.1),
                    "flags": get_default_value(self.flags, 0),
                    "flow": None,
                }
            )

    def prep_cell_profile_dict(self):
        self.cell_profile_dict = {
            "run": False,
            "cellpose_wavelength": "w1",
            "cellpose_model": "20220830_all",
            "pipeline": "wormsize_intensity_cellpose",
        }
        if "cellprofiler" in self.pipeline_selection:
            self.cell_profile_dict.update(
                {
                    "run": True,
                    "cellpose_wavelength": self.wavelengths_cellprofiler,
                    "cellpose_model": self.cellpose_model_cellprofiler,
                    "pipeline": get_default_value(
                        self.cellprofiler_pipeline_selection,
                        "wormsize_intensity_cellpose",
                    ),
                }
            )

    def prep_tracking_dict(self):
        self.tracking_dict = {
            "run": False,
            "wavelengths": ["All"],
            "diameter": 35,
            "minmass": 1200,
            "noisesize": 2,
            "searchrange": 45,
            "memory": 25,
            "adaptivestop": 30,
        }

        if "tracking" in self.pipeline_selection:
            self.tracking_dict.update(
                {
                    "run": True,
                    "wavelengths": [self.wavelengths_tracking],
                    "diameter": get_default_value(self.tracking_diameter, 35),
                    "minmass": get_default_value(self.tracking_minmass, 1200),
                    "noisesize": get_default_value(self.tracking_noisesize, 2),
                    "searchrange": get_default_value(self.tracking_searchrange, 45),
                    "memory": get_default_value(self.tracking_memory, 25),
                    "adaptivestop": get_default_value(self.tracking_adaptivestop, 30),
                }
            )

    def prep_segmentation_dict(self):
        # Base dictionary with default values
        self.segmentation_dict = {
            "run": False,
            "model": "cellpose",
            "model_type": "20220830_all",
            "model_sigma": 0.25,
            "wavelengths": ["All"],
        }

        if "segmentation" in self.pipeline_selection:
            update_dict = {
                "run": True,
                "model": self.cellpose_model_segmentation,
                "model_type": self.type_segmentation,
                "wavelengths": [self.wavelengths_segmentation],
            }

            if self.type_segmentation == "python":
                update_dict["model_sigma"] = get_default_value(
                    self.python_model_sigma, 0.25
                )

            self.segmentation_dict.update(update_dict)

    def create_yaml_dict(self):
        yml = {
            "imaging_mode": [self.imaging_mode],
            "file_structure": [self.file_structure],
            "well-row": self.well_row,
            "well-col": self.well_col,
            "multi-well-row": self.multi_well_row,
            "multi-well-col": self.multi_well_col,
            "multi-well-detection": self.multi_well_detection,
            "x-sites": self.x_sites,
            "y-sites": self.y_sites,
            "stitch": self.stitch_switch,
            "circle_diameter": self.circle_diameter,
            "square_side": self.square_diameter,
            "pipelines": {
                "static_dx": self.static_dx_dict,
                "video_dx": self.video_dx_dict,
                "optical_flow": self.motility_run_dict,
                "segmentation": self.segmentation_dict,
                "cellprofiler": self.cell_profile_dict,
                "tracking": self.tracking_dict,
            },
            "wells": self.well_selection_list,
            "directories": {
                "work": [str(Path(self.mounted_volume, "work"))],
                "input": [str(Path(self.mounted_volume, "input"))],
                "output": [str(Path(self.mounted_volume, "output"))],
            },
        }

        return yml

    def prep_yml(self):
        self.prep_well_instance()
        self.set_default_multi_well_row_and_col()
        self.set_default_x_sites_and_y_sites()
        self.set_default_mask_diameter()
        self.set_well_and_column()
        self.create_static_dx_dict()
        self.create_video_dx_dict()
        self.modify_params_if_single_well()
        self.modify_params_if_multi_well()
        self.modify_params_if_multi_site()
        self.pre_motility_run_dict()
        self.prep_cell_profile_dict()
        self.prep_tracking_dict()
        self.prep_segmentation_dict()

        return self.create_yaml_dict()

    # In[6]: Select Diagnostic Image to Preview

    def get_motility_image_diagnostic_parameters(self):
        return (
            {
                "Optical flow": "optical_flow",
            }
            if "motility" in self.pipeline_selection
            else {}
        )

    def get_segmentation_image_diagnostic_parameters(self):
        return (
            {
                "Segmentation": "segmentation",
            }
            if "segmentation" in self.pipeline_selection
            else {}
        )

    def get_tracking_image_diagnostic_parameters(self):
        return {"Tracks": "tracks"} if "tracking" in self.pipeline_selection else {}

    def get_cell_profile_image_diagnostic_parameters(self):
        if "cellprofiler" in self.pipeline_selection:
            pipeline_mapping = {
                "wormsize_intensity_cellpose": {
                    "Straightened worms": "straightened_worms",
                    "Cellpose masks": "cellprofiler",
                },
                "mf_celltox": {
                    "raw": "raw",
                },
                "wormsize": {
                    # "straightened_worms": "straightened_worms", # when I ran this pipeline, I did not get straightened_worms in the output directory
                },
                "feeding": {
                    # "straightened_worms": "straightened_worms", # when I ran this pipeline, I did not get straightened_worms in the output directory
                },
            }

            return pipeline_mapping.get(self.cellprofiler_pipeline_selection, {})

        return {}

    def get_wavelengths_from_files(self, params):
        plate_folder = Path(self.mounted_volume, self.plate_name)

        # Find the first folder containing "TimePoint_"
        timepoint_folders = [
            folder for folder in plate_folder.iterdir() if "TimePoint_" in folder.name
        ]
        if not timepoint_folders:
            raise FileNotFoundError(
                f"No folders containing 'TimePoint_' found in {plate_folder}"
            )

        first_folder = timepoint_folders[0]

        # Find all files in the first folder
        all_files = list(first_folder.glob("*"))

        # Extract unique wavelengths from filenames
        wavelengths = {
            file.stem.split("_")[-1]
            for file in all_files
            if "w" in file.stem.split("_")[-1]  # Ensure the part contains 'w'
        }

        # add wavelengths to params for each wavelength have a key where its wavelength_{number} with the value of the w{number}
        for i, wavelength in enumerate(wavelengths):
            params[f"wavelength_{i + 1}"] = wavelength

        return params

    def get_static_dx_image_diagnostic_parameters(self):
        return (
            {
                "static_dx": "static_dx",
            }
            if self.static_dx
            else {}
        )

    def get_video_dx_image_diagnostic_parameters(self):
        return (
            {
                "video_dx": "video_dx",
            }
            if self.video_dx
            else {}
        )

    def get_image_diagnostic_parameters(self):
        motility_params = self.get_motility_image_diagnostic_parameters()
        segmentation_params = self.get_segmentation_image_diagnostic_parameters()
        tracking_params = self.get_tracking_image_diagnostic_parameters()
        cell_profile_params = self.get_cell_profile_image_diagnostic_parameters()
        # static_dx_params = self.get_static_dx_image_diagnostic_parameters()
        # video_dx_params = self.get_video_dx_image_diagnostic_parameters()

        # get the params that is not {}

        params = {
            **motility_params,
            **segmentation_params,
            **tracking_params,
            **cell_profile_params,
            # **static_dx_params,
            # **video_dx_params,
        }

        if (
            self.file_structure == "imagexpress"
            and self.pipeline_selection == "cellprofiler"
            and self.cellprofiler_pipeline_selection != "feeding"
        ):
            params = self.get_wavelengths_from_files(params)

        return {
            **params,
        }

    # In[7]: Analysis Methods

    def preamble_analysis(self, file_structure, first_well=False):

        # Prepare paths
        image_directory = Path(self.mounted_volume, self.plate_name)
        input_directory = Path(self.mounted_volume, "input")
        platename_input_directory = Path(input_directory, self.plate_name)
        work_directory = Path(self.mounted_volume, "work")
        output_directory = Path(self.mounted_volume, "output")

        # Clean and create directories
        self.clean_and_create_directories(
            input_path=platename_input_directory,
            work_path=work_directory,
            output_path=output_directory,
        )

        # Handle specific file structure logic
        htd_file = None
        plate_base = None
        if file_structure == "imagexpress":
            plate_base = self.plate_name.split("_", 1)[0]
            htd_file = Path(image_directory, f"{plate_base}.HTD")
        elif file_structure == "avi":
            plate_base = self.plate_name
            htd_file = None

        # Determine wells to copy
        wells_to_process = (
            self.get_first_well() if first_well else self.well_selection_list
        )

        # Copy files to input directory
        copy_files_to_input_directory(
            platename_input_dir=platename_input_directory,
            htd_file=htd_file,
            img_dir=image_directory,
            plate_base=plate_base,
            wells=wells_to_process,
            platename=self.plate_name,
            file_structure=self.file_structure,
        )

    def clean_and_create_directories(self, input_path, work_path, output_path=None):
        """
        Cleans and creates the input, work, and optionally output directories.
        Deletes existing contents and recreates the directories as needed.
        """
        # Ensure the paths are Path objects
        input_path = Path(input_path)
        work_path = Path(work_path)
        output_path = Path(output_path) if output_path else None

        # Clean and create the work directory
        if work_path.exists():
            shutil.rmtree(work_path)
        work_path.mkdir(parents=True, exist_ok=True)

        # Clean and create the input directory
        if input_path.exists():
            shutil.rmtree(input_path)
        input_path.mkdir(parents=True, exist_ok=True)

        # Clean and create the output directory, if specified
        if output_path:
            if output_path.exists():
                for item in output_path.iterdir():
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            else:
                output_path.mkdir(parents=True, exist_ok=True)

    def analysis_setup(self, type_of_analysis):
        if type_of_analysis == "preview":
            self.run_preview_analysis(file_structure=self.file_structure)
        elif type_of_analysis == "run":
            self.setup_run_analysis(file_structure=self.file_structure)

    def prepare_wrmxpress_command(self):

        # Helper methods within the class
        def generate_command(is_preview=False):
            """Generate the command split for wrmXpress based on preview flag."""
            file_prefix = f".{self.plate_name}" if is_preview else self.plate_name
            command = f"python /root/wrmXpress/wrapper.py {self.mounted_volume}{file_prefix}.yml {self.plate_name}"
            return shlex.split(command)

        def generate_log_file(is_preview=False):
            """Generate the log file path for wrmXpress based on preview flag."""
            log_file_name = (
                f"{self.plate_name}_preview.log"
                if is_preview
                else f"{self.plate_name}.log"
            )
            return Path(self.mounted_volume, "work", log_file_name)

        # Core logic
        self.command_message = f"```python /root/wrmXpress/wrapper.py {self.plate_name}.yml {self.plate_name}```"
        self.wrmxpress_preview_command_split = generate_command(is_preview=True)
        self.wrmxpress_command_split = generate_command()
        self.output_preview_log_file = generate_log_file(is_preview=True)
        self.output_log_file = generate_log_file()

    # In[8]: Preview Analysis Methods

    def get_first_well(self):

        if (
            self.well_selection_list is not None
            and len(self.well_selection_list) == 1
            and self.well_selection_list[0] != "All"
        ):
            print("First well is not All")
            first_well = self.well_selection_list[0]
        elif self.well_selection_list == ["All"]:
            first_well = "A01"
        elif self.well_selection_list is not None and len(self.well_selection_list) > 0:
            first_well = self.well_selection_list[0]
        else:
            first_well = "A01"  # default fallback

        return first_well

    def prepare_preview_yaml(self):
        # convert well selection to first well
        configure_yaml_file = self.prep_yml()

        first_well = self.get_first_well()

        configure_yaml_file["wells"] = [first_well]

        preview_yaml_platename = "." + self.plate_name + ".yml"
        preview_yaml_filepath = Path(self.mounted_volume, preview_yaml_platename)

        with open(preview_yaml_filepath, "w") as f:
            yaml.dump(configure_yaml_file, f)

    def run_preview_analysis(self, file_structure):
        """
        Runs a preview analysis for the first well.
        If the analysis has already been performed, it loads the preview image.
        Otherwise, it prepares and executes the analysis.
        """
        try:
            # Check if the first well has already been analyzed
            # if self.first_well_already_run():
            #     self._load_preview_image()
            #     return
            # Prepare necessary files and commands for analysis
            self.prepare_preview_yaml()
            self.preamble_analysis(file_structure, first_well=True)
            self.prepare_wrmxpress_command()

            # Run wrmXpress using the prepared command
            docker_output = self._run_wrmxpress_subprocess(
                self.wrmxpress_preview_command_split, self.output_preview_log_file
            )

            # Check again if the first well has been processed after running the command
            if self.first_well_already_run():
                print("wrmXpress completed successfully.")
                self._load_preview_image()

            return docker_output

        except Exception as e:
            print(f"Error in run_preview_analysis: {e}")
            self.run_preview_error_message = f"Error: {str(e)}"

    # Helper methods
    def _load_preview_image(self):
        """
        Loads the preview image for the first well and creates a figure.
        """
        fig = create_figure_from_filepath(self.preview_first_well_image_filepath)
        self.preview_first_well_figure = fig
        self.formatted_preview_first_well_path = (
            f"```{self.preview_first_well_image_filepath}```"
        )

    def _run_wrmxpress_subprocess(self, command_split, log_file):
        """
        Executes the wrmXpress command as a subprocess and returns its output.
        """
        try:
            print("Running wrmXpress: Preview.")
            docker_output = ["Running wrmXpress: Preview."]
            with open(log_file, "w") as file:
                process = subprocess.Popen(
                    command_split,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    env={**os.environ, "PYTHONUNBUFFERED": "1"},
                )
                for line in iter(process.stdout.readline, ""):
                    docker_output.append(line)
                    file.write(line)
                    file.flush()

                if process.returncode != 0 and process.returncode is not None:
                    print(process.returncode)
                    raise RuntimeError(f"wrmXpress failed: {docker_output[-1]}")

        except Exception as e:
            docker_output.append(f"Error: {str(e)}")
            print(f"Subprocess execution failed: {e}")

        return docker_output

    def first_well_already_run(self):
        """
        Checks if the first well has already been processed and a preview image exists.
        Returns True if the image is found, otherwise False.
        """
        pipeline = []
        if "motility" in self.pipeline_selection:
            pipeline.append("optical_flow")

        if "segmentation" in self.pipeline_selection:
            pipeline.append("segmentation")

        elif "tracking" in self.pipeline_selection:
            pipeline.append("tracking")

        elif "cellprofiler" in self.pipeline_selection:
            pipeline.append("cellprofiler")

        # pipeline = Path(self.mounted_volume, "work", f"{pipeline}")
        # get a list of the different pipeline paths in work directory
        pipeline_directory = [
            Path(self.mounted_volume, "work", f"{pipeline}") for pipeline in pipeline
        ]

        output_directory = [
            Path(self.mounted_volume, "output", f"{pipeline}", "img")
            for pipeline in pipeline
        ]
        pipeline_directory = pipeline_directory + output_directory

        first_well = self.get_first_well()
        png_file_pattern = f"*{first_well}*.png"
        tiff_file_pattern = f"*{first_well}*.tiff"
        try:
            for pipe in pipeline_directory:
                # Search for the first matching .png file
                first_well_image = next(pipe.glob(png_file_pattern), None)

                if first_well_image:
                    self.preview_first_well_image_filepath = first_well_image
                    return True

                # Search for the first matching .tiff file
                first_well_image = next(pipe.glob(tiff_file_pattern), None)

                if first_well_image:
                    self.preview_first_well_image_filepath = first_well_image
                    return True

        except Exception as e:
            print(f"Error checking for first well: {e}")

            return False
        return False

    # In[9]: Aprés analysis

    def check_for_output_files(self):
        output_directory = Path(self.mounted_volume, "output")
        plate_base = self.plate_name.split("_", 1)[0]

        if self.pipeline_selection == "cellprofiler":
            self.pipeline_selection = ["cellprofiler"]

        # Derive selected pipelines
        selected_pipelines = [
            "optical_flow" if p == "motility" else p for p in self.pipeline_selection
        ]
        if self.static_dx:
            selected_pipelines.append("static_dx")
        if self.video_dx:
            selected_pipelines.append("video_dx")

        # Initialize output files if not already done
        self.output_files_exist = False
        self.output_files = []

        # Search for output files in the specified pipelines
        for pipeline in selected_pipelines:
            if pipeline == "cellprofiler":
                pipeline_dir = Path(output_directory, pipeline)
                pipeline_img_dir = Path(output_directory, pipeline, "img")
            else:
                pipeline_dir = Path(output_directory, pipeline)
            if not pipeline_dir.exists():
                continue  # Skip if the directory doesn't exist

            # Collect PNG and TIF files
            files = (
                list(pipeline_dir.glob("*.PNG"))
                + list(pipeline_dir.glob("*.TIF"))
                + list(pipeline_dir.glob("*.tiff"))
            )

            if pipeline_img_dir.exists():
                files = list(pipeline_img_dir.glob("*.tiff"))

            # Check for plate_base consistency in file names
            matching_files = [file for file in files if plate_base in file.name]

            if matching_files:
                self.output_files_exist = True
                self.output_files.extend(matching_files)

    def sort_output_files(self):
        # set static_dx and video_dx to the last files
        static_dx_files = [
            file for file in self.output_files if "static_dx" in file.name
        ]
        video_dx_files = [file for file in self.output_files if "video_dx" in file.name]

        # remove the static_dx and video_dx files from the output_files list
        self.output_files = [
            file
            for file in self.output_files
            if file not in static_dx_files and file not in video_dx_files
        ]

    def set_processing_arguments(
        self, current_number, total_number, figure, image_path
    ):
        self.set_progress_running = True
        self.set_progress_current_number = current_number
        self.set_progress_total_number = total_number
        self.set_progress_figure = figure
        self.set_progress_image_path = image_path

    def get_output_file_path(self, selection):
        # print(self.output_files)
        returned_files = []

        if selection == "straightened_worms":
            return self.get_straightened_worms_file_path()

        if selection in ["w1", "w2", "w3", "w4"]:
            return self.get_wavelength_file_path(selection)

        for file in self.output_files:
            if selection in str(file):
                returned_files.append(file)

        # check if any of the wells from self.well_selection_list is in the file name
        if len(returned_files) >= 1:
            for file in returned_files:
                # first well in well selection list is in the file name
                if (
                    self.well_selection_list is not None
                    and len(self.well_selection_list) > 0
                    and self.well_selection_list[0] in str(file)
                ):
                    return file

        return returned_files

    def get_straightened_worms_file_path(self):
        # get the straightened_worms file path
        # ensure output files exist
        if self.output_files_exist:
            # search the cellprofiler folder for a directory called "img"
            cellprofiler_dir = Path(self.mounted_volume, "output", "cellprofiler")
            img_dir = Path(cellprofiler_dir, "img")

            # check if this directory exists
            if img_dir.exists():
                # get the first file in the img directory
                straightened_worms_files = list(img_dir.glob("*"))
                print(straightened_worms_files)
                # ensure this first file has extension of png/tiff if not remove it
                for file in straightened_worms_files:
                    if file.suffix not in [".png", ".tiff", ".tif"]:
                        straightened_worms_files.remove(file)

                return straightened_worms_files

    # TODO: update this
    def get_wavelength_file_path(self, selection):
        # get the wavelength file path
        # ensure output files exist
        if self.output_files_exist:
            # search the cellprofiler folder for a directory called "img"
            cellprofiler_dir = Path(self.mounted_volume, "output", "static_dx")
            img_dir = Path(cellprofiler_dir, "img")

            # check if this directory exists
            if img_dir.exists():
                # get the first file in the img directory
                wavelength_files = list(img_dir.glob(f"*{selection}*"))

                # ensure this first file has extension of png/tiff if not remove it
                for file in wavelength_files:
                    if file.suffix not in [".png", ".tiff", ".tif"]:
                        wavelength_files.remove(file)

                return wavelength_files

    # In[8]: Run Analysis

    def setup_run_analysis(self, file_structure):
        # Prepare for analysis
        self.preamble_analysis(file_structure)
        self.prepare_wrmxpress_command()

    def run_analysis(self, set_progress):
        # Run wrmXpress using the prepared command
        docker_output = self._run_wrmxpress_subprocess_analysis(
            self.wrmxpress_command_split, set_progress
        )

        return docker_output

    def _run_wrmxpress_subprocess_analysis(self, command_split, set_progress):
        """
        Executes the wrmXpress command as a subprocess and prints its output to the terminal in real-time.
        """
        print("Running wrmXpress: Run.")
        docker_output = ["Running wrmXpress."]

        # Use subprocess.Popen to execute the command and capture the output line-by-line
        process = subprocess.Popen(
            command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )

        # Read and print the output line-by-line
        for line in process.stdout:
            line = line.strip()  # Remove any trailing whitespace
            if line:
                print(line)  # Print each line to the terminal
                docker_output.append(line)

        # Wait for the process to finish
        process.wait()

        return docker_output

        """
        # Read and process the output in real-time
        for line in process.stdout:
            docker_output.append(line.strip())
            print(line.strip())  # Print each line as it's received

            # Check if any of the wells from well_selection_list is in the line
            if any([well in line for well in self.well_selection_list]):
                well_being_analyzed, progress = line.split(" ")
                current_progress, total_progress = progress.split("/")
                print(
                    f"Current Progress: {current_progress}, Total Progress: {total_progress}"
                )
                plate_base = self.plate_name.split("_")[0]

                # Hard code for now
                wave_length = "w1"

                well_analyzed_base_path = Path(
                    self.mounted_volume,
                    "input",
                    self.plate_name,
                    "TimePoint_1",
                    f"{plate_base}_{well_being_analyzed}_{wave_length}",
                )
                file_paths = list(
                    well_analyzed_base_path.parent.rglob(
                        f"{plate_base}_{well_being_analyzed}_{wave_length}"
                        + "*[._][tT][iI][fF]"
                    )
                )
                if file_paths:
                    file_paths_sorted = sorted(file_paths, key=lambda x: x.stem)
                    img_path = file_paths_sorted[-1]
                else:
                    img_path = well_analyzed_base_path.with_suffix(".TIF")

                if img_path.exists():
                    figure = create_figure_from_filepath(img_path)

                    docker_output_formatted = "".join(docker_output)

                    # Set the progress
                    set_progress(
                        (
                            int(current_progress),
                            int(total_progress),
                            figure,
                            f"```{str(well_analyzed_base_path)}```",
                            f"```{docker_output_formatted}```",
                        )
                    )

        # Wait for the process to complete
        process.wait()

        return docker_output
        """


"""
    def _run_wrmxpress_subprocess_analysis(self, command_split, set_progress):

        print("Running wrmXpress.")
        docker_output = ["Running wrmXpress."]
        try:
            # Use subprocess.run to execute the command and capture the output
            process = subprocess.run(
                command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=True,  # Raise exception if the command fails
            )

            # Print each line of the output to the terminal
            for line in process.stdout.splitlines():
                docker_output.append(line)
                print(line)

                # Check if any of the wells from well_selection_list is in the line
                if any([well in line for well in self.well_selection_list]):
                    well_being_analyzed, progress = line.split(" ")
                    # Process progress data
                    current_progress, total_progress = progress.split("/")
                    print(
                        f"Current Progress: {current_progress}, Total Progress: {total_progress}"
                    )
                    plate_base = self.plate_name.split("_")[0]

                    # Hard code for now
                    wave_length = "w1"

                    well_analyzed_base_path = Path(
                        self.mounted_volume,
                        "input",
                        self.plate_name,
                        "TimePoint_1",
                        f"{plate_base}_{well_being_analyzed}_{wave_length}",
                    )
                    file_paths = list(
                        well_analyzed_base_path.parent.rglob(
                            f"{plate_base}_{well_being_analyzed}_{wave_length}"
                            + "*[._][tT][iI][fF]"
                        )
                    )
                    if file_paths:
                        file_paths_sorted = sorted(file_paths, key=lambda x: x.stem)
                        img_path = file_paths_sorted[-1]
                    else:
                        img_path = well_analyzed_base_path.with_suffix(".TIF")

                    # Check if the file exists
                    if img_path.exists():
                        figure = create_figure_from_filepath(img_path)

                        docker_output_formatted = "".join(docker_output)

                        # Set the progress
                        set_progress(
                            (
                                int(current_progress),
                                int(total_progress),
                                figure,
                                f"```{str(well_analyzed_base_path)}```",
                                f"```{docker_output_formatted}```",
                            )
                        )

            return docker_output

        except subprocess.CalledProcessError as e:
            # Capture the error output
            error_message = e.stdout if e.stdout else str(e)
            docker_output.append(f"Error: {error_message}")
            print(f"Command failed with error: {error_message}")

        except Exception as e:
            docker_output.append(f"Error: {str(e)}")
            print(f"Execution failed: {e}")

        return docker_output
"""
