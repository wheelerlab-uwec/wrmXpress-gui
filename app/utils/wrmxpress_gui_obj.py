import json

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

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())
