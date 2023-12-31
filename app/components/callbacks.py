########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import os
import itertools

import dash
import docker
import numpy as np
import plotly.express as px
import yaml
from dash import dash_table
from dash.dependencies import Input, Output, State
from PIL import Image
from pathlib import Path

# Importing Components
from app.utils.create_df_from_user_input import create_df_from_inputs, create_empty_df_from_inputs
from app.utils.callback_functions import prep_yaml


def get_callbacks(app):
    # Create a callback to update the table based on user inputs
    @app.callback(
        [Output("table-container-batch", "children"),
         Output("table-container-species", "children"),
         Output("table-container-strains", "children"),
         Output("table-container-stages", "children"),
         Output("table-container-treatments", "children"),
         Output("table-container-conc", "children"),
         Output("table-container-other", "children"),
         Output("well-selection-table", 'children')
         ],
        [Input("total-num-rows", "value"),
         Input("total-well-cols", "value")]
    )
    def update_table(rows, cols):
        default_cols = 12
        default_rows = 8
        if rows is None:
            rows = default_rows
        if cols is None:
            cols = default_cols

        df = create_df_from_inputs(rows, cols)
        df_empty = create_empty_df_from_inputs(rows, cols)
        table_batch = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-batch'
        )
        table_species = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-species'
        )
        table_stages = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-stages'
        )
        table_strains = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-strains'
        )
        table_treatment = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-species'
        )
        table_conc = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-conc'
        )
        table_other = dash_table.DataTable(
            data=df_empty.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-other'
        )
        well_selection = dash_table.DataTable(
            data=df.reset_index().to_dict('records'),
            columns=[{'name': 'Row', 'id': 'index', 'editable': False}] +
            [{'name': col, 'id': col} for col in df.columns],
            editable=True,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            id='dynamic-table-container-well-selection-table'
        )
        return table_batch, table_species, table_strains, table_stages, table_treatment, table_conc, table_other, well_selection

    # Collapsing navbar
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # Appearing multi-well options
    @app.callback(
        [Output('multi-well-options-row', 'style'),
         Output('additional-options-row', 'style')],
        [Input('imaging-mode', 'value'),
         Input('file-structure', 'value')]
    )
    def update_options_visibility(imaging_mode, file_structure):
        multi_well_options_style = {'display': 'none'}
        additional_options_style = {'display': 'none'}

        if imaging_mode == 'multi-well':
            multi_well_options_style = {'display': 'flex'}

            if file_structure == 'avi':
                additional_options_style = {'display': 'flex'}

        return multi_well_options_style, additional_options_style

    # Populate list of wells to be analyzed

    @app.callback(
        Output('well-selection-list', 'children'),
        Input('dynamic-table-container-well-selection-table', 'data')
    )
    def update_wells(table_contents):
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
        sorted_list = sorted(filtered_list)

        return sorted_list

    

    # Write YAML from preview page
    @app.callback(
        Output("preview-page-status", "children"),
        Input("preview-button", "n_clicks"),
        State("imaging-mode", "value"),
        State("file-structure", "value"),
        State("multi-well-rows", "value"),
        State("multi-well-cols", "value"),
        State("multi-well-detection", "value"),
        State("species", "value"),
        State("stages", 'value'),
        State("motility-run", "value"),
        State("conversion-run", "value"),
        State("conversion-scale-video", "value"),
        State("conversion-rescale-multiplier", "value"),
        State("segment-run", "value"),
        State("segmentation-wavelength", 'value'),
        State("cell-profiler-run", "value"),
        State("cell-profiler-pipeline", "value"),
        State("diagnostics-dx", "value"),
        State("well-selection-list", "children"),
        State('mounted-volume', 'value'),
        State('plate-name', 'value')
    )
    def save_page_to_yaml(n_clicks, imagingmode, filestructure, multiwellrows, multiwellcols, multiwelldetection,
                          species, stages, motilityrun, conversionrun, conversionscalevideo,
                          conversionrescalemultiplier, segmentrun, wavelength, cellprofilerrun, cellprofilerpipeline,
                          diagnosticdx, wellselection, mountedvolume, platename
                          ):

        if n_clicks:
            yaml_dict = prep_yaml(imagingmode, filestructure, multiwellrows, multiwellcols, multiwelldetection,
                                  species, stages, motilityrun, conversionrun, conversionscalevideo,
                                  conversionrescalemultiplier, segmentrun, wavelength, cellprofilerrun,
                                  cellprofilerpipeline, diagnosticdx, wellselection)

            outpath = Path(mountedvolume, str(platename) + '.yml')

            with open(outpath, 'w') as yaml_file:
                yaml.dump(yaml_dict, yaml_file,
                          default_flow_style=False)

        return f"Configuration written to {outpath}"

    # Write YAML from save page
    @app.callback(
        Output("save-page-status", "children"),
        Input("save-page-button", "n_clicks"),
        State("imaging-mode", "value"),
        State("file-structure", "value"),
        State("multi-well-rows", "value"),
        State("multi-well-cols", "value"),
        State("multi-well-detection", "value"),
        State("species", "value"),
        State("stages", 'value'),
        State("motility-run", "value"),
        State("conversion-run", "value"),
        State("conversion-scale-video", "value"),
        State("conversion-rescale-multiplier", "value"),
        State("segment-run", "value"),
        State("segmentation-wavelength", 'value'),
        State("cell-profiler-run", "value"),
        State("cell-profiler-pipeline", "value"),
        State("diagnostics-dx", "value"),
        State("well-selection-list", "children"),
        State('mounted-volume', 'value'),
        State('plate-name', 'value')
    )
    def save_page_to_yaml(n_clicks, imagingmode, filestructure, multiwellrows, multiwellcols, multiwelldetection,
                          species, stages, motilityrun, conversionrun, conversionscalevideo,
                          conversionrescalemultiplier, segmentrun, wavelength, cellprofilerrun, cellprofilerpipeline,
                          diagnosticdx, wellselection, mountedvolume, platename
                          ):

        if n_clicks:
            yaml_dict = prep_yaml(imagingmode, filestructure, multiwellrows, multiwellcols, multiwelldetection,
                                  species, stages, motilityrun, conversionrun, conversionscalevideo,
                                  conversionrescalemultiplier, segmentrun, wavelength, cellprofilerrun,
                                  cellprofilerpipeline, diagnosticdx, wellselection)

            outpath = Path(mountedvolume, str(platename) + '.yml')

            with open(outpath, 'w') as yaml_file:
                yaml.dump(yaml_dict, yaml_file,
                          default_flow_style=False)

        return f"Configuration written to {outpath}"

    # Open and Close Info, Preview, and Save modals

    @app.callback(
        [Output("save-page-modal", "is_open"),
         Output("info-page-modal", "is_open"),
         Output("preview-page-modal", "is_open")],
        [Input("open-save-modal", "n_clicks"), Input("close-save-modal", "n_clicks"),
         Input("open-info-modal", "n_clicks"), Input("close-info-modal", "n_clicks"),
         Input("open-preview-modal", "n_clicks"), Input("close-preview-modal", "n_clicks")],
        [State("save-page-modal", "is_open"),
         State("info-page-modal", "is_open"),
         State("preview-page-modal", "is_open")],
    )
    def toggle_modals(open_save_clicks, close_save_clicks, open_info_clicks, close_info_clicks,
                      open_preview_clicks, close_preview_clicks, is_save_open, is_info_open, is_preview_open):
        ctx = dash.callback_context

        if ctx.triggered_id in ["open-save-modal", "close-save-modal"]:
            return not is_save_open, False, False
        elif ctx.triggered_id in ["open-info-modal", "close-info-modal"]:
            return False, not is_info_open, False
        elif ctx.triggered_id in ["open-preview-modal", "close-preview-modal"]:
            return False, False, not is_preview_open
        else:
            return is_save_open, is_info_open, is_preview_open
