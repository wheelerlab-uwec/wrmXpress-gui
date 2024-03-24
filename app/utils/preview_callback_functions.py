########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

from app.utils.callback_functions import motility_segment_fecundity_preview
from app.utils.callback_functions import cellprofile_wormsize_preview
from app.utils.callback_functions import cellprofile_wormsize_intensity_cellpose_preview
from app.utils.callback_functions import cellprofile_mf_celltox_preview
from app.utils.callback_functions import cellprofile_feeding_preview

########################################################################
####                                                                ####
####                          Functions                             ####
####                                                                ####
########################################################################

def preview_callback_functions(
    motility_selection, 
    segment_selection, 
    fecundity_selection, 
    selection, 
    cellprofiler, 
    cellprofilepipeline, 
    platename, 
    volume, 
    wells, 
    plate_base
):
        """
        This function is used to preview the analysis of the selected options.
        ======================================================================
        Arguments:
            - motility_selection : str : Motility selection
            - segment_selection : str : Segment selection
            - fecundity_selection : str : Fecundity selection
            - selection : str : Selection
            - cellprofiler : str : Cell profiler
            - cellprofilepipeline : str : Cell profile pipeline
            - platename : str : Plate name
            - volume : str : Volume
            - wells : str : Wells
            - plate_base : str : Plate base
        ======================================================================
        Returns:
            - function : function : Function to preview the analysis
                -- These functions are defined in app/utils/callback_functions.py
                -- and specified in what lines they are defined in the file
        ======================================================================

        """
        if motility_selection == 'True' or segment_selection == 'True' or fecundity_selection == 'True':
            return motility_segment_fecundity_preview(volume, 
                                               platename,
                                               wells,
                                               selection)
            
        elif cellprofiler == 'True':
            if cellprofilepipeline == 'wormsize':
                return cellprofile_wormsize_preview(
                    wells, 
                    volume,
                    platename,
                    plate_base,
                )
                        

            elif cellprofilepipeline == 'wormsize_intensity_cellpose':
                return cellprofile_wormsize_intensity_cellpose_preview(
                    wells, 
                    volume,
                    platename,
                    plate_base,
                )
                        
            elif cellprofilepipeline == 'mf_celltox':
                return cellprofile_mf_celltox_preview(
                    wells, 
                    volume,
                    platename,
                    plate_base,
                )
                    
            elif cellprofilepipeline == 'feeding':
                return cellprofile_feeding_preview(
                    wells, 
                    volume,
                    platename,
                    plate_base,
                )