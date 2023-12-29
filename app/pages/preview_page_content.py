########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html
import yaml
from dash.dependencies import Input, Output, State
import os
import pathlib
import numpy as np
import plotly.express as px
from PIL import Image


########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
preview_page_content = dbc.ModalBody(
    [
        # Preview page contents
        html.Div([
            # button for loadining image
            dbc.Button('Load first input image',
                       id='submit-val', className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
            html.Br(),
            html.Br(),
            html.Div([
                dbc.Row([
                        dbc.Col([
                            html.P(id='input-path-output'),
                            "Input image: ",
                            # First image for selected well
                            dcc.Graph(
                                id='input-preview',
                                # style={'height':'30%', 'width':'30%'}
                            )
                        ]),
                        dbc.Col([
                            html.P(),
                            "Analysis preview: ",
                            # Second image of wrmXpress product after analysis of same well
                            dcc.Graph(
                                id='analysis-preview',
                                # style={'height':'30%', 'width':'30%'}
                            )
                        ])
                        ])
            ]
            )]),
        html.Br(),
        html.Div([
            dcc.Markdown("Write a YAML for running wrmXpress remotely. Include a full path and file name ending in `.yaml`."),
            dbc.Input(id="file-path-for-preview-yaml-file",
                      placeholder="Enter the full save path...", type="text"),
            html.Br(), 
        ])
    ],
)

########################################################################
####                                                                ####
####                             Modal                              ####
####                                                                ####
########################################################################
# Preview Page Modal
preview_page = dbc.Modal(
    [
        # Modal Header
        dbc.ModalHeader(
            "Preview Page"
        ),
        # Modal page contents from defined above
        preview_page_content,

        # Modal Footer
        dbc.ModalFooter([
            # Buttons for the Info Page Modal
            dbc.Button("Preview", id="preview-preview-button",
                       className="ml-auto", color="success"),
            dbc.Button("Close", id="close-preview-modal", className="ml-auto"),
        ]),
        html.Div(id="preview-page-status")  
    ],
    id="preview-page-modal",
    size="xl"
)

########################################################################
####                                                                ####
####                             Callbacks                          ####
####                                                                ####
########################################################################

def save_yaml_from_preview(app):
    # Write YAML from preview page
    @app.callback(
        Output("preview-page-status", "children"),
        [Input("preview-preview-button", "n_clicks")],
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
            State("file-path-for-preview-yaml-file", "value"),
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
        filepathforyamlfile,
    ):
        if n_clicks:
            well_list = [s.replace(", ", '') for s in wellselection]
            
            # Formatting YAML file with correct layout
            preview_input_yaml_file = {
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
                yaml.dump(preview_input_yaml_file, yaml_file,
                        default_flow_style=False)
            return f"Data Saved to {filepathforyamlfile}"
        return ""
    
def load_first_img(app):
    # Load first image in Preview page
    @app.callback(
        Output('input-path-output', 'children'),
        Output('input-preview', 'figure'),
        Input('submit-val', 'n_clicks'),
        State("input-directory", "value"),
        prevent_initial_call=True
    )
    def update_preview_image(n_clicks, input_dir_state):

        path_split = pathlib.PurePath(str(input_dir_state))
        dir_path = str(path_split.parts[-1])
        plate_base = dir_path.split("_", 1)[0]

        if n_clicks >= 1:
            # assumes IX-like file structure
            img_path = input_dir_state + f'/TimePoint_1/{plate_base}_A01.TIF'
            img = np.array(Image.open(img_path))
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            return f'Input path: {input_dir_state}', fig
        n_clicks = 0