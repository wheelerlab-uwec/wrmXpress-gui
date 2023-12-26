########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc
from dash import dcc, html

########################################################################
####                                                                ####
####                              Layout                            ####
####                                                                ####
########################################################################
info_page_content = dbc.ModalBody(
    [
        # Introduction to wrmXpress
        html.P("wrmXpress is a unified framework for the analysis of diverse phenotypic imaging data in high-throughput and high-content experiments involving free-living and parasitic nematodes and flatworms. wrmXpress is a versatile solution capable of handling large datasets and generating relevant phenotypic measurements across various worm species and experimental assays. This software, designed to analyze a spectrum of phenotypes such as motility, development/size, fecundity, and feeding, not only addresses current research needs but also establishes itself as a platform for future extensibility, enabling the development of custom phenotypic modules."),

        # Header of Usage
        html.H3("Usage"),
        html.P("There are two options for running wrmXpress:"),

        # Content of usage seperated into cards 
        dbc.Row(
            [
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(
                            [
                                # Remote card
                                html.H5("Remotely", className="card-title"),
                                dcc.Markdown(
                                    # Remote card content
                                    "wrmXpress was originally designed to be invoked remotely, using a high-performance or high-throughput computer. There are many ways to go about this, but we recommend encapsulating the entire process in a Docker container. The container should include the Python libraries required by wrmXpress (see the [Zamanian Lab's Dockerfile/conda environment](https://github.com/zamanianlab/Docker/tree/main/chtc-wrmxpress) for an example), the cloned [wrmXpress repository](https://github.com/zamanianlab/wrmXpress), the input data in a directory called `input/`, and a YAML file that configures the analysis. A user can use this graphical user interface (GUI) to produce the YAML by selecting the options and modules and clicking Save YAML.",
                                    className="card-text")
                            ]
                        )
                    ],
                        color='light' # Defines the color for the card
                    )
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(
                             [
                                 # Locally Card
                                 html.H5("Locally", className="card-title"),
                                 # Local card content
                                 dcc.Markdown("Many analyses, such as those that include a few dozen separate videos or images, can be performed on a desktop computer without the need for high-performance or high-throughput computing. For these, a user can use this GUI to select the options and modules and run the analysis by clicking the Preview and Run button.",
                                              className="card-text")
                             ]
                             )
                    ],
                        color='light' # Defines the color for the card
                        )
                ])
            ]),
        html.Br(),
        # Developers section of information page
        html.H3("The Developers"),
        dcc.Markdown(
            "wrmXpress is entirely open-source. The code for the back-end is maintained by the [Zamanian Lab](https://www.zamanianlab.org/) at the University of Wisconsin-Madison and can be found [here](https://github.com/zamanianlab/wrmXpress). The code for the front-end is maintained by the [Wheeler Lab](wheelerlab.bio) at the University of Wisconsin-Eau Claire and can be found [here](https://github.com/wheelerlab-uwec/wrmXpress-gui)."),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [html.Img(
                        # Link to wheeler lab logo
                        src='https://assets.super.so/6d48c8d3-6e72-45c3-a5b9-04514883421e/images/9da71b53-e8f2-4234-9e55-e50d302f5c46/Lab_logo.svg',
                        style={'width':'30%'}
                    ),
                    html.Img(
                        # Link to uwec seal
                        src='https://lib02.uwec.edu/Omeka/files/original/37b67b60cca3c3ad308515aab27a66afe6c75b2f.gif',
                        style={'width':'30%'}
                    )],
                    style={'textAlign':'center'}
                ),
                dbc.Col(
                    [html.Img(
                        # Link to UW seal
                        src='https://upload.wikimedia.org/wikipedia/commons/4/45/Seal_of_the_University_of_Wisconsin.svg',
                        style={'width':'30%'}
                    )],
                    style={'textAlign':'center'}
                )
            ])
    ]
)

########################################################################
####                                                                ####
####                             Modal                              ####
####                                                                ####
########################################################################
info_page = dbc.Modal(
    [
        dbc.ModalHeader(
            "Information & Usage" # Header for the modal page
        ),
        info_page_content, # Modal Page content defined above in the layout section
        dbc.ModalFooter([
            # Buttons for the Info Page Modal Footer
            dbc.Button("Close", id="close-info-modal", className="ml-auto"),
        ]),
        html.Div(id="info-page-status")  # Placeholder for saving status
    ],
    id="info-page-modal",
    size="xl"
)