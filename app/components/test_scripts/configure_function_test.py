########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.utils.styling import SIDEBAR_STYLE, CONTENT_STYLE
from app.components.header import header
from app.pages.configure import update_options_visibility, rows_cols, update_table, update_wells, run_analysis
from app.utils.callback_functions import prep_yaml
from app.utils.callback_functions import create_df_from_inputs
from app.utils.callback_functions import eval_bool

########################################################################
####                                                                ####
####                           Testing                              ####
####                                                                ####
########################################################################

def test_updated_visibility():
    """
    This function tests the update_options_visibility function.
    ===============================================================================
    Arguments:
        - None
    ===============================================================================
    Returns:
        - Assert : Asserts that the function works as expected
            +- True: The function works as expected
            +- False: The function does not work as expected
    """
    output1 = update_options_visibility('multi-well', 'imgexpress')
    assert output1 == {'display': 'flex'}, {'display': 'none'}

    output2 = update_options_visibility('single-well', 'imgexpress')
    assert output2 == {'display': 'none'}, {'display': 'none'}

    output3 = update_options_visibility('multi-well', 'avi')
    assert output3 == {'display': 'flex'}, {'display': 'flex'}

    output4 = update_options_visibility('single-well', 'avi')
    assert output4 == {'display': 'none'}, {'display': 'flex'}

def test_rows_cols():
    """
    This function tests the rows_cols function.
    ===============================================================================
    Arguments:
        - None
    ===============================================================================
    Returns:
        - Assert : Asserts that the function works as expected
            +- True: The function works as expected
            +- False: The function does not work as expected
    """
    
