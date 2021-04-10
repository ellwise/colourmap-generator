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


col_kwargs = {"xs": 12, "sm": 12, "md": 12, "lg": 4, "xl": 4}


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
                                dbc.Col(
                                    children=[lightness_picker, ch_plane],
                                    **col_kwargs
                                ),
                                dbc.Col(
                                    children=[chroma_picker, lh_plane],
                                    **col_kwargs
                                ),
                                dbc.Col(
                                    children=[hue_picker, lc_plane],
                                    **col_kwargs
                                ),
                            ]
                        ),
                    ],
                ),
            ]
        ),
    )
