import pytest
import pandas as pd
import numpy as np
from app.utils.callback_functions import create_df_from_inputs
from app.utils.wrmxpress_gui_obj import WrmXpressGui

def test_create_df_from_inputs():
    """Test that the create_df_from_inputs function creates a dataframe with the expected structure."""
    # Test with default values
    rows = 8
    cols = 12
    
    df = create_df_from_inputs(rows, cols)
    
    # Check dataframe shape
    assert df.shape == (rows, cols)
    
    # Check that column names contain 01-12 (zero-padded)
    assert list(df.columns) == [f"{i:02d}" for i in range(1, cols + 1)]
    
    # Check that row names are A-H
    assert list(df.index) == [chr(65 + i) for i in range(rows)]
    
    # Check that all values are well identifiers (e.g., "A01", "B12")
    for i, row in enumerate(df.index):
        for j, col in enumerate(df.columns):
            expected_value = f"{row}{col}"
            assert df.iloc[i, j] == expected_value

def test_create_df_custom_dimensions():
    """Test the dataframe creation with custom dimensions."""
    rows = 4
    cols = 6
    
    df = create_df_from_inputs(rows, cols)
    
    # Check dataframe shape
    assert df.shape == (rows, cols)
    
    # Check that column names contain 01-06 (zero-padded)
    assert list(df.columns) == [f"{i:02d}" for i in range(1, cols + 1)]
    
    # Check that row names are A-D
    assert list(df.index) == [chr(65 + i) for i in range(rows)]

def test_wrmxpress_gui_obj_initialization():
    """Test basic initialization of the WrmXpressGui class."""
    # Create an initialization with all required arguments
    gui_obj = WrmXpressGui(
        file_structure="tif",
        imaging_mode="single-well",
        multi_well_row=None,
        multi_well_col=None,
        multi_well_detection=None,
        x_sites=None,
        y_sites=None,
        stitch_switch=None,
        well_col=12,
        well_row=8,
        mask=None,
        mask_diameter=None,
        pipeline_selection=["motility"],
        wavelengths=None,
        pyrscale=None,
        levels=None,
        winsize=None,
        iterations=None,
        poly_n=None,
        poly_sigma=None,
        flags=None,
        cellpose_model_segmentation=None,
        type_segmentation=None,
        python_model_sigma=None,
        wavelengths_segmentation=None,
        cellprofiler_pipeline_selection=None,
        cellpose_model_cellprofiler=None,
        wavelengths_cellprofiler=None,
        wavelengths_tracking=None,
        tracking_diameter=None,
        tracking_minmass=None,
        tracking_noisesize=None,
        tracking_searchrange=None,
        tracking_memory=None,
        tracking_adaptivestop=None,
        static_dx=None,
        static_dx_rescale=None,
        video_dx=None,
        video_dx_format=None,
        video_dx_rescale=None,
        mounted_volume="/data",
        plate_name="test_plate",
        well_selection_list=["A01", "A02"]
    )
    
    # Check that basic attributes are set correctly
    assert gui_obj.file_structure == "tif"
    assert gui_obj.imaging_mode == "single-well"
    assert gui_obj.pipeline_selection == ["motility"]
    assert gui_obj.mounted_volume == "/data"
    assert gui_obj.plate_name == "test_plate"
    assert gui_obj.well_selection_list == ["A01", "A02"]
    
def test_wrmxpress_gui_obj_to_dict():
    """Test the to_dict method of WrmXpressGui."""
    # Create an initialization with all required arguments
    gui_obj = WrmXpressGui(
        file_structure="tif",
        imaging_mode="single-well",
        multi_well_row=None,
        multi_well_col=None,
        multi_well_detection=None,
        x_sites=None,
        y_sites=None,
        stitch_switch=None,
        well_col=12,
        well_row=8,
        mask=None,
        mask_diameter=None,
        pipeline_selection=["motility"],
        wavelengths=None,
        pyrscale=None,
        levels=None,
        winsize=None,
        iterations=None,
        poly_n=None,
        poly_sigma=None,
        flags=None,
        cellpose_model_segmentation=None,
        type_segmentation=None,
        python_model_sigma=None,
        wavelengths_segmentation=None,
        cellprofiler_pipeline_selection=None,
        cellpose_model_cellprofiler=None,
        wavelengths_cellprofiler=None,
        wavelengths_tracking=None,
        tracking_diameter=None,
        tracking_minmass=None,
        tracking_noisesize=None,
        tracking_searchrange=None,
        tracking_memory=None,
        tracking_adaptivestop=None,
        static_dx=None,
        static_dx_rescale=None,
        video_dx=None,
        video_dx_format=None,
        video_dx_rescale=None,
        mounted_volume="/data",
        plate_name="test_plate",
        well_selection_list=["A01", "A02"]
    )
    
    # Convert to dictionary
    gui_dict = gui_obj.to_dict()
    
    # Check that the dictionary contains the expected keys
    assert "file_structure" in gui_dict
    assert "imaging_mode" in gui_dict
    assert "pipeline_selection" in gui_dict
    assert "mounted_volume" in gui_dict
    assert "plate_name" in gui_dict
    assert "well_selection_list" in gui_dict
    
    # Check that values are preserved
    assert gui_dict["file_structure"] == "tif"
    assert gui_dict["imaging_mode"] == "single-well"
    assert gui_dict["pipeline_selection"] == ["motility"]
    assert gui_dict["mounted_volume"] == "/data"
    assert gui_dict["plate_name"] == "test_plate"
    assert gui_dict["well_selection_list"] == ["A01", "A02"]