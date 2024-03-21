########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
from app.utils.callback_functions import motility_segment_fecundity_preview, cellprofile_wormsize_preview, cellprofile_wormsize_intensity_cellpose_preview, cellprofile_mf_celltox_preview, cellprofile_feeding_preview


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
        if motility_selection == 'True' or segment_selection == 'True' or fecundity_selection == 'True':
            return motility_segment_fecundity_preview(volume, 
                                               platename.
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
                return  cellprofile_wormsize_intensity_cellpose_preview(
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