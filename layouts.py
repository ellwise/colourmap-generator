import dash_bootstrap_components as dbc

from components import (
    msg,
    store,
    swatch,
    ch_plane,
    lh_plane,
    lc_plane,
    lightness_picker,
    chroma_picker,
    hue_picker,
)


def make_layout():
    return dbc.Container(
        className="mt-3 mb-3",
        children=dbc.Row(
            [
                dbc.Col(
                    children=[
                        msg,
                        store,
                        swatch,
                        dbc.Row(
                            [
                                dbc.Col([lightness_picker, ch_plane]),
                                dbc.Col([chroma_picker, lh_plane]),
                                dbc.Col([hue_picker, lc_plane]),
                            ]
                        ),
                    ],
                ),
            ]
        ),
    )
