# In[1]: Imports

import json
import os
import yaml
import shlex
import subprocess
from pathlib import Path
from app.utils.callback_functions import get_default_value, eval_bool, clean_and_create_directories, copy_files_to_input_directory

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
        cellpose_model_type_segmentation,
        python_model_sigma,
        wavelengths_segmentation,
        cellprofiler_pipeline_selection,
        cellpose_model_cellprofile,
        wavelengths_cellprofile,
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
        self.cellpose_model_type_segmentation = cellpose_model_type_segmentation
        self.python_model_sigma = python_model_sigma
        self.wavelengths_segmentation = wavelengths_segmentation
        self.cellprofiler_pipeline_selection = cellprofiler_pipeline_selection
        self.cellpose_model_cellprofile = cellpose_model_cellprofile
        self.wavelengths_cellprofile = wavelengths_cellprofile
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

    # In[3]: Object Functions to stroe and retrieve data as dictionary and json for the GUI
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
                "Mask diameter is missing. Default value (0) will be used."
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

    def validate_pipeline_parameters(self):
        if not self.pipeline_selection:
            self.error_occurred = True
            self.error_messages.append("No pipeline selected.")

        if self.pipeline_selection == "motility":
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
                        f"{param} is missing. Default value ({default}) will be used."
                    )

        if self.pipeline_selection == "segmentation" and not self.python_model_sigma:
            self.warning_occurred = True
            self.warning_messages.append(
                "Python model sigma is missing. Default value (0.25) will be used."
            )

        if self.pipeline_selection == "tracking":
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
                        f"{param} is missing. Default value ({default}) will be used."
                    )

    def validate_avi_pipeline_parameters(self):
        if self.file_structure == "avi" and self.pipeline_selection not in ["motility", "tracking"]:
            self.error_occurred = True
            self.error_messages.append("Only motility and tracking pipelines are supported for AVI files.")

    def validate_imagexpress_mode(self, platename_path):
        if self.file_structure == "imagexpress":
            platename_path = Path(platename_path)

            # Search for .htd and .HTD files
            htd_files = list(platename_path.glob("*.htd"))
            HTD_files = list(platename_path.glob("*.HTD"))

            if not htd_files and not HTD_files:
                self.error_occurred = True
                self.error_messages.append("No .HTD file found in the Plate/Folder.")

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

    def validate_avi_mode(self):
        if self.file_structure == "avi":
            avi_folder_path = Path(self.mounted_volume, self.plate_name)
            avi_pattern = f"{self.plate_name}_"
            matched_files_avi = list(avi_folder_path.glob(avi_pattern + "*.avi"))

            if not matched_files_avi:
                self.error_occurred = True
                self.error_messages.append("No AVI files found in the Plate/Folder.")

            for well in self.well_selection_list:
                pattern = f"{self.plate_name}_{well}"
                matched_files = list(avi_folder_path.glob(pattern + "*.avi"))
                if not matched_files:
                    self.error_occurred = True
                    self.error_messages.append(
                        f"No images found for well {well}. This may result in unexpected errors or results."
                    )

    def validate(self):
        self.validate_volume()
        self.validate_platename()
        self.validate_platename_in_volume()
        self.validate_well_selection()
        self.validate_mask_parameters()
        self.validate_multi_well_mode()
        self.validate_multi_site_mode()
        self.validate_pipeline_parameters()

        platename_path = Path(self.mounted_volume, self.plate_name)

        if platename_path:
            if self.file_structure == "imagexpress":
                self.validate_imagexpress_mode(platename_path)
            elif self.file_structure == "avi":
                self.validate_avi_mode()

        return self.error_occurred, self.error_messages, self.warning_occurred, self.warning_messages

    # In[5]: Preparing the yaml file
    def prep_well_instance(self):
        # check if well selection is a list or stirng
        if isinstance(self.well_selection_list, str):
            self.well_selection_list = [self.well_selection_list]

        # if length of well selection is 96, then change to "All"
        if len(self.well_selection_list) == 96:
            self.well_selection_list = ["All"]

    def set_default_multi_well_row_and_col(self):
        self.multi_well_row = get_default_value(self.multi_well_row, 1)
        self.multi_well_col = get_default_value(self.multi_well_col, 1)

    def set_default_x_sites_and_y_sites(self):
        self.x_sites = get_default_value(self.x_sites, "NA")
        self.y_sites = get_default_value(self.y_sites, "NA")

    def set_default_mask_diameter(self):
        if self.mask == "circular":
            self.circle_diameter = get_default_value(self.mask_diameter, "NA")
            self.square_diameter = "NA"
        elif self.mask == "square":
            self.square_diameter = get_default_value(self.mask_diameter, "NA")
            self.circle_diameter = "NA"
        else:
            self.circle_diameter = "NA"
            self.square_diameter = "NA"

    def set_well_and_column(self):
        self.well_col = get_default_value(self.well_col, 12)
        self.well_row = get_default_value(self.well_row, 8)

    def create_static_dx_dict(self):
        self.static_dx_dict = {
            "run": eval_bool(self.static_dx[0]) if len(self.static_dx) == 1 else False,
            "rescale_multiplier": (
                get_default_value(self.static_dx_rescale, 1)
                if len(self.static_dx) == 1
                else 1
            ),
        }

    def create_video_dx_dict(self):
        self.video_dx_dict = {
            "run": eval_bool(self.video_dx[0]) if len(self.video_dx) == 1 else False,
            "format": get_default_value(self.video_dx_format, "avi")
            if len(self.video_dx) == 1
            else "avi",
            "rescale_multiplier": (
                get_default_value(self.video_dx_rescale, 1)
                if len(self.video_dx) == 1
                else 1
            ),
        }

    def modify_params_if_single_well(self):
        if self.imaging_mode == "single-well":
            self.multi_well_row = 1
            self.multi_well_col = 1
            self.x_sites = "NA"
            self.y_sites = "NA"
            self.well_selection_list = ["All"]
            self.multi_well_detection = 'grid'
            self.stitch_switch = False

    def modify_params_if_multi_well(self):
        if self.imaging_mode == "multi-well":
            self.x_sites = "NA"
            self.y_sites = "NA"
            self.multi_well_detection = 'grid'
            self.stitch_switch = False

    def modify_params_if_multi_site(self):
        if self.imaging_mode == "multi-site":
            self.multi_well_row = 1
            self.multi_well_col = 1
            self.well_selection_list = ["All"]
            self.multi_well_detection = 'grid'
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
        if self.pipeline_selection == "motility":
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
            "wavelengths": ["All"],
            "cellpose_model": "20220830_all",
            "pipeline": "wormsize_intensity_cellpose",
        }

        if self.pipeline_selection == "cellprofile":
            self.cell_profile_dict.update({
                'run': True,
                'wavelengths': [self.wavelengths_cellprofile],
                'cellpose_model': self.cellpose_model_cellprofile,
                'pipeline': get_default_value(self.cellprofiler_pipeline_selection, "wormsize_intensity_cellpose"),
            })

    def prep_tracking_dict(self):
        self.tracking_dict = {
            "run": False,
            "diameter": 35,
            "minmass": 1200,
            "noisesize": 2,
            "searchrange": 45,
            "memory": 25,
            "adaptivestop": 30,
        }

        if self.pipeline_selection == "tracking":
            self.tracking_dict.update({
                'run': True,
                'diameter': get_default_value(self.tracking_diameter, 35),
                'minmass': get_default_value(self.tracking_minmass, 1200),
                'noisesize': get_default_value(self.tracking_noisesize, 2),
                'searchrange': get_default_value(self.tracking_searchrange, 45),
                'memory': get_default_value(self.tracking_memory, 25),
                'adaptivestop': get_default_value(self.tracking_adaptivestop, 30),
            })

    def prep_segmentation_dict(self):
        # Base dictionary with default values
        self.segmentation_dict = {
            "run": False,
            "model": "cellpose",
            "model_type": "20220830_all",
            "model_sigma": 0.25,
            "wavelengths": ["All"],
        }

        if self.pipeline_selection == "segmentation":
            update_dict = {
                'run': True,
                'model': self.cellpose_model_segmentation,
                'model_type': self.cellpose_model_type_segmentation,
                'wavelengths': [self.wavelengths_segmentation],
            }

            if self.cellpose_model_segmentation == "python":
                update_dict['model_sigma'] = get_default_value(self.python_model_sigma, 0.25)

            self.segmentation_dict.update(update_dict)

    def create_yaml_dict(self):
        yml = {
            "imaging_mode": [self.imaging_mode],
            'file_structure': [self.file_structure],
            'well-row': self.well_row,
            'well-col': self.well_col,
            'multi-well-row': self.multi_well_row,
            'multi-well-col': self.multi_well_col,
            'multi-well-detection': self.multi_well_detection,
            'x-sites': self.x_sites,
            'y-sites': self.y_sites,
            "stitch": self.stitch_switch,
            'circle_diameter': self.circle_diameter,
            'square_side': self.square_diameter,
            "pipelines": {
                "static_dx": self.static_dx_dict,
                "video_dx": self.video_dx_dict,
                "optical_flow": self.motility_run_dict,
                "segmentation": self.segmentation_dict,
                "cell-profile": self.cell_profile_dict,
                "tracking": self.tracking_dict
            },
            "wells": self.well_selection_list,
            "directories": {
                "work": [str(Path(self.mounted_volume, "work"))],
                "input": [str(Path(self.mounted_volume, 'input'))],
                "output": [str(Path(self.mounted_volume, 'output'))],
            }
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
        return {
            "motility": "motility",
            "segment": "binary",
            "blur": "blur",
            "edge": "edge",
            "raw": "raw",
        } if self.pipeline_selection == "motility" else {}

    def get_segmentation_image_diagnostic_parameters(self):
        return (
            {
                "binary": "binary",
                "blur": "blur",
                "edge": "edge",
                "raw": "raw",
            }
            if self.pipeline_selection == "segmentation"
            else {}
        )

    def get_tracking_image_diagnostic_parameters(self):
        return (
            {"tracks": "tracks", "raw": "raw"}
            if self.pipeline_selection == "tracking"
            else {}
        )

    def get_cell_profile_image_diagnostic_parameters(self):
        if self.pipeline_selection == "cellprofile":
            pipeline_mapping = {
                "wormsize_intensity_cellpose": {
                    "raw": "raw",
                    "straightened_worms": "straightened_worms",
                    "cp_masks": "cp_masks",
                },
                "mf_celltox": {
                    "raw": "raw",
                },
                "wormsize": {
                    "raw": "raw",
                    "straightened_worms": "straightened_worms",
                },
                "feeding": {
                    "straightened_worms": "straightened_worms",
                },
            }

            return pipeline_mapping.get(
                self.cellprofiler_pipeline_selection, {}
            )

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

    def get_image_diagnostic_parameters(self):
        motility_params = self.get_motility_image_diagnostic_parameters()
        segmentation_params = self.get_segmentation_image_diagnostic_parameters()
        tracking_params = self.get_tracking_image_diagnostic_parameters()
        cell_profile_params = self.get_cell_profile_image_diagnostic_parameters()

        # get the params that is not {}

        params = {
            **motility_params,
            **segmentation_params,
            **tracking_params,
            **cell_profile_params,
        }

        params = self.get_wavelengths_from_files(params)

        return {
            **params,
        }

    # In[7]: Preview Analysis

    def get_first_well(self):
        if self.well_selection_list == ["All"]:
            first_well = "A01"
        else:
            first_well = self.well_selection_list[0]

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

    def preview_analysis(self):
        if self.file_structure == "imagexpress":
            self.run_preview_analysis("imagexpress")
        elif self.file_structure == "avi":
            self.run_preview_analysis("avi")

    def run_preview_analysis(self, file_structure):
        # Check if the first well has already been run (implement this logic)
        if self.first_well_already_run():
            print(f"First well already processed for {file_structure}.")
            return

        # Prepare for preview analysis
        self.preamble_to_preview_analysis(file_structure)

        # Run the subprocess
        print("Running wrmXpress.")
        docker_output = ["Running wrmXpress."]

        try:
            process = subprocess.Popen(
                self.wrmxpress_preview_command_split,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            stdout, _ = process.communicate()

            if process.returncode != 0:
                print(f"Error occurred during wrmXpress execution: {stdout}")
            else:
                print("wrmXpress completed successfully.")
            docker_output.append(stdout)
        except Exception as e:
            print(f"Subprocess execution failed: {e}")
            docker_output.append(str(e))

    def preamble_to_preview_analysis(self, file_structure):
        self.prepare_preview_yaml()

        # Prepare paths
        image_directory = Path(self.mounted_volume, self.plate_name)
        input_directory = Path(self.mounted_volume, "input")
        platename_input_directory = Path(input_directory, self.plate_name)
        work_directory = Path(self.mounted_volume, "work", self.plate_name)
        output_directory = Path(self.mounted_volume, "output")

        # Clean and create directories
        clean_and_create_directories(
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

        # Copy files to input directory
        copy_files_to_input_directory(
            platename_input_dir=platename_input_directory,
            htd_file=htd_file,
            img_dir=image_directory,
            plate_base=plate_base,
            wells=self.get_first_well(),
            platename=self.plate_name,
        )

        # Prepare wrmXpress command
        self.prepare_preview_wrmxpress_command()

    def prepare_preview_wrmxpress_command(self):
        self.command_message = (
            f"```python wrmXpress/wrapper.py {self.plate_name}.yml {self.plate_name}```"
        )
        wrmxpress_preview_command = (
            f"python wrmXpress/wrapper.py {self.mounted_volume}/.{self.plate_name}.yml {self.plate_name}"
        )
        self.wrmxpress_preview_command_split = shlex.split(wrmxpress_preview_command)
        self.output_preview_log_file = Path(
            self.mounted_volume, "work", self.plate_name, f"{self.plate_name}_preview.log"
        )

    def first_well_already_run(self):
        # TODO: Implement logic to check if the first well has already been processed
        return False
