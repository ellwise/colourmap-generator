import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from components import msg_controls, pickers, store, msg_outputs, swatch, graphs


layout = dbc.Container(
    className="mt-3 mb-3",
    children=dbc.Row(
        [
            dbc.Col(
                children=[
                    msg_controls,
                    pickers,
                    store,
                ],
                width=3,
            ),
            dbc.Col(
                children=[
                    msg_outputs,
                    swatch,
                    graphs,
                ],
                width=9,
            ),
        ]
    ),
)
