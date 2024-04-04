########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
import dash
from dash import callback, html
from dash.dependencies import Input, Output, State
from app.utils.callback_functions import create_df_from_inputs
from dash import dash_table
import itertools
import yaml
from pathlib import Path
from app.utils.callback_functions import prep_yaml
import os

# Importing Components and functions
from app.components.instrument_settings import instrument_settings
from app.components.worm_information import worm_information
from app.components.module_selection import module_selection
from app.components.run_time_settings import run_time_settings
from app.utils.callback_functions import eval_bool, create_figure_from_filepath, create_figure_from_url

# Registering this page
dash.register_page(__name__)

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

layout = dbc.Container([
    dbc.Accordion(
        [
            # Order of the Accordian item in which they appear in the app
            instrument_settings,  # Instrument settings, see instrument_settings.py
            worm_information,  # Worm information, see worm_information.py
            module_selection,  # Module selection, see module_selection.py
            run_time_settings,  # Run time settings, see run_time_settings.py
        ],
        start_collapsed=False,  # Start with the accordian open
        always_open=True,  # Always open the accordian
        id="configure-accordion",  # ID of the accordian
    ),
    html.Hr(),
    dbc.Alert(
        id='resolving-error-issue-configure',
        is_open=False,  # Alert is not open by default
        color='danger',  # Alert color is red
        duration=10000  # Alert will close after 10 seconds
    ),
    html.Br(),
    # Button to finalize configuration
    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Finalize configuration",  # Button text
                    id="finalize-configure-button",
                    className="flex",  # Button class is flex
                    color='primary'  # Default button color is (wrmXpress) blue
                ),
                width="auto"  # Button width is auto
            ),
        ],
        justify="center"  # Center the button
    ),
],
    # Adjust the white space between tab and accordian elements
    style={"paddingTop": "80px"}
)

########################################################################
####                                                                ####
####                              Callback                          ####
####                                                                ####
########################################################################

@callback(
    [
        Output('multi-well-options-row', 'style'),
        Output('additional-options-row', 'style')
    ],
    [
        Input('imaging-mode', 'value'),
        Input('file-structure', 'value')
    ]
)
# appearing selections upon meeting certain critera
def update_options_visibility(imaging_mode, file_structure):
    """
    This function will display the multi-well options and additional options based on the imaging mode and file structure selected.
    =======================================================================================================
    Arguments:
        - imaging_mode : str : The imaging mode selected
        - file_structure : str : The file structure selected
    =======================================================================================================
    Returns:
        - multi_well_options_style : dict : The style for the multi-well options
        - additional_options_style : dict : The style for the additional options
    """
    multi_well_options_style = {'display': 'none'}
    additional_options_style = {'display': 'none'}

    if imaging_mode == 'multi-well':  # if multi-well is selected
        # display the multi-well options
        multi_well_options_style = {'display': 'flex'}

        if file_structure == 'avi':  # if avi is selected
                # display the additional options
            additional_options_style = {'display': 'flex'}

    return multi_well_options_style, additional_options_style  # return the styles

@callback(
    # Storing values of inputs to be used in different pages
    Output("store", "data"),
    Input("total-well-cols", "value"),
    Input("total-num-rows", "value"),
    Input('mounted-volume', 'value'),
    Input('plate-name', 'value'),
    Input('well-selection-list', 'children'),
    Input('well-selection-list', 'children'),
    Input('imaging-mode', 'value'),
    Input("file-structure", 'value'),
    Input('pipeline-selection', 'value'),
    # Input("circ-or-square-img-masking", 'value'), # Image masking
)
def store_values(
    cols,
    rows,
    mounter,
    platename,
    well_selection,
    wells,
    imgaging_mode,
    file_sturcture,
    pipeline_selection,
    # img_masking, # Image masking
):
    """
    This function will store the values of the inputs to be used in different pages.
    =======================================================================================================
    Arguments:
        - cols : int : The number of columns
        - rows : int : The number of rows
        - mounter : str : The mounted volume
        - platename : str : The plate name
        - well_selection : list : The list of wells selected
        - wells : list : The list of wells
        - imgaging_mode : str : The imaging mode
        - file_sturcture : str : The file structure
        - pipeline_selection : str : The pipeline selection
    =======================================================================================================
    Returns:
        - dict : The values of the inputs to be used in different pages
    """
    # storing and returning the values of the inputs to be used in different pages
    return {
        'cols': cols,
        'rows': rows,
        'mount': mounter,
        'platename': platename,
        'wells': well_selection,
        'wells': wells,
        'img_mode': imgaging_mode,
        'file_structure': file_sturcture,
        'pipeline_selection': pipeline_selection,
        #'img_masking': img_masking, # Image masking
    }

@callback(
    Output("well-selection-table", 'children'),
    [
        Input("total-num-rows", "value"),
        Input("total-well-cols", "value")
    ]
)
# creating a selection table based on the dimensions of rows and columns selected
def update_table(rows, cols):
    """
    This function will create a selection table based on the dimensions of rows and columns selected.
    =======================================================================================================
    Arguments:
        - rows : int : The number of rows
        - cols : int : The number of columns
    =======================================================================================================
    Returns:
        - well_selection : dash_table.DataTable : The selection table
    """
    # default values for rows and columns
    default_cols = 12
    default_rows = 8
    if rows is None:  # if rows is not selected
        rows = default_rows
    if cols is None:  # if cols is not selected
        cols = default_cols

    # create a dataframe from the inputs, see callback_functions.py
    df = create_df_from_inputs(rows, cols)

    # create a table from the dataframe
    well_selection = dash_table.DataTable(
        data=df.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,  # table is editable
        style_table={'overflowX': 'auto'},  # table style
        style_cell={'textAlign': 'center'},  # cell style
        id='dynamic-table-container-well-selection-table'
    )
    return well_selection  # return the table

@callback(
    Output('well-selection-list', 'children'),
    Input('dynamic-table-container-well-selection-table', 'data')
)
def update_wells(table_contents):  # list of cells from selection table
    """
    This function will populate the list of wells to be analyzed.
    =======================================================================================================
    Arguments:
        - table_contents : list : The list of cells from the selection table
    =======================================================================================================
    Returns:
        - list : The sorted list of wells to be analyzed
    """
    values_list = [list(d.values()) for d in table_contents]
    flattened_list = list(itertools.chain.from_iterable(values_list))
    filtered_list = []
    for item in flattened_list:  # remove empty cells
        if item is None:
            continue
        elif len(item) == 1:  # remove single character cells
            continue
        else:
            filtered_list.append(item)  # append the item to the filtered list

    sorted_list = sorted(filtered_list)  # sort the list
    return sorted_list  # return the sorted list

@callback(
    [
        Output('finalize-configure-button', 'color'),
        Output("resolving-error-issue-configure", 'is_open'),
        Output('resolving-error-issue-configure', 'children'),
        Output("resolving-error-issue-configure", 'color'),
    ],
    Input('finalize-configure-button', 'n_clicks'),
    State('imaging-mode', 'value'),
    State('file-structure', 'value'),
    State('multi-well-rows', 'value'),
    State('multi-well-cols', 'value'),
    State('multi-well-detection', 'value'),
    State('species', 'value'),
    State('stages', 'value'),
    State('plate-name', 'value'),
    State('mounted-volume', 'value'),
    State('well-selection-list', 'children'),
    State('pipeline-selection', 'value'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def run_analysis(  # function to save the yaml file from the sections in the configuration page
    nclicks,
    imagingmode,
    filestructure,
    multiwellrows,
    multiwellcols,
    multiwelldetection,
    species,
    stages,
    platename,
    volume,
    wells,
    pipeline
):
    """
    This function will save the yaml file from the sections in the configuration page.
    =======================================================================================================
    Arguments:
        - nclicks : int : The number of clicks
        - imagingmode : str : The imaging mode
        - filestructure : str : The file structure
        - multiwellrows : int : The number of multi-well rows
        - multiwellcols : int : The number of multi-well columns
        - multiwelldetection : str : The multi-well detection
        - species : str : The species
        - stages : str : The stages
        - motilityrun : str : The motility run
        - conversionrun : str : The conversion run
        - conversionscalevideo : str : The conversion scale video
        - conversionrescalemultiplier : str : The conversion rescale multiplier
        - segmentrun : str : The segment run
        - wavelength : str : The wavelength
        - cellprofilerrun : str : The cell profiler run
        - cellprofilerpipeline : str : The cell profiler pipeline
        - diagnosticdx : str : The diagnostics dx
        - platename : str : The plate name
        - volume : str : The volume
        - wells : list : The list of wells
    =======================================================================================================
    Returns:
        - str : The color of the finalize configuration button
            +- 'primary' : The color of the initial configuration button
            +- 'danger' : The color of the configuration button upon encountering an error
            +- 'success' : The color of the finalize configuration button upon successful configuration
        - bool : The open state of the alert 
            +- False : The alert is not open
            +- True : The alert is open
        - str : The children of the alert
            +- str : The error message
            +- str : The success message
        - str : The color of the alert
            +- 'danger' : The color of the alert upon encountering an error
            +- 'success' : The color of the alert upon successful configuration

    """
    if nclicks:

        # try to catch any errors that may occur
        # return an error message if an error occurs
        try:
            # initializing the first error message
            error_messages = [
                "While finalizing the configuration, the following errors were found:"]
            error_occured = False  # initializing the error flag

            # checks volume and plate names to ensure they are adequately named
            check_cases = [None, '', ' ']

            # checks to ensure that plate name and volume contains characters
            if platename in check_cases:
                error_occured = True
                error_messages.append(
                    "Plate/Folder name is missing."  # error message
                )
            if volume in check_cases:
                error_occured = True
                error_messages.append(
                    "Volume path is missing."  # error message
                )

            # ensures that plate name and volume contains characters
            if volume not in check_cases and platename not in check_cases:

                # splits plate name into a list of characters
                platename_parts = list(platename)
                if len(platename_parts) > 0:

                    # ensures plate name does not contain spaces or slashes
                    has_invalid_chars = any(
                        letter == ' ' or letter == '/' for letter in platename_parts)
                    if has_invalid_chars == True:
                        error_occured = True
                        error_messages.append(
                            'Plate/Folder name contains invalid characters. A valid platename only contains letters, numbers, underscores ( _ ), and dashs ( - ).'
                        )

                # splits volume into a list of characters
                volume_parts = list(volume)
                if len(volume_parts) > 0:

                    # obtains last character of volume
                    volume_parts_end = volume_parts[-1]

                    # ensures last character of volume is not a forbidden character
                    if volume_parts_end in check_cases:
                        error_occured = True
                        error_messages.append(
                            'Volume path contains invalid characters. A valid path only contains letters, numbers, underscores ( _ ), dashes ( - ), and slashes ( / ).')

                    # ensures volume does not contain spaces
                    has_invalid_characters = any(
                        letter == ' ' for letter in volume_parts)
                    if has_invalid_characters == True:
                        error_occured = True
                        error_messages.append(
                            'Volume path contains invalid characters. A valid path only contains letters, numbers, underscores ( _ ), dashes ( - ), and slashes ( / ).')

                # check to see if volume, plate, and input directories exist
                # obtain and full plate name path
                platename_path = Path(volume, platename)
                plate_base = platename.split("_", 1)[0]

                # ensure all of these file paths exist (volume, input path, and plate name path)
                if not os.path.exists(volume):
                    error_occured = True
                    error_messages.append(
                        'The volume path does not exist.'
                    )

                # check to see if the plate name path exists
                if not os.path.exists(platename_path):
                    error_occured = True
                    error_messages.append(
                        "No Plate/Folder in the volume."
                    )

                # check to see if imagexpress mode is selected
                # if so, ensure that an .htd file exists
                if filestructure == 'imagexpress':
                    HTD_file = Path(platename_path, f'{plate_base}.HTD')
                    htd_file = Path(platename_path, f'{plate_base}.htd')
                    if not os.path.exists(htd_file) or not os.path.exists(HTD_file):
                        error_occured = True
                        error_messages.append(
                            'No .HTD file found in the Plate/Folder.'
                        )
                if filestructure == 'avi':
                    avi_folder_path = Path(volume, platename)
                    avi_pattern = f'{platename}_'
                    matched_files_avi = list(avi_folder_path.glob(avi_pattern + "*.avi"))
                    if not matched_files_avi:
                        error_occured = True
                        error_messages.append(
                            'No AVI files found in the Plate/Folder.'
                        )
                
                # check to see if avi mode is selected for fecundity, and any
                # of the cellprofiler modules, if it is thow an error
                if filestructure == 'avi' and pipeline in ['fecundity', 'wormsize_intensity_cellpose',
                                                           "mf_celltox", 'feeding', 'wormsize']:
                    error_occured = True
                    error_messages.append(
                        'AVI mode is not supported for the selected pipeline.'
                    )

                plate_base = platename.split("_", 1)[0]

                # Directory containing the TIFF files
                folder_path = Path(volume, f'{platename}/TimePoint_1')
                avi_folder_path = Path(volume, platename)
                # Iterate through the wells that have been selected
                for well in wells:
                    # Construct a pattern to match files for the current well, ignoring suffixes
                    pattern = f"{plate_base}_{well}"
                    avi_pattern = f'{platename}_{well}'
                    
                    # Find all files in the directory that match the well pattern
                    matched_files_TIF = list(folder_path.glob(pattern + "*.TIF"))
                    matched_files_tif = list(folder_path.glob(pattern + "*.tif"))
                    matched_files_avi = list(avi_folder_path.glob(avi_pattern + "*.avi"))
                    matched_files = matched_files_tif + matched_files_avi + matched_files_TIF
                    # If no files match the current well, set error flags
                    if not matched_files:
                        error_occured = True
                        error_messages.append(f'No images found for well {well}. This may result in unexpected errors or results.')
                if pipeline is None:
                    error_occured = True
                    error_messages.append(
                        'No pipeline selected.'
                    )
            # check to see if there was an error message
            if error_occured == True:

                # formats the first line of the error message
                error_messages[0] = html.H4(
                    f'{error_messages[0]}',
                    className='alert-heading'
                )

                # format the content of the error messages
                for i in range(1, len(error_messages)):
                    error_messages[i] = html.P(
                        f'{i}. {error_messages[i]}',
                        className="mb-0"
                    )

                # return the error messages
                return 'danger', True, error_messages, 'danger'

        # additional error messages that we have not accounted for
        except ValueError:
            return 'danger', True, 'A ValueError occurred', 'danger'
        except Exception as e:
            return 'danger', True, f'An unexpected error occurred: {str(e)}', 'danger'
        
        diagnosticdx = "True" # set diagnosticdx to True 

        # if no error messages are found, write the configuration to a YAML file
        config = prep_yaml(
            imagingmode,
            filestructure,
            multiwellrows,
            multiwellcols,
            multiwelldetection,
            species,
            stages,
            wells,
            volume,
            pipeline
        )

        output_file = Path(volume, platename + '.yml')

        # dump preview data to YAML file
        with open(output_file, 'w') as yaml_file:
            yaml.dump(config, yaml_file,
                      default_flow_style=False)

        # return success message
        return 'success', True, f'Configuration written to {output_file}', 'success'

@callback(
    Output('configure-input-preview', 'figure'),  # Targeting the figure of the non-working graph
    Output("configure-preview-dropdown", "options"),  # Targeting the dropdown options
    [Input('pipeline-selection', 'value')],  # Assuming this is how the user selects the pipeline
    Input("configure-preview-dropdown", 'value'),
    prevent_initial_call=True  # Preventing callback from running before any action is taken
)
def update_figure_based_on_selection(module_initial, image):
    """
    This function will load the image module for the selected pipeline.
    =======================================================================================================
    Arguments:
        - module : str : The selected module
        - store : dict : The stored values
    =======================================================================================================
    Returns:
        - fig : The image module for the selected pipeline
    """
    permalink_to_folder = "https://github.com/wheelerlab-uwec/wrmXpress-gui/tree/7007c5ced2b1c9d20a0e60ad1af606951ab1c3a2/assets/configure_assets"
    # obtain the volume and plate name from the stored values
    options = {
        'plate':'plate'
    }

    # identify which module is selected
    if module_initial == 'motility':
        options = {
            'plate':'plate',
            'binary':'binary',
            'blur':'blur',
            'edge':'edge',
            'motility':'motility'
        }
        if image not in options:
            image = 'plate'

        if image == 'plate':
            # obtain the motility image
            motility_img = "https://github.com/wheelerlab-uwec/wrmXpress-gui/blob/7007c5ced2b1c9d20a0e60ad1af606951ab1c3a2/assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01.png"
            # motility_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01.png"

            fig = create_figure_from_url(motility_img)
            return fig, options
        elif image == 'binary':
            # obtain the motility image
            binary_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01_binary.png"
            
            if os.path.exists(binary_img):
                # create figure from file path 
                fig = create_figure_from_filepath(binary_img)
                return fig, options
            
        elif image == 'blur':
            blur_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01_blur.png"

            if os.path.exists(blur_img):
                # create figure from file path 
                fig = create_figure_from_filepath(blur_img)
                return fig, options
            
        elif image == 'edge':
            edge_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01_edge.png"

            if os.path.exists(edge_img):
                # create figure from file path 
                fig = create_figure_from_filepath(edge_img)
                return fig, options
            
        elif image == 'motility':
            motility_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/motility/A01/img/20210819-p01-NJW_753_A01_motility.png"

            if os.path.exists(motility_img):
                # create figure from file path 
                fig = create_figure_from_filepath(motility_img,scale = 'inferno')
                return fig, options
        else:
            print('No motility image found')
    
    elif module_initial == 'fecundity':
        options = {
            'plate':'plate',
            'binary':'binary',
            'blur':'blur',
            'edge':'edge',
        }
        if image not in options:
            image = 'plate'

        if image == 'plate':
            # obtain the motility image
            fecundity_img ="/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/fecundity/A01/img/20210906-p01-NJW_857_A01.png"
            if os.path.exists(fecundity_img):
                # create figure from file path 
                fig = create_figure_from_filepath(fecundity_img)
                return fig, options
        elif image == 'binary':
            # obtain the motility image
            fecundity_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/fecundity/A01/img/20210906-p01-NJW_857_A01_binary.png"

            if os.path.exists(fecundity_img):
                # create figure from file path 
                fig = create_figure_from_filepath(fecundity_img)
                return fig, options
        elif image == 'blur':
            fecundity_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/fecundity/A01/img/20210906-p01-NJW_857_A01_blur.png"

            if os.path.exists(fecundity_img):
                # create figure from file path 
                fig = create_figure_from_filepath(fecundity_img)
                return fig, options
        elif image == 'edge':
            fecundity_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/fecundity/A01/img/20210906-p01-NJW_857_A01_edge.png"

            if os.path.exists(fecundity_img):
                fig = create_figure_from_filepath(fecundity_img)
                return fig, options
        else:
            print('No fecundity image found')
         
    elif module_initial == 'tracking':
        options = {
            'plate':'plate',
            'tracks':'tracks',
        }
        if image not in options:
            image = 'plate'
        
        if image == 'plate':
            tracking_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/tracking/A01/img/20240222-p01-RVH_A01.png"

            if os.path.exists(tracking_img):
                # create figure from file path 
                fig = create_figure_from_filepath(tracking_img)
                return fig, options
            
        elif image == 'tracks':
            # obtain the motility image
            tracking_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/tracking/A01/img/20240222-p01-RVH_A01_tracks.png"
            
            if os.path.exists(tracking_img):
                # create figure from file path 
                fig = create_figure_from_filepath(tracking_img)
                return fig, options
        else:
            print('No tracking image found')
    
    elif module_initial == 'wormsize_intensity_cellpose':
        options = {
            "plate": "plate",
            'straightened_worms': 'straightened_worms',
            'cp_masks': 'cp_masks'
        }
        if image not in options:
            image = 'plate'
        
        if image == 'plate':
            # obtain the motility image
            wrmsize_inten_cellpose = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/wormsize_intensity_cellpose/A01/img/20220408-p01-MGC_1351_A01.png"

            if os.path.exists(wrmsize_inten_cellpose):
                # create figure from file path 
                fig = create_figure_from_filepath(wrmsize_inten_cellpose)
                return fig, options
        elif image == 'straightened_worms':
            straightend_worm = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/wormsize_intensity_cellpose/A01/img/20220408-p01-MGC_A01.tiff"

            if os.path.exists(straightend_worm):
                # create figure from file path 
                fig = create_figure_from_filepath(straightend_worm)
                return fig, options
        elif image == 'cp_masks':
            cp_masks = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/wormsize_intensity_cellpose/A01/img/20220408-p01-MGC_A01_cp_masks.png"

            if os.path.exists(cp_masks):
                # create figure from file path 
                fig = create_figure_from_filepath(cp_masks)
                return fig, options
        else:
            print('No wormsize_intensity_cellpose image found')
    
    elif module_initial == 'mf_celltox':
        options = {
            "plate": "plate",
            "straightened_worms": "straightened_worms"
        }
        if image not in options:
            image = 'plate'
        
        if image == 'plate':
            plate_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/mf_celltox/A01/img/20210917-p15-NJW_913_A01.png"

            if os.path.exists(plate_img):
                # create figure from file path 
                fig = create_figure_from_filepath(plate_img)
                return fig, options
        elif image == 'straightened_worms':
            # obtain the motility image
            mf_celltox_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/mf_celltox/A01/img/20210917-p15-NJW_913_A01.TIF"
            if os.path.exists(mf_celltox_img):
                # create figure from file path 
                fig = create_figure_from_filepath(mf_celltox_img)
                return fig, options
        else:
            print('No mf_celltox image found')
    
    elif module_initial == 'feeding':
        options = {
            "plate": "plate",
            'w1': 'w1',
            'w2': 'w2',
            'w3': 'w3',
        }
        if image not in options:
            image = 'plate'
        
        if image == 'plate':

            # obtain the motility image
            feeding_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/feeding/A01/img/20210823-p01-KJG-A01.tiff"
            if os.path.exists(feeding_img):
                # create figure from file path 
                fig = create_figure_from_filepath(feeding_img)
                return fig, options
        elif image == 'w1':
            w1_path = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/feeding/A01/img/20210823-p01-KJG_795_A01_w1.png"
            if os.path.exists(w1_path):
                # create figure from file path 
                fig = create_figure_from_filepath(w1_path)
                return fig, options
        elif image == 'w2':
            w2_path = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/feeding/A01/img/20210823-p01-KJG_795_A01_w2.png"
            if os.path.exists(w2_path):
                # create figure from file path 
                fig = create_figure_from_filepath(w2_path)
                return fig, options
        elif image == 'w3':
            w3_path = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/feeding/A01/img/20210823-p01-KJG_795_A01_w3.png"
            if os.path.exists(w3_path):
                # create figure from file path 
                fig = create_figure_from_filepath(w3_path)
                return fig, options
        else:
            print('No feeding image found')
    
    elif module_initial == 'wormsize':
        options = {
            "plate": "plate",
            'straightened_worms': 'straightened_worms',
        }
        if image not in options:
            image = 'plate'

        if image == 'plate':
            plate_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/wormsize/A01/img/20220408-p01-MGC_1351_A01.png"
            if os.path.exists(plate_img):
                # create figure from file path 
                fig = create_figure_from_filepath(plate_img)
                return fig, options
        elif image == 'straightened_worms':    
            # obtain the motility image
            wrmsize_img = "/Users/zc/Library/CloudStorage/OneDrive-UW-EauClaire/Academics/Wheeler_Lab/wrmXpress-gui/assets/configure_assets/wormsize/A01/img/20220408-p01-MGC_A01.tiff"
            if os.path.exists(wrmsize_img):
                # create figure from file path 
                fig = create_figure_from_filepath(wrmsize_img)
                return fig, options
        else:
            print('No wormsize image found')
    
