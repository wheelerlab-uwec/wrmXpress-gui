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
import time

# Importing Components
from app.components.instrument_settings import instrument_settings
from app.components.worm_information import worm_information
from app.components.module_selection import module_selection
from app.components.run_time_settings import run_time_settings
from app.utils.callback_functions import eval_bool

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
            instrument_settings,
            worm_information,
            module_selection,
            run_time_settings,
        ],
        start_collapsed=False,
        always_open=True,
    ),
    html.Hr(),
    dbc.Alert(id='resolving-error-issue-configure',
              is_open=False, color='danger', duration=10000),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Finalize Configure",
                    id="finalize-configure-button",
                    className="flex",
                    color='info'
                ),
                width="auto"
            ),
        ],
        justify="center"
    ),
],
    style={"paddingTop": "80px"})  # Adjust the white space between tab and accordian elements

########################################################################
####                                                                ####
####                              Callback                          ####
####                                                                ####
########################################################################


@callback(
    [Output('multi-well-options-row', 'style'),
     Output('additional-options-row', 'style')],
    [Input('imaging-mode', 'value'),
     Input('file-structure', 'value')]
)
# appearing selections upon meeting certain critera
def update_options_visibility(imaging_mode, file_structure):
    multi_well_options_style = {'display': 'none'}
    additional_options_style = {'display': 'none'}

    if imaging_mode == 'multi-well':
        multi_well_options_style = {'display': 'flex'}

        if file_structure == 'avi':
            additional_options_style = {'display': 'flex'}

    return multi_well_options_style, additional_options_style


@callback(  # Storing values of inputs to be used in different pages
    Output("store", "data"),
    Input("total-well-cols", "value"),
    Input("total-num-rows", "value"),
    Input('mounted-volume', 'value'),
    Input('plate-name', 'value'),
    Input('well-selection-list', 'children'),
    Input('motility-run', 'value'),
    Input('segment-run', 'value'),
    Input('well-selection-list', 'children'),
    Input('imaging-mode', 'value'),
    Input("file-structure", 'value'),
    Input("circ-or-square-img-masking", 'value')
)
def rows_cols(cols,
              rows,
              mounter,
              platename,
              well_selection,
              motility,
              segment,
              wells,
              imgaging_mode,
              file_sturcture,
              img_masking
              ):
    return {'cols': cols,
            'rows': rows,
            'mount': mounter,
            'platename': platename,
            'wells': well_selection,
            'motility': motility,
            'segment': segment,
            'wells': wells,
            'img_mode': imgaging_mode,
            'file_structure': file_sturcture,
            'img_masking': img_masking
            }


@callback(
    Output("well-selection-table", 'children'),
    [Input("total-num-rows", "value"),
     Input("total-well-cols", "value")]
)
# creating a selection table based on the dimensions of rows and columns selected
def update_table(rows, cols):
    default_cols = 12
    default_rows = 8
    if rows is None:
        rows = default_rows
    if cols is None:
        cols = default_cols

    df = create_df_from_inputs(rows, cols)
    well_selection = dash_table.DataTable(
        data=df.reset_index().to_dict('records'),
        columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
        [{'name': col, 'id': col} for col in df.columns],
        editable=True,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        id='dynamic-table-container-well-selection-table'
    )
    return well_selection

# Populate list of wells to be analyzed


@callback(
    Output('well-selection-list', 'children'),
    Input('dynamic-table-container-well-selection-table', 'data')
)
def update_wells(table_contents):  # list of cells from selection table
    values_list = [list(d.values()) for d in table_contents]
    flattened_list = list(itertools.chain.from_iterable(values_list))
    filtered_list = []
    for item in flattened_list:
        if item is None:
            continue
        elif len(item) == 1:
            continue
        else:
            filtered_list.append(item)
    # filtered_list = [item for item in flattened_list if item is None or len(item) > 1]
    sorted_list = sorted(filtered_list)

    return sorted_list


@callback(
    [Output('finalize-configure-button', 'color'),
     Output("resolving-error-issue-configure", 'is_open'),
     Output('resolving-error-issue-configure', 'children'),
     Output("resolving-error-issue-configure", 'color'),],
    Input('finalize-configure-button', 'n_clicks'),
    State('imaging-mode', 'value'),
    State('file-structure', 'value'),
    State('multi-well-rows', 'value'),
    State('multi-well-cols', 'value'),
    State('multi-well-detection', 'value'),
    State('species', 'value'),
    State('stages', 'value'),
    State('motility-run', 'value'),
    State('conversion-run', 'value'),
    State('conversion-scale-video', 'value'),
    State('conversion-rescale-multiplier', 'value'),
    State('segment-run', 'value'),
    State('segmentation-wavelength', 'value'),
    State('cell-profiler-run', 'value'),
    State('cell-profiler-pipeline', 'value'),
    State('diagnostics-dx', 'value'),
    State('plate-name', 'value'),
    State('mounted-volume', 'value'),
    State('well-selection-list', 'children'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def run_analysis(
    nclicks,
    imagingmode,
    filestructure,
    multiwellrows,
    multiwellcols,
    multiwelldetection,
    species,
    stages,
    motilityrun,
    conversionrun,
    conversionscalevideo,
    conversionrescalemultiplier,
    segmentrun,
    wavelength,
    cellprofilerrun,
    cellprofilerpipeline,
    diagnosticdx,
    platename,
    volume,
    wells,
):
    if nclicks:

        try:
            # initializing the first error message
            error_messages = [
                "While finalizing the configuration, the following errors were found:"]
            error_occured = False

            # checks volume and plate names to ensure they are adequately named
            check_cases = [None, '', ' ']

            # checks to ensure that plate name and volume contains characters
            if platename in check_cases:
                error_occured = True
                error_messages.append(
                    "Plate/Folder name is missing.")
            if volume in check_cases:
                error_occured = True
                error_messages.append(
                    "Volume path is missing.")

            # ensures that plate name and volume contains characters
            if volume not in check_cases and platename not in check_cases:

                # splits plate name into a list of characters
                platename_parts = list(platename)
                if len(platename_parts) > 0:

                    # obtains the first and last character of plate name
                    platename_parts_start = platename_parts[0]
                    platename_parts_end = platename_parts[-1]
                    plate_name_end_checks = [None, '', ' ', '/']

                    # ensures plate name does not contain spaces or slashes
                    has_invalid_chars = any(
                        letter == ' ' or letter == '/' for letter in platename_parts)
                    if has_invalid_chars == True:
                        error_occured = True
                        error_messages.append(
                            'Plate/Folder name contains invalid characters. A valid platename only contains letters, numbers, underscores ( _ ), and dashs ( - ).')

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

                # obtain input path and full plate name path
                input_path = Path(volume, 'input')
                platename_path = Path(volume, "input", platename)

                # ensure all of these file paths exist (volume, input path, and plate name path)
                if not os.path.exists(volume):
                    error_occured = True
                    error_messages.append(
                        'The volume path does not exist.')
                if not os.path.exists(input_path):
                    error_occured = True
                    error_messages.append(
                        "No 'input/' directory in the volume.")
                if not os.path.exists(platename_path):
                    error_occured = True
                    error_messages.append(
                        "No Plate/Folder in the 'input/' of the volume.")

                # check to see if the wells selected exist
                plate_base = platename.split("_", 1)[0]
                well_fail = False
                index = 0

                while not well_fail and index < len(wells):
                    well = wells[index]
                    img_path = Path(
                        volume, 'input', f'{platename}/TimePoint_1/{plate_base}_{well}.TIF')
                    if not os.path.exists(img_path):
                        error_occured = True
                        error_messages.append(
                            'You have selected more wells than you have images. This may result in unexpected errors or results.')
                        well_fail = True
                    index += 1

                # check if video module is selected with only one time point
                if eval_bool(cellprofilerrun) == True:
                    timept = Path(volume, 'input',
                                  f'{platename}/TimePoint_2')
                    if os.path.exists(timept):
                        error_occured = True
                        error_messages.append(
                            'You have selected a Cell Profiler pipeline while having multiple time points.')

            # check for conflicting modules
            if eval_bool(cellprofilerrun) == True and eval_bool(segmentrun):
                error_occured = True
                error_messages.append(
                    'Cannot run Cellprofiler and Segment together.')

            if eval_bool(cellprofilerrun) == True and eval_bool(motilityrun):
                error_occured = True
                error_messages.append(
                    'Cannot run Cellprofiler and Motility together.')

            # check to see if there was an error message
            if error_occured == True:

                # formats the first line of the error message
                error_messages[0] = html.H4(
                    f'{error_messages[0]}', className='alert-heading')

                # format the content of the error messages
                for i in range(1, len(error_messages)):
                    error_messages[i] = html.P(
                        f'{i}. {error_messages[i]}', className="mb-0")

                return 'danger', True, error_messages, 'danger'

        # additional error messages that we have not accounted for
        except ValueError:
            return 'danger', True, 'A ValueError occurred', 'danger'
        except Exception as e:
            return 'danger', True, f'An unexpected error occurred: {str(e)}', 'danger'
        config = prep_yaml(
            imagingmode,
            filestructure,
            multiwellrows,
            multiwellcols,
            multiwelldetection,
            species,
            stages,
            motilityrun,
            conversionrun,
            conversionscalevideo,
            conversionrescalemultiplier,
            segmentrun,
            wavelength,
            cellprofilerrun,
            cellprofilerpipeline,
            diagnosticdx,
            wells
        )

        output_file = Path(volume, platename + '.yml')

        # dump preview data to YAML file
        with open(output_file, 'w') as yaml_file:
            yaml.dump(config, yaml_file,
                      default_flow_style=False)
        return 'success', True, f'Configuration written to {output_file}', 'success'
