########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################

import dash_bootstrap_components as dbc
from dash import html

# Importing Components and functions
from app.components.instrument_settings import instrument_settings
from app.components.worm_information import worm_information
from app.components.module_selection import module_selection
from app.components.run_time_settings import run_time_settings

########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################

configure_layout = dbc.Container([
    dbc.Accordion(
        [
            # Order of the Accordian item in which they appear in the app
            instrument_settings,  # Instrument settings, see instrument_settings.py
            worm_information,  # Worm information, see worm_information.py
            module_selection,  # Module selection, see module_selection.py
            run_time_settings,  # Run time settings, see run_time_settings.py
        ],
        start_collapsed=False,  # Start with the accordian open
        always_open=True,  # Always open the accordian
        id="configure-accordion",  # ID of the accordian
    ),
    html.Hr(),
    dbc.Alert(
        id='resolving-error-issue-configure',
        is_open=False,  # Alert is not open by default
        color='danger',  # Alert color is red
        duration=10000  # Alert will close after 10 seconds
    ),
    html.Br(),
    # Button to finalize configuration
    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Finalize configuration",  # Button text
                    id="finalize-configure-button",
                    className="flex",  # Button class is flex
                    color='primary'  # Default button color is (wrmXpress) blue
                ),
                width="auto"  # Button width is auto
            ),
        ],
        justify="center"  # Center the button
    ),
],
    # Adjust the white space between tab and accordian elements
    style={"paddingTop": "80px"}
)