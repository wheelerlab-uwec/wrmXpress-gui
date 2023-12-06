import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import callback_context
from dash.exceptions import PreventUpdate
from dash import dash_table
from collections import OrderedDict
import dash_bootstrap_components as dbc
import pandas as pd
import yaml
import plotly.graph_objs as go
import os
import pathlib
import base64
import cv2
import base64

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Create a DataFrame with 11 columns and 8 rows
columns = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# data = {col: [False] * len(rows) for col in columns}
# df = pd.DataFrame(data, index=rows)

col_vals = ['True', 'False', 'False', 'False',
            'False', 'False', 'False', 'False']

df = pd.DataFrame(OrderedDict([
    ('row', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']),
    ('01', col_vals),
    ('02', col_vals),
    ('03', col_vals),
    ('04', col_vals),
    ('05', col_vals),
    ('06', col_vals),
    ('07', col_vals),
    ('08', col_vals),
    ('09', col_vals),
    ('10', col_vals),
    ('11', col_vals),
    ('12', col_vals),
]))

gummy_worm_file_path = "Main_Page/Figures/gummy_worms.png"
wrmXpress_logo_file_path = "Main_Page/Figures/wrmXpress_logo.png"
uwec_logo_file_path = "Main_Page/Figures/uwec_logo.png"
uw_logo_file_path = "Main_Page/Figures/uw_logo.png"
wheeler_lab_file_path = "Main_Page/Figures/wheeler_lab_logo.png"

user_input_yaml_file = {}
preview_input_yaml_file = {}

# Helper Functions


def run_terminal_file(wrapper_py_file_path, yaml_file_path, plate_file_path):
    """
    Running wrmXpress through the terminal
    ======================================
    Inputs:
        wrapper_py_file_path: 
            file path to the wrapper python file (wrmXpress)
        yaml_file_path:
            file path to the yaml file for the corresponding plate
        plate_file_path:
            file path for the corresponding plate

    Returns:    
        wrmXpress product
    """
    import subprocess

    # Command to run wrmXpress
    command = f"python {wrapper_py_file_path} {yaml_file_path} {plate_file_path}"

    # Run the command in the terminal
    result = subprocess.run(command, shell=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Check the result
    if result.returncode == 0:
        return "Successful"
    else:
        return "Not Successful"


def convert_png_to_image(file_path):
    """
    converting a file path of image into an image that can be displayed in Dash
    ===========================================================================
    Inputs:
        file_path:
            file path to the image

    Returns:
        image which has been encoded into bit 64
    """
    # Obtaining the file extension
    file_extension = os.path.splitext(file_path)[1]

    # Load the image using cv2
    image = cv2.imread(file_path)

    # Convert the image to Base64
    ret, buffer = cv2.imencode(f'{file_extension}', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    # Returning encoded image
    return img_base64


gummy_wrm = convert_png_to_image(gummy_worm_file_path)
wrmXpress_logo = convert_png_to_image(wrmXpress_logo_file_path)
uwec_img = convert_png_to_image(uwec_logo_file_path)
uw_img = convert_png_to_image(uw_logo_file_path)
wheeler_lab_logo = convert_png_to_image(wheeler_lab_file_path)

# Functionality and page layout functions


def create_imaging_settings():
    """
    Creating the Structure and Layout of the Imaging Settings Accordian Item
    ========================================================================
    Inputs:
        None
    Returns:
        Accordian Item with elements for Imaging Settings
    """
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
            # New section for Multi-Well Options
            dbc.Row([
                html.H6("Multi-Well Options"),
                dbc.Col(html.H6("Multi Well Rows"), width=6),
                dbc.Col(dbc.Input(id="multi-well-rows",
                        placeholder="Please insert the multi well rows.", type="number"), width=6),
                dbc.Col(html.H6("Multi Well Columns"), width=6),
                dbc.Col(dbc.Input(id="multi-well-cols",
                        placeholder="Please insert the multi well columns.", type="number"), width=6),
            ], id='multi-well-options-row', style={'display': 'flex'}),  # Initially hidden

            # New section for additional dropdown
            dbc.Row([
                html.H6("Additional Options"),
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
            ], id='additional-options-row', style={'display': 'flex'}),  # Initially hidden
        ],
        id="instrument-settings-file-structure",
        title="Instrument Settings"
    )


def create_worm_information():
    """
    Creating the Structure and Layout of the Worm Information Accordian Item
    ========================================================================
    Inputs:
        None
    Returns:
        Accordian Item with elements for Wrom Information
    """
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
    """
    Creating the Structure and Layout of the Module Selection Accordian Item
    ========================================================================
    Inputs:
        None
    Returns:
        Accordian Item with elements for Module Selection
    """
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
            dbc.Input(id="conversion-rescale-multiplier",
                      placeholder="Please insert the rescale multiplier:", type="text"),
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
            dbc.Input(id="segmentation-wavelength",
                      placeholder="Please insert the segmentation wavelength (please seperate multiple values by a comma):", type="text"),
            html.H4("Cell Profiler"),
            html.H6("Cell Profiler Run"),
            dbc.RadioItems(
                id="cell-profiler-run",
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
            html.H6("Cell Profiler Pipeline"),
            dbc.RadioItems(
                id="cell-profiler-pipeline",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "Worm Size, Intensity, Cell Pose",
                     "value": "wormsize_intensity_cellpose"},
                    {"label": "Mf Celltox", "value": "mf_celltox"},
                    {"label": "Wormsize", "value": "wormsize"},
                    {"label": "Wormsize Trans", "value": "wormsize_trans"}
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
    """
    Creating the Structure and Layout of the Run Time Settings Accordion Item
    ========================================================================
    Inputs:
        None
    Returns:
        Accordion Item with elements for Run Time Settings
    """
    return dbc.AccordionItem(
        [
            html.H6("Select the wells to be analyzed."),
            html.Div(
                [
                    dash_table.DataTable(
                        id='table-dropdown',
                        data=df.to_dict('records'),

                        columns=[
                            {'id': 'row', 'name': ["", "Row"], 'editable': False},
                            {'id': '01', 'name': ["Column", "01"], 'presentation': 'dropdown'},
                            {'id': '02', 'name': ["Column", "02"], 'presentation': 'dropdown'},
                            {'id': '03', 'name': ["Column", "03"], 'presentation': 'dropdown'},
                            {'id': '04', 'name': ["Column", "04"], 'presentation': 'dropdown'},
                            {'id': '05', 'name': ["Column", "05"], 'presentation': 'dropdown'},
                            {'id': '06', 'name': ["Column", "06"], 'presentation': 'dropdown'},
                            {'id': '07', 'name': ["Column", "07"], 'presentation': 'dropdown'},
                            {'id': '08', 'name': ["Column", "08"], 'presentation': 'dropdown'},
                            {'id': '09', 'name': ["Column", "09"], 'presentation': 'dropdown'},
                            {'id': '10', 'name': ["Column", "10"], 'presentation': 'dropdown'},
                            {'id': '11', 'name': ["Column", "11"], 'presentation': 'dropdown'},
                            {'id': '12', 'name': ["Column", "12"], 'presentation': 'dropdown'},
                        ],
                        
                        merge_duplicate_headers=True,
                        tooltip_header={'01': 'Select "True" for all wells to be analyzed.'},

                        # Style headers with a dotted underline to indicate a tooltip
                        style_header_conditional=[{
                            'if': {'column_id': '01'},
                            'textDecoration': 'underline',
                            'textDecorationStyle': 'dotted',
                        }],
                        style_cell={'textAlign': 'center'},
                        editable=True,
                        css=[{"selector": ".Select-menu-outer",
                              "rule": "display: block !important"}],
                        markdown_options={
                            'html': True  # Enable HTML rendering for markdown cells
                        },
                        dropdown={
                            '01': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '02': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '03': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '04': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '05': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '06': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '07': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '08': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '09': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '10': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '11': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            },
                            '12': {
                                'options': [
                                    {'label': i, 'value': i}
                                    for i in df['01'].unique()
                                ]
                            }
                        }
                    ),
                    html.Div(id='table-dropdown-container'),
                    html.H6("Wells"),
                    dbc.Input(
                        id="wells-information", placeholder="Please insert the wells information (please separate multiple values by a comma):", type="text"),
                    html.H4("Directories"),
                    html.H6("Work"),
                    dbc.Input(
                        id="work-directory", placeholder="Please insert the work directory:", type="text"),
                    html.H6("Input"),
                    dbc.Input(
                        id="input-directory", placeholder="Please insert the input directory:", type="text"),
                    html.H6("Output"),
                    dbc.Input(
                        id="output-directory", placeholder="Please insert the output directory:", type="text"),
                ],
                id="run-time-settings",
            )
        ],
        title="Run-Time Settings"
    )


def save_page_content():
    """
    Creating the Structure and Layout of the Save Page 
    ========================================================================
    Inputs:
        None
    Returns:
        Accordian Item with elements for Save Page
    """
    return dbc.ModalBody(
        [
            # Content for the Save Page Modal
            html.H6("Write a YAML for running wrmXpress remotely"),
            dbc.Input(id="file-path-for-saved-yaml-file",
                      placeholder="Please enter the full path for your YAML file:", type="text"),
        ]
    )


def info_page_content():
    """
    Creating the Structure and Layout of the Information Page
    ========================================================================
    Inputs:
        None
    Returns:
        Accordian Item with elements for the Information Page
    """
    return dbc.ModalBody(
        [
            html.H4("Welcome to the Information Page"),
            html.Div(
                html.Img(
                    # Replace with your image URL
                    src=f'data:image/png;base64, {wrmXpress_logo}',
                    # Adjust image width and positioning
                    style={'width': '500px', 'float': 'right'},
                ),
            ),
            html.H6("What is wrmXpress"),
            html.P("wrmXpress stands as a groundbreaking unified framework for the analysis of diverse phenotypic imaging data in high-throughput and high-content experiments involving free-living and parasitic nematodes and flatworms. In response to the limitations of existing tools, wrmXpress transcends silos by providing a versatile solution capable of handling large datasets and generating relevant phenotypic measurements across various worm species and experimental assays. This innovative software, designed to analyze a spectrum of phenotypes such as motility, development/size, fecundity, and feeding, not only addresses current research needs but also establishes itself as a platform for future extensibility, enabling the development of custom phenotypic modules. With applications in anthelmintic screening efforts spanning schistosomes, filarial nematodes, and free-living model nematodes, wrmXpress emerges as a collaborative analytical workhorse, promising to drive innovation and facilitate cooperation among investigators with diverse scientific interests."),
            html.H6("What is a file path"),
            html.P("A file path is a reference to the location of a file or a folder in a file system. It describes the hierarchical structure of directories or folders leading to a specific file or folder. A file path is used by operating systems to locate and access files. There are two types of file paths: absolute and relative."),
            html.P("Absolute Path: An absolute path provides the complete location of a file or folder from the root directory of the file system. Example (on Windows): C:\\Users\\Username\\Documents\\file.txt Example (on Unix-like systems): /home/username/documents/file.txt Relative Path: A relative path specifies the location of a file or folder relative to the current working directory. Example: If the current working directory is /home/username/, a relative path to the file might be documents/file.txt. Relative paths are dependent on the current working directory, so they may change if the working directory changes. In both types of paths, directories or folders are separated by a delimiter (e.g., \\ on Windows or / on Unix-like systems), and the file name is typically specified at the end of the path. Understanding and correctly specifying file paths is crucial for navigating and working with files in computer systems."),
            dcc.Link(
                "File Path", href="https://en.wikipedia.org/wiki/Path_(computing)", target="_blank"),
            html.H6("What is a yaml file"),
            html.P("YAML (YAML Ain't Markup Language or, sometimes, Yet Another Markup Language) is a human-readable data serialization format. It's often used for configuration files and data exchange between languages with different data structures. YAML files use indentation to represent the structure of the data, and it relies on whitespace for nesting and scope."),
            dcc.Link(
                "YAML File", href="https://www.redhat.com/en/topics/automation/what-is-yaml", target="_blank"),

            html.H5("The Developers"),

            # Front End
            dbc.Row([
                # Full width for the title
                dbc.Col(html.H6("Front End"), width=12),
            ]),
            dbc.Row([
                dbc.Col(html.Img(
                    # Replace with your image URL
                    src=f'data:image/png;base64, {uwec_img}',
                    # Adjust image width and positioning
                    style={'width': '200px', 'float': 'left'},
                ), width=12),  # Full width for the image
            ]),

            # Back End
            dbc.Row([
                # Full width for the title
                dbc.Col(html.H6("Back End"), width=12),
            ]),
            dbc.Row([
                dbc.Col(html.Img(
                    # Replace with your image URL
                    src=f'data:image/png;base64, {uw_img}',
                    # Adjust image width and positioning
                    style={'width': '200px', 'float': 'left'},
                ), width=12),  # Full width for the image
            ]),
        ]
    )


def preview_page_content():
    """
    Creating the Structure and Layout of the Preview Page 
    ========================================================================
    Inputs:
        None
    Returns:
        Accordian Item with elements for Preview Page
    """
    return dbc.ModalBody(
        [
            html.H6("Preview Page Content"),

            # Center the Image component
            html.Img(
                # Replace with your image URL
                src=f'data:image/png;base64, {gummy_wrm}',
                style={'width': '500px', 'display': 'block', 'margin': 'auto',
                       'margin-bottom': '10px'},  # Center the image
            ),

            # Add other content below the image
            dbc.Input(id="file-path-for-preview-yaml-file",
                      placeholder="Please enter the full filepath for your yaml file:", type="text"),
            dbc.Input(id="file-path-to-wrapper-py",
                      placeholder="Please Enter the File Path for the Wrapper.py File", type="text"),
        ],
    )


# Create the Preview Page Modal
preview_page = dbc.Modal(
    [
        dbc.ModalHeader(
            "Preview Page"
        ),
        preview_page_content(),
        dbc.ModalFooter([
            # Buttons for the Info Page Modal
            dbc.Button("Preview", id="preview-preview-button",
                       className="ml-auto", color="success"),
            dbc.Button("Close", id="close-preview-modal", className="ml-auto"),
        ]),
        html.Div(id="preview-page-status")  # Placeholder for saving status
    ],
    id="preview-page-modal",
    size="xl"
)

# Create the Save Page Modal
info_page = dbc.Modal(
    [
        dbc.ModalHeader(
            "Information Page"
        ),
        info_page_content(),
        dbc.ModalFooter([
            # Buttons for the Info Page Modal
            dbc.Button("Close", id="close-info-modal", className="ml-auto"),
        ]),
        html.Div(id="info-page-status")  # Placeholder for saving status
    ],
    id="info-page-modal",
    size="xl"
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

# Main Page Layout
app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            dbc.Nav(
                [
                    dbc.NavItem(dbc.Button(
                        "Save Page", id="open-save-modal", color="primary")),
                    dbc.NavItem(dbc.Button(
                        "Info Page", id="open-info-modal", color="secondary")),
                    dbc.NavItem(dbc.Button(
                        "Preview Page", id="open-preview-modal", color="success", n_clicks=0))

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
    info_page,
    preview_page,
])


@app.callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"

# Call Back for pop up multi well


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

# Preview page call back


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
        State("wells-information", "value"),
        State("work-directory", "value"),
        State("input-directory", "value"),
        State("output-directory", "value"),
        State("file-path-for-preview-yaml-file", "value"),
        State("file-path-to-wrapper-py", "value"),
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
    wellsinformation,
    workdirectory,
    inputdirectory,
    outputdirectory,
    filepathforyamlfile,
    wrapper_py_file_path,
):
    if n_clicks:
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
            yaml.dump(preview_input_yaml_file, yaml_file,
                      default_flow_style=False)
        return f"Data Saved to {filepathforyamlfile}"
    return ""

# Save Page Call Back


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
        State("wells-information", "value"),
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
            yaml.dump(user_input_yaml_file, yaml_file,
                      default_flow_style=False)
        return f"Data Saved to {filepathforyamlfile}"
    return ""

# Ensure that the IDs used in these callback functions correspond to components in the layout


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
        # Toggle the preview modal based on the button click
        return False, False, not is_preview_open
    else:
        return is_save_open, is_info_open, is_preview_open


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
     State("cell-profiler-run", "value"),
     State("cell-profiler-pipeline", "value"),
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
                                segment_run, segmentation_wavelength, cell_profiler_run,
                                cell_profiler_pipeline, diagnostics_dx, wells_information,
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
            "cellprofiler": {
                "run": cell_profiler_run,
                "pipeline": [cell_profiler_pipeline]
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
            "cellprofiler": {
                "run": cell_profiler_run,
                "pipeline": [cell_profiler_pipeline]
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
