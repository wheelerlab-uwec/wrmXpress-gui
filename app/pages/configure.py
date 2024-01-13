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
import docker
import yaml
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
from app.utils.callback_functions import prep_yaml
import os

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
    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Finalize Configure",
                    id="finalize-configure-button",
                    className="flex",
                    color='success'
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
    Input('well-selection-list', 'children')
)
def rows_cols(cols, rows, mounter, platename, well_selection, motility, segment, wells):
    return {'cols': cols,
            'rows': rows,
            'mount': mounter,
            'platename': platename,
            'wells': well_selection,
            'motility': motility,
            'segment': segment,
            'wells': wells
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
     Output("error-modal", 'is_open'),
     Output('error-modal-content', 'children'),
     Output('resolving-error-issue', 'children')],
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
    prevent_initial_call=True
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

            """
            Checking volume and plate names to ensure they are adequately named
            """
            check_cases = [None, '', '/']
            if platename in check_cases or volume in check_cases:
                return 'success', True, 'There is an inadequate Volume or Plate name', 'Please adequately name the Volume and Plate name'

            platename_parts = list(platename)
            if len(platename_parts) > 0:
                platename_parts_start = platename_parts[0]
                platename_parts_end = platename_parts[-1]
                if platename_parts_start in check_cases or platename_parts_end in check_cases:
                    return 'success', True, f'{platename} is an inadequate plate name', 'Please adequately name the plate'
            
            volume_parts=list(volume)
            if len(volume_parts)>0:
                volume_parts = volume_parts[-1]
                if volume_parts in check_cases:
                    return "success", True, f'{volume} is an inadequate volume name', 'Please adequately name the volume'
                
            """
            Checking to see if volume and plate names exist
            """
            platename_path = Path(volume, "input", platename)
            if not os.path.exists(volume):
                return 'success', True, f'The directory {volume} does not exist', 'Please choose the accurate volume'
            if not os.path.exists(platename_path):
                return 'success', True, f'The directory {platename} does not exist', 'Please choose the accurate platename'
            
            '''
            Checking to see if the wells selected exist
            '''
            plate_base = platename.split("_", 1)[0]
            for well in wells:
                img_path = Path(volume, 'input', f'{platename}/TimePoint_1/{plate_base}_{well}.TIF')
                if not os.path.exists(img_path):
                    return 'success', True, f'the selected well {well} does not exist', 'Please ensure you select onley the wells which you wish to analyze'

            """
            Checking if video module is selected with only one time point
            """
            if eval_bool(cellprofilerrun)==True:
                for i in range(2,3):
                    timept = Path(volume, 'input', f'{platename}/TimePoint_{i}')
                    if not os.path.exists(timept):
                        return 'success', True, "cannot select cell prolfiler with one time point", 'please ensure accurate selections'

            """
            Checking for conflicting modules
            """
            if eval_bool(cellprofilerrun) ==True and eval_bool(segmentrun):
                return 'success', True, f'Conflicting selections of Cell Profile Run: {cellprofilerrun} and Segment Run: {segmentrun}', 'please ensure accurate selections'
  
            if eval_bool(cellprofilerrun) ==True and eval_bool(motilityrun):
                return 'success', True, f'Conflicting selections of Cell Profile Run: {cellprofilerrun} and Segment Run: {motilityrun}', 'please ensure accurate selections'
  

        except ValueError:
            return 'success', True, 'A ValueError occurred', ''
        except Exception as e:
            return 'success', True, f'An unexpected error occurred: {str(e)}', ''
        
        if wells == 'All':
            first_well = 'A01'
        else:
            first_well = wells[0]

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

        # Dump preview data to YAML file
        with open(output_file, 'w') as yaml_file:
            yaml.dump(config, yaml_file,
                      default_flow_style=False)

        return 'success', False, None, None
