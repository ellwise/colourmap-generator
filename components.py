import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np

from app import SWATCH_SIZE, PICKER_SIZE


msg = html.P(
    className="text-justify",
    children="""
        To create good colourmaps for data visualisations, it's important to
        consider the way colours are perceived. The lightness-chroma-hue
        (LCH) colourspace is a good choice for doing so. Below, you can create
        a swatch of colours by choosing values in LCH-space that map to valid
        red-green-blue (RGB) colours. By valid, we mean that they are
        commonly supported, e.g. within CSS. Typically, a colourmap should aim
        to hold some LCH channels constant, and linearly transition through
        others. For instance, the chroma and hue might be constant, and the
        lightness linearly changing.
    """,
)

hue_label = dbc.Label("Hue", html_for="bar-hue")
hue_progress = dbc.Progress(
    className="mb-1",
    id="bar-hue",
    multi=True,
    children=[
        dbc.Progress(
            id={"class": "bar-hue", "index": j},
            style={"width": f"{100 / PICKER_SIZE}%"},
            bar=True,
            animated=False,
        )
        for j in range(PICKER_SIZE)
    ],
)
hue_slider = html.Div(
    style={
        "marginLeft": "-25px",
        "marginRight": "-25px",
    },  # counter the slider's left/right padding
    children=dcc.Slider(
        id="slider-hue",
        min=0,
        max=2 * np.pi,
        step=np.pi / 180,
        value=np.pi,
        marks={
            0: "0",
            np.pi / 2: "90",
            np.pi: "180",
            3 * np.pi / 2: "270",
            2 * np.pi: "360",
        },
    ),
)
hue_picker = dbc.FormGroup(
    [
        hue_label,
        hue_progress,
        hue_slider,
        html.Div(style={"marginTop": "-10px"}),
    ]
)

chroma_label = dbc.Label("Chroma", html_for="bar-chroma")
chroma_progress = dbc.Progress(
    className="mb-1",
    id="bar-chroma",
    multi=True,
    children=[
        dbc.Progress(
            id={"class": "bar-chroma", "index": j},
            style={"width": f"{100 / PICKER_SIZE}%"},
            bar=True,
            animated=False,
        )
        for j in range(PICKER_SIZE)
    ],
)
chroma_slider = html.Div(
    style={
        "marginLeft": "-25px",
        "marginRight": "-25px",
    },  # counter the slider's left/right padding
    children=dcc.Slider(
        id="slider-chroma",
        min=0,
        max=136,
        step=1,
        value=68,
        marks={j: f"{j}" for j in [0, 34, 68, 102, 136]},
    ),
)
chroma_picker = dbc.FormGroup(
    [
        chroma_label,
        chroma_progress,
        chroma_slider,
        html.Div(style={"marginTop": "-10px"}),
    ]
)

lightness_label = dbc.Label("Lightness", html_for="bar-lightness")
lightness_progress = dbc.Progress(
    className="mb-1",
    id="bar-lightness",
    multi=True,
    children=[
        dbc.Progress(
            id={"class": "bar-lightness", "index": j},
            style={"width": f"{100 / PICKER_SIZE}%"},
            bar=True,
            animated=False,
        )
        for j in range(PICKER_SIZE)
    ],
)
lightness_slider = html.Div(
    style={
        "marginLeft": "-25px",
        "marginRight": "-25px",
    },  # counter the slider's left/right padding
    children=dcc.Slider(
        id="slider-lightness",
        min=0,
        max=100,
        step=1,
        value=50,
        marks={j: f"{j}" for j in [0, 25, 50, 75, 100]},
    ),
)
lightness_picker = dbc.FormGroup(
    [
        lightness_label,
        lightness_progress,
        lightness_slider,
        html.Div(style={"marginTop": "-10px"}),
    ]
)

store = dcc.Store(id="store", data={j: None for j in range(SWATCH_SIZE)})

label_swatch = dbc.Label("Swatch", html_for="slider")
progress_swatch_top = dbc.Progress(
    className="mb-1",
    multi=True,
    children=[
        dbc.Progress(
            id={"class": "swatch-light", "index": j},
            style={"width": f"{100 / SWATCH_SIZE}%"},
            bar=True,
        )
        for j in range(SWATCH_SIZE)
    ],
)
progress_swatch_bottom = dbc.Progress(
    className="mb-1",
    multi=True,
    children=[
        dbc.Progress(
            id={"class": "swatch-dark", "index": j},
            style={"width": f"{100 / SWATCH_SIZE}%"},
            bar=True,
            animated=False,
            color="#808080",
        )
        for j in range(SWATCH_SIZE)
    ],
)
slider_swatch = html.Div(
    style={
        "marginLeft": "-25px",
        "marginRight": "-25px",
    },  # counter the slider's left/right padding
    children=html.Div(
        style={
            "marginLeft": "5%",
            "marginRight": "5%",
        },  # ensure marks align with the progress bars
        children=dcc.Slider(
            id="slider-swatch",
            min=0,
            max=8,
            step=1,
            value=0,
            marks={j: "" for j in range(10)},
            included=False,
        ),
    ),
)
swatch = dbc.FormGroup(
    [
        label_swatch,
        progress_swatch_top,
        progress_swatch_bottom,
        slider_swatch,
        dbc.FormText(
            style={
                "marginTop": "-20px"
            },  # (partially) counter the slider's bottom padding
            children="Use the slider above activate a swatch element",
        ),
    ]
)

kwargs = {
    "className": "mb-1",
    "style": {"height": "50vh"},
    "config": {"staticPlot": True},
}
ch_plane = dcc.Graph(id="graph-ch", **kwargs)
lh_plane = dcc.Graph(id="graph-lh", **kwargs)
lc_plane = dcc.Graph(id="graph-lc", **kwargs)
