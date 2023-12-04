import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import yaml
import plotly.graph_objs as go
import os
import pathlib
import base64

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

user_input_yaml_file = {}
preview_input_yaml_file = {}

def create_imaging_settings():
    return dbc.AccordionItem(
                [
                    html.H6("Imaging Mode:"),
                    dbc.RadioItems(
                        id="imaging-mode",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Single Well", "value": "single-well"},
                            {"label": "Multi Well", "value": "multi-well"},
                        ],
                        value="single-well",
                    ),
                    html.H6("File Structure:"),
                    dbc.RadioItems(
                        id="file-structure",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Image Express", "value": "imagexpress"},
                            {"label": "AVI", "value": "avi"},
                        ],
                        value="imagexpress",
                    ),
                    html.H6("Multi Well Rows"),
                    dbc.Input(id="multi-well-rows", placeholder="Please insert the multi well rows.", type="number"),
                    html.H6("Multi Well Columns"),
                    dbc.Input(id="multi-well-cols", placeholder="Please insert the multi well columns.", type="number"),
                    html.H6("Multi Well Detection:"),
                    dbc.RadioItems(
                        id="multi-well-detection",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Auto", "value": "auto"},
                            {"label": "Grid", "value": "grid"},
                        ],
                        value="auto",
                    ),
                ],
                id="instrument-settings-file-structure",
                title="Instrument Settings"
            )
def create_worm_information():
    return dbc.AccordionItem(
                [
                    html.H6("Species:"),
                    dbc.RadioItems(
                        id="species",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Bma", "value": "Bma"},
                            {"label": "Cel", "value": "Cel"},
                            {"label": "Sma", "value": "Sma"}
                        ],
                        value="Bma",
                    ),
                    html.H6("Stages:"),
                    dbc.RadioItems(
                        id="stages",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Mf", "value": "Mf"},
                            {"label": "Adult", "value": "Adult"},
                            {"label": "Mixed", "value": "Mixed"},                            
                        ],
                        value="Mf",
                    ),
                ],
                id="worm-information",
                title="Worm Information"
            )
def create_module_selection():
    return dbc.AccordionItem(
                [
                    html.H4("Motility"),
                    html.H6("Motility Run"),
                    dbc.RadioItems(
                        id="motility-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="True",
                    ),
                    html.H4("Conversion"),
                    html.H6("Conversion Run"),
                    dbc.RadioItems(
                        id="conversion-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="False",
                    ),
                    html.H6("Conversion Scale Video"),
                    dbc.RadioItems(
                        id="conversion-scale-video",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="False",
                    ),
                    html.H6("Conversion Rescale Multiplier"),
                    dbc.Input(id="conversion-rescale-multiplier", placeholder="Please insert the rescale multiplier:", type="number"),
                    html.H4("Segmentation"),
                    html.H6("Segment Run"),
                    dbc.RadioItems(
                        id="segment-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="True",
                    ),
                    html.H6("Wavelength"),
                    dbc.Input(id="segmentation-wavelength", placeholder="Please insert the segmentation wavelength (please seperate multiple values by a comma):", type="text"),
                    html.H4("Cell Profilier"),
                    html.H6("Cell Profilier Run"),
                    dbc.RadioItems(
                        id="cell-profilier-run",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="False",
                    ),
                    html.H6("Cell Profilier Pipeline"),
                    dbc.RadioItems(
                        id="cell-profilier-pipeline",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Worm Size, Intensity, Cell Pose", "value": "wormsize_intensity_cellpose"},
                            {"label": "Mf Celltox", "value": "mf_celltox"},
                            {"label": "Wormsize", "value":"wormsize"},
                            {"label":"Wormsize Trans","value":"wormsize_trans"}
                        ],
                        value="wormsize_intensity_cellpose",
                    ),
                    html.H4("Diagnostics"),
                    html.H6("dx"),
                    dbc.RadioItems(
                        id="diagnostics-dx",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "True", "value": "True"},
                            {"label": "False", "value": "False"}
                        ],
                        value="True",
                    ),
                ],
                id="module-selection",
                title="Module Selection"
            )
def create_run_time_settings():
    return dbc.AccordionItem([
                html.H6("Wells"),
                dbc.Input(id="wells-information", placeholder="Please insert the wells information (please seperate multiple values by a comma):", type="text"),
                html.H4("Directories"),
                html.H6("Work"),
                dbc.Input(id="work-directory", placeholder="Please insert the work directory:", type="text"),
                html.H6("Input"),
                dbc.Input(id="input-directory", placeholder="Please insert the input directory:", type="text"),
                html.H6("Output"),
                dbc.Input(id="output-directory", placeholder="Please insert the output directory:", type="text"),
            ],
                id="run-time-settings",
                title="Run-Time Settings"
            )
def save_page_content():
    return dbc.ModalBody(
        [
            # Content for the Save Page Modal
            html.H6("Save Page Content"),
            dbc.Input(id= "file-path-for-saved-yaml-file", placeholder="Please enter the full filepath for your yaml file:", type="text"),
                            ]
    )

# Create the Save Page Modal
save_page = dbc.Modal(
    [
        dbc.ModalHeader("Save Page"),
        save_page_content(),
        dbc.ModalFooter([
            # Buttons for the Save Page Modal
            dbc.Button("Save", id="save-page-button", className="ml-auto"),
            dbc.Button("Close", id="close-save-modal", className="ml-auto"),
        ]),
        html.Div(id="save-page-status")  # Placeholder for saving status
    ],
    id="save-page-modal",
    size="xl"
)

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            dbc.Nav(
                [
                    dbc.NavItem(dbc.Button("Save Page", id="open-save-modal", color="primary")),
                ],
                className="ml-auto",  # Set the left margin to auto
            ),
            fluid=True,
        ),
        color="light",
        dark=False,
        sticky="top",
    ),
    dbc.Container([
        dbc.Accordion(
            [
                create_imaging_settings(),
                create_worm_information(),
                create_module_selection(),
                create_run_time_settings(),
            ],
            start_collapsed=False,
            always_open=True,
        ),
    ]),
    save_page,
])

@app.callback(
        Output("save-page-status", "children"),
        [Input("save-page-button", "n_clicks")],
        [
            State("imaging-mode", "value"),
            State("file-structure", "value"),
            State("multi-well-rows", "value"),
            State("multi-well-cols", "value"),
            State("multi-well-detection","value"),
            State("species","value"),
            State("stages", 'value'),
            State("motility-run","value"),
            State("conversion-run","value"),
            State("conversion-scale-video","value"),
            State("conversion-rescale-multiplier","value"),
            State("segment-run","value"),
            State("segmentation-wavelength",'value'),
            State("cell-profilier-run","value"),
            State("cell-profilier-pipeline","value"),
            State("diagnostics-dx","value"),
            State("wells-information", "value"),
            State("work-directory","value"),
            State("input-directory", "value"),
            State("output-directory","value"),
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
    cellprofilierrun,
    cellprofilierpipeline,
    diagnosticdx,
    wellsinformation,
    workdirectory,
    inputdirectory,
    outputdirectory,
    filepathforyamlfile
):
    if n_clicks:
        user_input_yaml_file = {
            "imaging_mode": [imagingmode],
            "file_structure": [filestructure],
            "multi-well-rows": multiwellrows,
            "multi-well-cols": multiwellcols,
            "multi-well-detection": [multiwelldetection],
            "species": [species],
            "stages": [stages],
            "modules": {
                "motility": {"run": motilityrun},
                "convert": {
                    "run": conversionrun,
                    "save_video": conversionscalevideo,
                    "rescale_multiplier": conversionrescalemultiplier
                },
                "segment": {
                    "run": segmentrun,
                    "wavelength": [wavelength]
                },
                "cellprofilier": {
                    "run": cellprofilierrun,
                    "pipeline": [cellprofilierpipeline]
                },
                "dx": {
                    "run": diagnosticdx
                }
            },
            "wells": [wellsinformation],
            "directories": {
                "work": [workdirectory],
                "input": [inputdirectory],
                "output": [outputdirectory]
            }
        }
        # Create the full filepath using os.path.join
        output_file = os.path.join(filepathforyamlfile + ".yaml")

        # Dump preview data to YAML file
        with open(output_file, 'w') as yaml_file:
            yaml.dump(user_input_yaml_file, yaml_file, default_flow_style=False)
        return f"Data Saved to {filepathforyamlfile}"
    return ""


# Ensure that the IDs used in these callback functions correspond to components in the layout
@app.callback(
    Output("save-page-modal", "is_open"),
    [Input("open-save-modal", "n_clicks"), Input("close-save-modal", "n_clicks")],
    [State("save-page-modal", "is_open")],
)
def toggle_save_page_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)

"""
@app.callback(
    [Output("preview-page-modal", "is_open"),
     Output("save-page-modal", "is_open")],
    [Input("preview-wrmXpress-product", "n_clicks"),
     Input("save-wrmXpress-yaml-file-from-preview-page", "n_clicks")],
    [State("preview-page-modal", "is_open"),
     State("save-page-modal", "is_open")]
)
def navigate_to_save_page(preview_clicks, save_clicks, preview_is_open, save_is_open):
    ctx = callback_context
    triggered_id = ctx.triggered_id

    if triggered_id == "preview-wrmXpress-product.n_clicks":
        # The "Preview" button was clicked, close the Save Page Modal
        return not preview_is_open, False
    elif triggered_id == "save-wrmXpress-yaml-file-from-preview-page.n_clicks":
        # The "Save" button was clicked, open the Save Page Modal
        return False, not save_is_open
    else:
        raise PreventUpdate
    
@app.callback(
    Output("save-page-modal", "is_open"),
    [Input("open-save-modal", "n_clicks"), Input("close-save-modal", "n_clicks")],
    [State("save-page-modal", "is_open")],
)

def toggle_save_page_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("save-page-modal", "is_open"),
    [Input("open-save-modal", "n_clicks")],
    [State("save-page-modal", "is_open")],
)

def open_save_page_modal(open_clicks, is_open):
    if open_clicks:
        return True
    return is_open

@app.callback(
    [Output("wells-information", "value"),
     Output("save-status", "children")],  # New Output for saving status
    [Input("open-preview-modal", "n_clicks"),
     Input("close-modal", "n_clicks"),
     Input("well-for-preview-id", "value")],
    [State("imaging-mode", "value"),
     State("file-structure", "value"),
     State("multi-well-rows", "value"),
     State("multi-well-cols", "value"),
     State("multi-well-detection", "value"),
     State("species", "value"),
     State("stages", "value"),
     State("motility-run", "value"),
     State("conversion-run", "value"),
     State("conversion-scale-video", "value"),
     State("conversion-rescale-multiplier", "value"),
     State("segment-run", "value"),
     State("segmentation-wavelength", "value"),
     State("cell-profilier-run", "value"),
     State("cell-profilier-pipeline", "value"),
     State("diagnostics-dx", "value"),
     State("wells-information", "value"),
     State("work-directory", "value"),
     State("input-directory", "value"),
     State("output-directory", "value"),
     State("file-path-for-preview-yaml-file", "value")]  # New State for the output file path
)
def update_user_input_yaml_file(open_clicks, close_clicks, well_for_preview_id,
                                imaging_mode, file_structure, multi_well_rows, multi_well_cols,
                                multi_well_detection, species, stages, motility_run,
                                conversion_run, conversion_scale_video, conversion_rescale_multiplier,
                                segment_run, segmentation_wavelength, cell_profilier_run,
                                cell_profilier_pipeline, diagnostics_dx, wells_information,
                                work_directory, input_directory, output_directory, file_path):
    
    # Initialize the user_input_yaml_file dictionary
    user_input_yaml_file = {
        "imaging_mode": [imaging_mode],
        "file_structure": [file_structure],
        "multi-well-rows": multi_well_rows,
        "multi-well-cols": multi_well_cols,
        "multi-well-detection": [multi_well_detection],
        "species": [species],
        "stages": [stages],
        "modules": {
            "motility": {"run": motility_run},
            "convert": {
                "run": conversion_run,
                "save_video": conversion_scale_video,
                "rescale_multiplier": conversion_rescale_multiplier
            },
            "segment": {
                "run": segment_run,
                "wavelength": [float(value) for value in segmentation_wavelength.split(',')]
            },
            "cellprofilier": {
                "run": cell_profilier_run,
                "pipeline": [cell_profilier_pipeline]
            },
            "dx": {
                "run": diagnostics_dx
            }
        },
        "wells": [float(value) for value in wells_information.split(",")],
        "directories": {
            "work": [work_directory],
            "input": [input_directory],
            "output": [output_directory]
        }
    }

    # Initialize the preview_input_yaml_file dictionary
    preview_input_yaml_file = {
        "imaging_mode": [imaging_mode],
        "file_structure": [file_structure],
        "multi-well-rows": multi_well_rows,
        "multi-well-cols": multi_well_cols,
        "multi-well-detection": [multi_well_detection],
        "species": [species],
        "stages": [stages],
        "modules": {
            "motility": {"run": motility_run},
            "convert": {
                "run": conversion_run,
                "save_video": conversion_scale_video,
                "rescale_multiplier": conversion_rescale_multiplier
            },
            "segment": {
                "run": segment_run,
                "wavelength": [float(value) for value in segmentation_wavelength.split(',')]
            },
            "cellprofilier": {
                "run": cell_profilier_run,
                "pipeline": [cell_profilier_pipeline]
            },
            "dx": {
                "run": diagnostics_dx
            }
        },
        "wells": [float(value) for value in wells_information.split(",")],
        "directories": {
            "work": [work_directory],
            "input": [input_directory],
            "output": [output_directory]
        }
    }

    # Create the full filepath using os.path.join
    output_file = os.path.join(file_path, ".yaml")

    # Dump preview data to YAML file
    with open(output_file, 'w') as yaml_file:
        yaml.dump(preview_input_yaml_file, yaml_file, default_flow_style=False)

    # Determine which button was clicked
    ctx = callback_context
    triggered_id = ctx.triggered_id
    if triggered_id is None:
        raise PreventUpdate

    # Determine whether to open or close the modal
    if open_clicks or close_clicks:
        return well_for_preview_id, f"Saved preview data to {output_file}"

    return "", f"Saved preview data to {output_file}"
"""


