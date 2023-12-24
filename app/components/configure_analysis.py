########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import dash_bootstrap_components as dbc

# Importing Components
from app.components.instrument_settings import instrument_settings
from app.components.worm_information import worm_information
from app.components.module_selection import module_selection
from app.components.run_time_settings import run_time_settings


########################################################################
####                                                                ####
####                             Layout                             ####
####                                                                ####
########################################################################
configure_analysis = dbc.Container([
            dbc.Accordion(
                [
                    # Order of the Accordian item in which they appear in the app
                    instrument_settings,
                    worm_information,
                    module_selection,
                    run_time_settings,
                ],
                start_collapsed=False,
                always_open=True,
            ),
        ],
        style={"paddingTop":"150px"})