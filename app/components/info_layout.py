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

info_layout = [
    html.H4("Information"),
    # Introduction to wrmXpress
    html.P(
        "wrmXpress is a unified framework for the analysis of diverse phenotypic imaging data in "
        "high-throughput and high-content experiments involving free-living and parasitic nematodes "
        "and flatworms. This GUI is designed to be a user-friendly option for running analyses on a smaller scale. "
        "For large scale experiments, we recommend running wrmXpress on a "
        "high-performance or high-throughput computer cluster."
    ),
    html.Br(),
    html.H4("Usage"),
    dcc.Markdown(
        """
        To configure and run analyses, use the navigation column at left-hand side of the screen.

        1. **Configure** allows you to select relevant experimental and imaging parameters, as well as select the pipeline that you wish to run. Note that some selections will clash and be disallowed - you should see relevant warnings/errors if so.
        2. **Metadata** allows you to include well-based metadata. Each metadata type (i.e., concentration, treatment, time point, etc.) will be saved in a separate CSV with the same numbers of rows/columns selected in Configure.
        Custom metadata types can be added. Metadata will be merged with raw output after completing the analysis. Metadata is not required for a pipeline to run. 
        3. **Preview** will allow you to preview the ouptput of the pipeline's analysis on well A01. Note that the preview step will fail if well A01 is empty. 
        4. **Run** is where the final pipeline will be run on all of the selected wells. Logs are written dynamically to the screen but also to the working directory.,
        """
    ),
    html.Br(),
    html.H4("The Developers"),
    dcc.Markdown(
        """
        wrmXpress is entirely open-source. The code for the back-end is maintained by the [Zamanian Lab](https://www.zamanianlab.org/) at the University of Wisconsin-Madison and can be found [here](https://github.com/zamanianlab/wrmXpress).
        The code for the front-end is maintained by the [Wheeler Lab](https://wheelerlab.bio/) at the University of Wisconsin-Eau Claire and can be found [here](https://github.com/wheelerlab-uwec/wrmXpress-gui). To receive support for either
        the GUI or running wrmXpress remotely, please submit a GitHub Issue at the relevent linked repositories.
        """
    ),
    html.Br(),
    # logos row
    dbc.Row(
        [
            dbc.Col(
                [
                    html.A(
                        html.Img(
                            src="assets/wheeler_logo.png",
                            style={"width": "50%"},
                        ),
                        href="https://wheelerlab.bio",
                        target="_blank",
                    )
                ]
            ),
            dbc.Col(
                [
                    html.A(
                        html.Img(
                            src="assets/madison_mark.svg",
                            style={"width": "50%"},
                        ),
                        href="https://wisc.edu",
                        target="_blank",
                    )
                ]
            ),
        ],
        style={"textAlign": "center"},
    ),
    html.Br(),
    # campus photo row
    dbc.Row(
        [
            dbc.Col(
                [
                    html.A(
                        html.Img(
                            src="assets/ec_aerial.jpg",
                            style={"width": "100%"},
                        ),
                        href="https://uwec.edu",
                        target="_blank",
                    )
                ]
            ),
            dbc.Col(
                [
                    html.A(
                        html.Img(
                            src="assets/madison_aerial.jpg",
                            style={"width": "100%"},
                        ),
                        href="https://wisc.edu",
                        target="_blank",
                    )
                ]
            ),
        ]
    ),
]

#     dbc.Row(
#         [
#             dbc.Col(
#                 dbc.Row(
#                 ),
#                 dbc.Row(
#                 dbc.Col(
#                 [
#                     html.A(
#                         html.Img(
#                             src="assets/UWEC_Mark__UWEC_stckd_Old-Gold.svg",
#                             style={"width": "30%"},
#                         ),
#                         href="https://www.uwec.edu/",
#                         target="_blank",  # Opens the link in a new tab
#                     )
#                 ],
#                 style={"textAlign": "center"},
#             ),
#             dbc.Col(
#                 [
#                     html.A(
#                         html.Img(
#                             src="https://assets.super.so/6d48c8d3-6e72-45c3-a5b9-04514883421e/images/9da71b53-e8f2-4234-9e55-e50d302f5c46/Lab_logo.svg",
#                             style={"width": "30%"},
#                         ),
#                         href="https://wheelerlab.bio/",
#                         target="_blank",
#                     )
#                 ],
#                 style={"textAlign": "center"},
#                 )
#                 # [
#                 #     html.A(
#                 #         html.Img(
#                 #             src="https://assets.super.so/6d48c8d3-6e72-45c3-a5b9-04514883421e/images/9da71b53-e8f2-4234-9e55-e50d302f5c46/Lab_logo.svg",
#                 #             style={"width": "50%"},
#                 #         ),
#                 #         href="https://wheelerlab.bio/",
#                 #         target="_blank",  # Opens the link in a new tab
#                 #     ),
#                 # ],
#                 # style={"textAlign": "center"},
#             ))],

#             dbc.Col(
#                 [
#                     html.A(
#                         html.Img(
#                             src="https://upload.wikimedia.org/wikipedia/commons/4/45/Seal_of_the_University_of_Wisconsin.svg",
#                             style={"width": "40%"},
#                         ),
#                         href="https://www.wisc.edu/",
#                         target="_blank",  # Opens the link in a new tab
#                     )
#                 ],
#                 style={"textAlign": "center"},
#             ),
#         ]
#     ),
# ]
