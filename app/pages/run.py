########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import docker
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
import os
import dash
import plotly.graph_objs as go
import subprocess
import shutil

# importing utils
from app.utils.styling import layout

dash.register_page(__name__)

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################

layout = dbc.ModalBody(
    [
        # Preview page contents
        html.Div([
            html.Div([
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Configure Summary",
                                        className="text-center"),
                                dcc.Markdown(
                                    id='img-mode-output',
                                    className="card-subtitle"),
                                dcc.Markdown(
                                    id='file-structure-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='plate-format-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='img-masking-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='mod-selection-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='volume-name-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='plate-name-output',
                                    className='card-subtitle'),
                                dcc.Markdown(
                                    id='wells-content-output',
                                    className='card-subtitle'),
                                dbc.Button('Begin Analysis',
                                           id='submit-analysis',
                                           className="d-grid gap-2 col-6 mx-auto",
                                           color="primary",
                                           n_clicks=0),
                                dcc.Graph(
                                    id='image-analysis-preview',
                                    # Empty layout for now
                                    figure={'layout': {}},
                                    className='h-100 w-100'
                                ),
                            ])
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4(
                                    "Run Diagnosis", className="text-center"),
                                dcc.Graph(
                                    id='analysis-postview',
                                    # Empty layout for now
                                    figure={'layout': {}},
                                    className='h-100 w-100'
                                ),
                                dcc.Graph(
                                    id='analysis-postview-another',
                                    # Empty layout for now
                                    figure={'layout': {}},
                                    className='h-100 w-100'
                                ),
                            ])
                        )
                    ),
                ]),
                dbc.Row([
                    dbc.Alert(
                        id='run-page-alert',
                        color='success',
                        is_open=False,
                        duration=30000,
                    ),
                ])
            ])
        ])
    ]
)

########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################


@callback(
    Output("img-mode-output", 'children'),
    Output('file-structure-output', 'children'),
    Output('plate-format-output', 'children'),
    Output('img-masking-output',  'children'),
    Output('mod-selection-output', 'children'),
    Output('volume-name-output', 'children'),
    Output('plate-name-output',  'children'),
    Output('wells-content-output',  'children'),
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_results_message_for_run_page(
    nclicks,
    store
):
    img_mode = f'Imaging Mode: {store["img_mode"]}'
    file_structure = f'File Structure: {store["file_structure"]}'
    plate_format = f'Plate Format: Rows = {store["rows"]}, Cols = {store["cols"]}'
    img_masking = f'Image Masking: {store["img_masking"]}'
    mod_selection = f'Module Selection: {store["motility"]}'
    volume = f'Volume: {store["mount"]}'
    platename = f'Platename: {store["platename"]}'
    wells = f'Wells: {store["wells"]}'
    results = [
        img_mode,
        file_structure,
        plate_format,
        img_masking,
        mod_selection,
        volume,
        platename,
        wells
    ]
    if nclicks:
        return results


@callback(
    Output('image-analysis-preview', 'figure'),
    Output('analysis-postview', 'figure'),
    Output('analysis-postview-another', 'figure'),
    Output('run-page-alert', 'is_open'),
    Output('run-page-alert', 'children'),
    Input('submit-analysis', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def run_analysis(
    nclicks,
    store
):
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]

    if nclicks:

        """
        Checking if input folder exists, and if not, create it, 
        then subsequently copy the images into this folder
        """
        # check to see how many wells we are analyzing
        remove_wells_later = False
        if len(wells) == 1 and wells[0] != 'All':
            remove_wells_later = True
            # check to see if a second well exists

            # Assuming wells[0] is a string like "A01"
            first_well = wells[0]
            # Get the last character of the well identifier
            last_char = first_well[-1]
            # Increment the last character by 1
            next_char = chr(ord(last_char) + 1)
            # Concatenate the first part with the incremented character
            second_well = first_well[:-1] + next_char
            wells.append(second_well)
            first_well = wells

            # create a new img in the volume with the new well for analysis
            plate_base = platename.split("_", 1)[0]
            # Collecting the time point folders
            folder_containing_img = Path(volume, platename)
            folders = [item for item in os.listdir(folder_containing_img) if os.path.isdir(
                os.path.join(folder_containing_img, item))]
            # Iterate through each time point
            for folder in folders:
                # Copy first and second well image into time point folder
                first_well_path = folder_containing_img / \
                    folder / f'{plate_base}_{first_well[0]}.TIF'
                second_well_path = folder_containing_img / \
                    folder / f'{plate_base}_{first_well[1]}.TIF'
                # rename first well path with second well name
                shutil.copy(first_well_path, second_well_path)

        # input and platename input folder paths
        input_folder = Path(volume, 'input')
        platename_input_folder = Path(input_folder, platename)

        # if the input folder does not exist, create it
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
            os.system(f'cp -r {Path(volume, platename)} {input_folder}')

        # if the input folder exists, but the platename folder does not exist, create it
        if os.path.exists(input_folder):
            if not os.path.exists(platename_input_folder):
                os.system(f'cp -r {Path(volume, platename)} {input_folder}')

            # if the input folder exists, and the platename folder exists, replace the platename folder with the input folder
            if os.path.exists(platename_input_folder):
                os.system(f'cp -rf {Path(volume, platename)} {input_folder}')

        client = docker.from_env()
        print(client)

        command = f"python wrmXpress/wrapper.py {platename}.yml {platename}"
        command_message = f"```python wrmXpress/wrapper.py {platename}.yml {platename}```"

        container = client.containers.run('zamanianlab/wrmxpress', command=f"{command}", detach=True,
                                          volumes={f'{volume}/input/': {'bind': '/input/', 'mode': 'rw'},
                                                   f'{volume}/output/': {'bind': '/output/', 'mode': 'rw'},
                                                   f'{volume}/work/': {'bind': '/work/', 'mode': 'rw'},
                                                   f'{volume}/{platename}.yml': {'bind': f'/{platename}.yml', 'mode': 'rw'}
                                                   })
        # Get the name of the most recent container
        container_name = container.name

        # Wait for the container to finish running (adjust timeout as needed)
        container.wait(timeout=300)

        # Retrieve and process the logs after the container has finished
        result = subprocess.run(
            ['docker', 'logs', container_name], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()

        # ensure that these rows of the output are not indented
        non_indented = [
            'instrument settings:',
            "wormzzzz:",
            "modules:",
            "run-time settings:",
            "HTD metadata:",
        ]
        # Convert each line into an HTML paragraph element
        markdown_lines = [dcc.Markdown(f"```{line}```", className='mb-0') if line in non_indented else dcc.Markdown(
            f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```{line}```", className='mb-0') for line in output_lines]

        # assumes IX-like file structure
        img_path = Path(
            volume, 'output', 'thumbs', f'{platename}.png')

        # directory path to the thumbs
        file_path = Path(
            volume, 'output', 'thumbs'
        )

        # ensures that the images have been processed
        while not os.path.exists(img_path):
            time.sleep(1)

        # empty list of filepaths which will be added to later
        files_with_png = []

        # Iterate through all files and subdirectories
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.lower().endswith('.png'):  # Check if the file is a PNG file
                    # Get the full file path
                    file_path = os.path.join(root, file)
                    # append the file path to the list
                    files_with_png.append(file_path)

        # empty list for the figures to be added to once they have been processed
        figs = []

        # iterating through each file path and getting the subsequent image
        for i, file_path in enumerate(files_with_png):
            img = np.array(Image.open(file_path))  # Open the image using PIL
            fig = px.imshow(img, color_continuous_scale="gray")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            figs.append(fig)  # appending this image to the list
        # Return the figures as a tuple

        # remove all the created files
        if remove_wells_later == True:
            # create a new img in the volume with the new well for analysis
            plate_base = platename.split("_", 1)[0]
            # Collecting the time point folders
            folder_containing_img = Path(volume, platename)
            folders = [item for item in os.listdir(folder_containing_img) if os.path.isdir(
                os.path.join(folder_containing_img, item))]
            # Iterate through each time point
            for folder in folders:
                # obtain the second well image path
                second_well_path = folder_containing_img / \
                    folder / f'{plate_base}_{first_well[1]}.TIF'
                # remove the second well image
                os.remove(second_well_path)
        return figs[0], figs[1], figs[2], True, markdown_lines
