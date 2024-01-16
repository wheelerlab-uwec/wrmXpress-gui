########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import docker
import yaml
import time
from pathlib import Path
import numpy as np
import plotly.express as px
from PIL import Image
from app.utils.callback_functions import prep_yaml
import os
import plotly.graph_objs as go
import subprocess

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
                                    html.H4("Input",
                                            className="text-center mb-5"),
                                    html.Br(),
                                    html.H6(
                                        "Path:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(id='input-path-output'),
                                    html.Div(
                                        dcc.Graph(
                                            id='input-preview',
                                            figure={'layout': layout},
                                            className='h-100 w-100'
                                        )),
                                    dbc.Button('Load first input image',
                                               id='submit-val',
                                               className="d-grid gap-2 col-6 mx-auto",
                                               color="primary",
                                               n_clicks=0),
                                ]
                                )
                            ),
                            width={'size': 6}
                        ),

                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4(
                                        "Analysis", className="text-center"),
                                    dcc.Dropdown(
                                        id='preview-dropdown',
                                        placeholder='Select image to preview...'),
                                    html.Br(),
                                    html.H6(
                                        "Command:", className="card-subtitle"),
                                    html.Br(),
                                    dcc.Markdown(
                                        id='analysis-preview-message'),
                                    dcc.Graph(
                                        id='analysis-preview',
                                        figure={'layout': layout},
                                        className='h-100 w-100'
                                    ),
                                    dbc.Alert(id='resolving-error-issue-preview',is_open=False, color='success', duration=6000),
                                    dbc.Button(
                                        "Preview analysis", id="preview-button", className="d-grid gap-2 col-6 mx-auto", color="primary", n_clicks=0),
                                    dbc.Alert(id='view-docker-logs',is_open=False, color='success', duration=30000),
                                ]
                                )
                            ),
                            width={'size': 6})
                        ])
            ]
            )
        ]
        )
    ],
)


########################################################################
####                                                                ####
####                           Callbacks                            ####
####                                                                ####
########################################################################

@callback(
    Output('input-path-output', 'children'),
    Output('input-preview', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def update_preview_image(n_clicks, store):

    wells = store['wells']
    first_well = wells[0].replace(', ', '')

    platename = store['platename']
    plate_base = platename.split("_", 1)[0]

    volume = store['mount']
    if n_clicks >= 1:
        # assumes IX-like file structure
        img_path = Path(
            volume, f'{platename}/TimePoint_1/{plate_base}_{first_well}.TIF')
        img = np.array(Image.open(img_path))
        fig = px.imshow(img, color_continuous_scale="gray")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return f'```{img_path}```', fig
    n_clicks = 0


@callback(
    Output('preview-dropdown', 'options'),
    # update the option dropdown when the previous load is clicked
    Input('submit-val', 'n_clicks'),
    State('store', 'data'),
    prevent_initial_call=True
)
def get_options(nclicks, store):

    motility = store['motility']
    segment = store['segment']
    selection_dict = {'motility': 'motility', 'segment': 'binary'}
    option_dict = {}

    if nclicks is not None:
        for selection in selection_dict.keys():
            if eval(selection) == 'True':
                option_dict[selection] = selection_dict[selection]

    dict_option = {v: k for k, v in option_dict.items()}
    return dict_option


@callback(
    Output('analysis-preview-message', 'children'),
    Output('analysis-preview', 'figure'),
    Output('resolving-error-issue-preview', 'is_open'),
    Output('resolving-error-issue-preview','children'),
    Output("view-docker-logs", 'is_open'),
    Output("view-docker-logs", 'children'),
    Input('preview-button', 'n_clicks'),
    State('store', 'data'),
    State('preview-dropdown', 'value'),
    prevent_initial_call=True
)
def run_analysis(
    nclicks,
    store,
    selection
):
    volume = store['mount']
    platename = store['platename']
    wells = store["wells"]

    if nclicks:
        """
        Checking if wrmXpress container exists
        """
        try:
            good_to_go = False
            check_for_names = ['zamanianlab/wrmxpress', 'latest']
            client = docker.from_env()
            images_in_docker = client.images.list()
            for img in images_in_docker:
                img = f"{img}"
                image_info = img.strip()[8:-1].strip("'").split("', '")  # Remove angle brackets, quotes, and split
                image_tag = image_info[-1]
                if check_for_names[0] in image_tag:
                    good_to_go = True
                if check_for_names[1] in image_tag:
                    good_to_go = True

            if good_to_go == False:
                return None, None, True, f'Please ensure that you have the Image "{check_for_names[0]}" and is the "{check_for_names[1]}" image.', False, ''
        except ValueError as ve:
            return None, None, True, 'An error occured somewhere', False, ''

        if wells == 'All':
            first_well = 'A01'
        else:
            first_well = wells[0]
        plate_base = platename.split("_", 1)[0]

        """
        Checking if input folder exists, and if not, create it, 
        then subsequently copy the images into this folder
        """
        # input and platename input folder paths
        input_folder = Path(volume, 'input')
        platename_input_folder = Path(input_folder, platename)
        
        # collecting the time point folders
        folder_containing_img = Path(volume, platename)
        timept_list_dirs = os.listdir(folder_containing_img)
        folders = [item for item in timept_list_dirs if os.path.isdir(os.path.join(folder_containing_img, item))]
        print(folders)

        # if input folder does not exists
        if not os.path.exists(input_folder):

            # create input folder and platename input folder
            os.mkdir(input_folder)
            os.mkdir(platename_input_folder)

            # HTD file path
            htd_file_path = f'{Path(folder_containing_img)}/{plate_base}.HTD'
            
            #copying the .htd file into the platename folder
            os.system(f'cp {htd_file_path} {platename_input_folder}')

            # iterating through each of the time points
            for folder in folders:

                # creating the time point folder
                os.mkdir(Path(platename_input_folder, folder))

                # first well file path
                first_well_path = f'{Path(folder_containing_img, folder, plate_base)}_{first_well}.TIF'

                # coping the images into the newly created time point folder
                os.system(f'cp {first_well_path} {Path(platename_input_folder, folder)}')

        # if the input folder exists
        if os.path.exists(input_folder):

            # if the platename input folder does not exist
            if not os.path.exists(platename_input_folder):

                # create platename input folder
                os.mkdir(platename_input_folder)

                # HTD file path
                htd_file_path = f'{Path(folder_containing_img)}/{plate_base}.HTD'

                #copying the .htd file into the platename folder
                os.system(f'cp {htd_file_path} {platename_input_folder}')

                # iterating through each of the time points
                for folder in folders:

                    # creating the time point folder
                    os.mkdir(Path(platename_input_folder, folder))

                    # first well file path
                    first_well_path = f'{Path(folder_containing_img, folder, plate_base)}_{first_well}.TIF'
                    
                    # coping the images into the newly created time point folder
                    os.system(f'cp {first_well_path} {Path(platename_input_folder, folder)}')

            # if the platename input folder exists
            if os.path.exists(platename_input_folder):

                # HTD file path
                htd_file_path = f'{Path(folder_containing_img)}/{plate_base}.HTD'

                # if the .htd file does not exist
                if not os.path.exists(htd_file_path):

                    # copy the .htd file into the platename folder
                    os.system(f'cp {htd_file_path} {platename_input_folder}')

                # iterating through each of the time points
                for folder in folders:

                    # if the time point folder does not exist
                    if not os.path.exists(Path(platename_input_folder, folder)):
    
                        # create the time point folder
                        os.mkdir(Path(platename_input_folder, folder))
    
                        # first well file path
                        first_well_path = f'{Path(folder_containing_img, folder, plate_base)}_{first_well}.TIF'
                        
                        # coping the images into the newly created time point folder
                        os.system(f'cp {first_well_path} {Path(platename_input_folder, folder)}')
    
                    # if the time point folder exists
                    if os.path.exists(Path(platename_input_folder, folder)):
                        
                        # first well file path
                        first_well_path = f'{Path(folder_containing_img, folder, plate_base)}_{first_well}.TIF'
               
                        # if the images do not exist
                        if not os.path.exists(first_well_path):
    
                            # coping the images into the newly created time point folder
                            os.system(f'cp {first_well_path} {Path(platename_input_folder, folder)}')


        # defining the yaml file path (same as the filepath from configure.py)
        full_yaml = Path(volume, platename + '.yml')

        # reading in yaml file
        with open(full_yaml, 'r') as file:
            data = yaml.safe_load(file)

        # assigning first well to the well value
        data['wells'] = [first_well]

        # Dump preview data to temp YAML file
        with open(full_yaml, 'w') as yaml_file:
            yaml.dump(data, yaml_file,
                    default_flow_style=False)

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

        # Run the docker logs command
        result = subprocess.run(['docker', 'logs', '-f', container_name], capture_output=True, text=True).stdout

        # Assuming `output` is the string containing the docker logs output
        output_lines = result.splitlines()  # Split the output into lines

        # Convert each line into an HTML paragraph element
        result = [html.P(line, className="mb-0") for line in output_lines]

        # assumes IX-like file structure
        img_path = Path(
            volume, 'work', f'{platename}/{first_well}/img/{platename}_{first_well}_{selection}.png')

        while not os.path.exists(img_path):
            time.sleep(1)

        img = np.array(Image.open(img_path))
        fig = px.imshow(img, color_continuous_scale="gray")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        if isinstance(wells, list):
            if len(wells) == 96:
                wells = ['All']
            else:
                wells = wells
        elif isinstance(wells, str):
            wells = [wells]
        # assigning well to the full well values
        data['wells'] = wells

        # Dump preview data to YAML file
        with open(full_yaml, 'w') as yaml_file:
            yaml.dump(data, yaml_file,
                    default_flow_style=False)
            
        return command_message, fig, False, f'', True, result
