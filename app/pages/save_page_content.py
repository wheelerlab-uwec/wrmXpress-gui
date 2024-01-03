########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yaml
import os

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
        [Input("save-page-button", "n_clicks")],
        [
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
            State("work-directory", "value"),
            State("input-directory", "value"),
            State("output-directory", "value"),
            State("file-path-for-saved-yaml-file", "value")
        ]
    )
    def save_page_to_yaml(
        n_clicks,
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
        wellselection,
        workdirectory,
        inputdirectory,
        outputdirectory,
        filepathforyamlfile
    ):
        if n_clicks:
            well_list = [s.replace(", ", '') for s in wellselection]

            # Formatting YAML file with correct layout
            user_input_yaml_file = {
                "imaging_mode": [imagingmode],
                "file_structure": [filestructure],
                "multi-well-rows": multiwellrows,
                "multi-well-cols": multiwellcols,
                "multi-well-detection": [multiwelldetection],
                "species": [species],
                "stages": [stages],
                "modules": {
                    "motility": {"run": bool(motilityrun)},
                    "convert": {
                        "run": bool(conversionrun),
                        "save_video": bool(conversionscalevideo),
                        "rescale_multiplier": conversionrescalemultiplier
                    },
                    "segment": {
                        "run": bool(segmentrun),
                        "wavelength": [wavelength]
                    },
                    "cellprofiler": {
                        "run": bool(cellprofilerrun),
                        "pipeline": [cellprofilerpipeline]
                    },
                    "dx": {
                        "run": bool(diagnosticdx)
                    }
                },
                "wells": well_list,
                "directories": {
                    "work": [workdirectory],
                    "input": [inputdirectory],
                    "output": [outputdirectory]
                }
            }
            # Create the full filepath using os.path.join
            output_file = os.path.join(filepathforyamlfile)

            # Dump preview data to YAML file
            with open(output_file, 'w') as yaml_file:
                yaml.dump(user_input_yaml_file, yaml_file,
                          default_flow_style=False)
            return f"Data Saved to {filepathforyamlfile}"
        return ""
