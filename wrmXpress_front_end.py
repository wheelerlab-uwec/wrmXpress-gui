import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import yaml

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"})
external_stylesheets = ['/Users/zach/avacado_analytics/wrmXpress/wrmXpress_funny_file.css']  # Add the path to your CSS file

app.title = "wrmXpress"  # Set the title of your app

image_path = "/Users/zach/avacado_analytics/wrmXpress/funny-venn-diagram-8.png"
image_path_upper_right = "/Users/zach/avacado_analytics/wrmXpress/output.png"  # Specify the path to your upper right image
image_path_bottom = "/Users/zach/avacado_analytics/wrmXpress/gummy.png"  # Specify the path to your bottom image

# Modal body to display the summary
modal_body = dbc.ModalBody([
    html.Div(id='selection-summary')
])

# Modal for displaying information when the "Submit" button is clicked
modal = dbc.Modal(
    [
        dbc.ModalHeader("Submission Successful"),
        modal_body,  # Use the modal_body here
        dbc.ModalFooter(
            dbc.Row([
                dbc.Col(
                    dbc.Button("Confirm", id="confirm-button", color="success"),
                    width={"size": 3, "offset": 5}
                ),
                dbc.Col(
                    dbc.Button("Cancel", id="cancel-button", color="danger"),
                    width={"size": 3, 'offset': 5}
                ),
            ]),
        ),
    ],
    id="submit-modal",
    size="lg",
    centered=True,
)

# Define the layout of your Dash app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Welcome to wrmXpress", style={'color': 'white'}),
            width={"size": 6, "offset": 3},
            className="mb-4"
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Img(
                src=image_path,
                alt='Upper Right Image',
                style={'width': '100px', 'position': 'absolute', 'top': '10px', 'right': '10px', 'display': 'block', 'margin': '0 auto'},
            ),
            width=6,
            className='mx-auto',  # Center the content horizontally
        ),
    ]),
    # Second row with the input button
    dbc.Row([
        dbc.Col(
            [html.P("Input", className="mb-2"),  # Text above the button
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload File'),
                multiple=False
            )],
            width=6,
            className="mb-3"
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(id='output-message', className="mt-4")
        )
    ]),
    # New section for Instrument Settings
    dbc.Row([
        dbc.Col(
            html.H2("Instrument Settings", style={'color': 'white'}),
            width=12,  # Full width for the title
            className="mb-3"
        ),
        dbc.Col(
            [
                html.H3("Imaging Mode", style={'color': 'white'}),  # Subheading for Imaging Mode
                dcc.RadioItems(
                    id='imaging-mode',
                    options=[
                        {'label': 'Single Well', 'value': 'single-well'},
                        {'label': 'Multi Well', 'value': 'multi-well'}
                    ],
                    value='single-well',
                    labelStyle={'display': 'block', 'font-size': '18px'}  # Font size adjustment
                ),
            ],
            width=6,
        ),
        dbc.Col(
            [
                html.H3("File Structure", style={'color': 'white'}),  # Subheading for File Structure
                dcc.RadioItems(
                    id='file-structure',
                    options=[
                        {'label': 'Image Express', 'value': 'image-express'},
                        {'label': 'AVI', 'value': 'avi'}
                    ],
                    value='image-express',
                    labelStyle={'display': 'block', 'font-size': '18px'}  # Font size adjustment
                ),
            ],
            width=6,
        ),
    ]),

    dbc.Row([
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
        
    ]),
     # New section for Multi-Well Rows and Columns dropdown
    dbc.Row([
        dbc.Col(
            html.H3("Multi-Well Options", style={'color': 'white'}),  # Subheading for Multi-Well Options
            width=6,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='multi-well-options',
                options=[
                    {'label': 'Multi-Well Rows', 'value': 'multi-well-rows'},
                    {'label': 'Multi-Well Columns', 'value': 'multi-well-columns'},
                ],
                multi=True,
                placeholder="Select options",
            ),
            width=6,
        ),
    ], id='multi-well-options-row', style={'display': 'none'}),  # Initially hidden
    # New section for additional dropdown
    dbc.Row([
        dbc.Col(
            html.H3("Additional Options", style={'color': 'white'}),  # Subheading for additional options
            width=6,
        ),
        dbc.Col(
            dcc.Checklist(
                id='additional-options',
                options=[
                    {'label': 'Add', 'value': 'add'},
                    {'label': 'Stuff', 'value': 'stuff'},
                    {'label': 'Here', 'value': 'here'}
                ],
                value=[],
                labelStyle={'display': 'block', 'font-size': '18px'}  # Font size adjustment
            ),
            width=6,
        ),
    ], id='additional-options-row', style={'display': 'none'}),  # Initially hidden
    dbc.Row([
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
    ]),
    # New section for Worm Information
    dbc.Row([
        dbc.Col(
            html.H2("Worm Information", style={'color': 'white'}),
            width=12,  # Full width for the title
            className="mb-3"
        ),
        dbc.Col(
            [
                html.H3("Species", style={'color': 'white'}),  # Subheading for Imaging Mode
                dcc.RadioItems(
                    id='species',
                    options=[
                        {'label': 'Bma', 'value': 'bma'},
                        {'label': 'Cel', 'value': 'cel'},
                        {'label': 'Sma', 'value': 'sma'}
                    ],
                    value='bma',
                    labelStyle={'display': 'block', 'font-size': '18px'}  # Font size adjustment
                ),
            ],
            width=6,
        ),
        dbc.Col(
            [
                html.H3("Stages", style={'color': 'white'}),  # Subheading for File Structure
                dcc.RadioItems(
                    id='stages',
                    options=[
                        {'label': 'Mf', 'value': 'mf'},
                        {'label': 'Adult', 'value': 'adult'},
                        {'label': 'Mixed', 'value': 'mixed'}
                    ],
                    value='mf',
                    labelStyle={'display': 'block', 'font-size': '18px'}  # Font size adjustment
                ),
            ],
            width=6,
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
    ]),
    # New section for Module Settings
    dbc.Row([
        dbc.Col(
            html.H2("Module Settings", style={'color': 'white'}),
            width=12,  # Full width for the title
            className="mb-3"
        ),
    ]),
    dbc.Row([
        dbc.Col(
            [
                html.H4("Motility", style={'color': 'white'}),  # Subheading for Motility
                html.Div([
                    html.H5("Run", style={'color': 'white'}),  # Sub-subheading for Run
                    dcc.Dropdown(
                        id='motility-run',
                        options=[
                            {'label': 'True', 'value': 'True'},
                            {'label': 'False', 'value': 'False'}
                        ],
                        value='True',
                        style={'font-size': '18px'}  # Font size adjustment
                    ),
                ]),
            ],
            width=6,
        ),
        dbc.Col(
            [
                html.H4("Convert", style={'color': 'white'}),  # Subheading for Convert
                html.Div([
                    html.H5("Run", style={'color': 'white'}),  # Sub-subheading for Run
                    dcc.Dropdown(
                        id='convert-run',
                        options=[
                            {'label': 'True', 'value': 'True'},
                            {'label': 'False', 'value': 'False'}
                        ],
                        value='True',
                        style={'font-size': '18px'}  # Font size adjustment
                    )
                ]),
            ],
            width=6,
        ),
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Save Video", style={'color': 'white'}),  # Sub-subheading for Save Video
            dcc.Dropdown(
                id='convert-save-video',
                options=[
                    {'label': 'True', 'value': 'true'},
                    {'label': 'False', 'value': 'false'}
                ],
                value='true',
                style={'font-size': '18px'}  # Font size adjustment
            ),
        ]),
        dbc.Col([
            html.H4("Rescale Multiplier", style={'color': 'white'}),  # Sub-subheading for Rescale Multiplier
            dcc.Dropdown(
                id='convert-rescale-multiplier',
                options=[
                    {'label': 'True', 'value': 'true'},
                    {'label': 'False', 'value': 'false'}
                ],
                value='true',
                style={'font-size': '18px'}  # Font size adjustment
            ),
        ])
    ]),
    dbc.Row([
        dbc.Col(
            [
                html.H3("Segment", style={'color': 'white'}),  # Subheading for Segment
                html.Div([
                    html.H4("Run", style={'color': 'white'}),  # Sub-subheading for Run
                    dcc.Dropdown(
                        id='segment-run',
                        options=[
                            {'label': 'True', 'value': 'true'},
                            {'label': 'False', 'value': 'false'}
                        ],
                        value='true',
                        style={'font-size': '18px'}  # Font size adjustment
                    ),
                    html.H4("Wavelength", style={'color': 'white'}),  # Sub-subheading for Wavelength
                    dcc.Input(
                        id='segment-wavelength',
                        type='text',
                        value='',
                        style={'width': '80%', 'font-size': '18px'}  # Font size adjustment
                    ),
                ]),
            ],
            width=6,
        ),
        dbc.Col(
            [
                html.H3("Cell Profiling", style={'color': 'white'}),  # Subheading for Cell Profiling
                html.Div([
                    html.H4("Run", style={'color': 'white'}),  # Sub-subheading for Run
                    dcc.Dropdown(
                        id='cellprofiling-run',
                        options=[
                            {'label': 'True', 'value': 'true'},
                            {'label': 'False', 'value': 'false'}
                        ],
                        value='true',
                        style={'font-size': '18px'}  # Font size adjustment
                    ),
                    html.H4("Pipeline", style={'color': 'white'}),  # Sub-subheading for Pipeline
                    dcc.Dropdown(
                        id='pipeline_dropdown',
                        options=[
                            {'label': 'mf_celltox', 'value': 'mf_celltox'},
                            {'label': 'feeding', 'value': 'feeding'},
                            {'label': 'wormsize', 'value': 'wormsize'},
                            {'label': 'wormsize_trans', 'value': 'wormsize_trans'}
                        ],
                        value='true',
                        style={'mf_celltox': '18px'}  # Font size adjustment
                    ),
                ]),
            ],
            width=6,
        ),
    ]),
    dbc.Row([
        dbc.Col(
            [
                html.H3("Diagnostics", style={'color': 'white'}),  # Subheading for Diagnostics
                html.Div([
                    html.H4("dx", style={'color': 'white'}),  # Sub-subheading for dx
                    dcc.Dropdown(
                        id='diagnostics-dx',
                        options=[
                            {'label': 'True', 'value': 'true'},
                            {'label': 'False', 'value': 'false'}
                        ],
                        value='true',
                        style={'font-size': '18px'}  # Font size adjustment
                    ),
                ]),
            ],
            width=6,
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
        dbc.Col(
            html.Hr(),  # Add a horizontal line
            width=6,
        ),
    ]),
    # New section for Run-Time settings
    dbc.Row([
        dbc.Col(
            html.H2("Run-Time Settings", style={'color': 'white'}),
            width=12,  # Full width for the title
            className="mb-3"
        ),
    ]),
    dbc.Row([
        dbc.Col(
            [
                html.H3("Wells", style={'color': 'white'}),  # Subheading for Wells
                dcc.Input(
                    id='wells',
                    type='text',
                    value='all',
                    style={'width': '80%'}  # Adjust the width of the input box
                ),
            ],
            width=6,
        ),
        dbc.Col(
            [
                html.H3("Directories", style={'color': 'white'}),  # Subheading for Directories
                html.Div([
                    html.H4("Work", style={'color': 'white'}),  # Sub-subheading for Work
                    dcc.Upload(
                        id='upload-input-folder',
                        children=html.Button('Select Input Folder', style={'color': 'white'}),
                        multiple=False,
                    ),
                    dcc.Input(
                        id='output-filename',
                        type='text',
                        value='',
                        placeholder='Enter output filename...',
                        style={'width': '80%', 'font-size': '18px'}  # Font size adjustment
                    ),
                    dcc.Upload(
                        id='upload-output-folder',
                        children=html.Button('Select Output Folder', style={'color': 'white'}),
                        multiple=False,
                    ),
                ]),
            ],
            width=6,
        ),
    ]),
    # New section for Submit button
    dbc.Row([
        dbc.Col(
            dbc.Button("Submit", id="submit-button", color="primary", className="mt-3"),
            width={"size": 6, "offset": 3},
        )
    ]),
    modal,  
], style={'background-color': 'black', 'color': 'white'})  # Set background color and text color

# Define callback to control the visibility of Cell Profiler options
@app.callback(
    [Output('cell-profiler-radio', 'style')],
    [Input('cell-profiler-checkbox', 'value')]
)
def update_cell_profiler_options(cell_profiler_checked):
    if 'cell-profiler' in cell_profiler_checked:
        return [{'display': 'block'}]
    else:
        return [{'display': 'none'}]

# Modify the existing callback to control the visibility of additional options
@app.callback(
    [Output('additional-options-row', 'style')],
    [Input('imaging-mode', 'value'),
     Input('file-structure', 'value')]
)
def show_additional_components(imaging_mode, file_structure):
    if imaging_mode == 'multi-well' and file_structure == 'avi':
        return [{'display': 'block'}]
    else:
        return [{'display': 'none'}]

# Callback to control the visibility of Multi-Well Options dropdown
@app.callback(
    [Output('multi-well-options-row', 'style')],
    [Input('imaging-mode', 'value')]
)
def show_multi_well_options(imaging_mode):
    if imaging_mode == 'multi-well':
        return [{'display': 'block'}]
    else:
        return [{'display': 'none'}]

@app.callback(
    Output("submit-modal", "is_open"),
    Input("submit-button", "n_clicks"),
    State("submit-modal", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open 
# Callback to update the selection summary in the modal
@app.callback(
    Output('selection-summary', 'children'),
    [
        Input('imaging-mode', 'value'),
        Input('file-structure', 'value'),
        Input('multi-well-options', 'value'),
        Input('additional-options', 'value'),
        Input('species', 'value'),
        Input('stages', 'value'),
        Input('motility-run', 'value'),
        Input('convert-run', 'value'),
        Input('convert-save-video', 'value'),
        Input('convert-rescale-multiplier', 'value'),
        Input('segment-run', 'value'),
        Input('segment-wavelength', 'value'),
        Input('cellprofiling-run', 'value'),
        Input('pipeline_dropdown', 'value'),
        Input('diagnostics-dx', 'value'),
        Input('wells', 'value'),
    ]
)
def update_selection_summary(
        imaging_mode, file_structure, multi_well_options, additional_options,
        species, stages, motility_run, convert_run, convert_save_video,
        convert_rescale_multiplier, segment_run, segment_wavelength,
        cellprofiling_run, pipeline_dropdown, diagnostics_dx, wells):
    # Create a dictionary to store the selections
    selections = {
        'Imaging Mode': imaging_mode,
        'File Structure': file_structure,
        'Multi-Well Options': multi_well_options,
        'Additional Options': additional_options,
        'Species': species,
        'Stages': stages,
        'Motility Run': convert_save_video,
        'Rescale Multiplier': convert_rescale_multiplier,
        'Segment Run': segment_run,
        'Wavelength': segment_wavelength,
        'Cell Profiling Run': cellprofiling_run,
        'Pipeline Dropdown': pipeline_dropdown,
        'Diagnostics dx': diagnostics_dx,
        'Wells': wells,
    }

    # Create a list of HTML elements to display the selections
    selection_items = [html.Div(f"{key}: {value}") for key, value in selections.items()]

    return selection_items

if __name__ == '__main__':
    app.run_server(debug=True)


