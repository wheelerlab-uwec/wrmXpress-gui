import time
import dash
from dash import html
from dash.long_callback import DiskcacheLongCallbackManager
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

## Diskcache
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

dash.register_page(__name__, long_callback_manager=long_callback_manager)

layout = html.Div(
    [
        html.Div(
            [
                html.P(id="paragraph_id", children=["Button not clicked"]),
                dbc.Progress(id="progress_bar", color = 'success', striped = True, animated = True),
                html.P(id="progress_bar_text", children=["Progress Bar Text"]),
            ]
        ),
        dbc.Button(id="button_id", children="Run Job!", color = 'success'),
        dbc.Button(id="cancel_button_id", children="Cancel Running Job!", color = 'danger'),
    ]
)