########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yaml
from pathlib import Path
from app.utils.callback_functions import prep_yaml

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
save_page_content = dbc.ModalBody(
    [
        # Content for the Save Page Modal Body
        dcc.Markdown(
            "Write a YAML for running wrmXpress remotely. Include a full path and file name ending in `.yaml`."),
        dbc.Input(id="file-path-for-saved-yaml-file",
                  placeholder="Enter the full save path...", type="text"),
    ]
)

########################################################################
####                                                                ####
####                             Modal                              ####
####                                                                ####
########################################################################
save_page = dbc.Modal(
    [
        # Modal content header
        dbc.ModalHeader("Save Page"),
        # Modal page content as defined above
        save_page_content,
        # Modal page footer
        dbc.ModalFooter([
            # Buttons for the Save Page Modal
            dbc.Button("Save", id="save-page-button", className="ml-auto"),
            dbc.Button("Close", id="close-save-modal", className="ml-auto"),
        ]),
        html.Div(id="save-page-status")
    ],
    id="save-page-modal",
    size="l"
)

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################


def save_page_yaml(app):
    # Write YAML from save page
    @app.callback(
        Output("save-page-status", "children"),
        Input("save-page-button", "n_clicks"),
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
    def save_page_to_yaml(
            nclicks, imagingmode, filestructure, multiwellrows, multiwellcols, multiwelldetection, species, stages, motilityrun, conversionrun, conversionscalevideo, conversionrescalemultiplier, segmentrun, wavelength, cellprofilerrun, cellprofilerpipeline, diagnosticdx, platename, volume, wells):

        if nclicks:

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

           # Create the full filepath using os.path.join
            output_file = Path(volume, platename + '.yml')

            # Dump preview data to YAML file
            with open(output_file, 'w') as yaml_file:
                yaml.dump(config, yaml_file,
                          default_flow_style=False)
        return ""
