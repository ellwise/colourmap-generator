import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import SWATCH_SIZE, PICKER_SIZE

msg_controls = html.P(
    className="text-justify",
    children="""
        Specify each colour within HSL-space.
        These colours all transform to points within RGB-space, so we can be sure they can be represented in CSS.
        Note that hue and lightness are not perfectly equivalent in HSL-space and LCH-space, but they are related.
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
            value=100 / PICKER_SIZE,
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
    children=dcc.Slider(id="slider-hue", min=0, max=1, step=0.01, value=0.5),
)
hue_picker = dbc.FormGroup(
    [hue_label, hue_progress, hue_slider, html.Div(style={"marginTop": "-30px"})]
)

saturation_label = dbc.Label("Saturation", html_for="bar-saturation")
saturation_progress = dbc.Progress(
    className="mb-1",
    id="bar-saturation",
    multi=True,
    children=[
        dbc.Progress(
            id={"class": "bar-saturation", "index": j},
            value=100 / PICKER_SIZE,
            bar=True,
            animated=False,
        )
        for j in range(PICKER_SIZE)
    ],
)
saturation_slider = html.Div(
    style={
        "marginLeft": "-25px",
        "marginRight": "-25px",
    },  # counter the slider's left/right padding
    children=dcc.Slider(id="slider-saturation", min=0, max=1, step=0.01, value=0.5),
)
saturation_picker = dbc.FormGroup(
    [
        saturation_label,
        saturation_progress,
        saturation_slider,
        html.Div(style={"marginTop": "-30px"}),
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
            value=100 / PICKER_SIZE,
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
    children=dcc.Slider(id="slider-lightness", min=0, max=1, step=0.01, value=0.5),
)
lightness_picker = dbc.FormGroup(
    [
        lightness_label,
        lightness_progress,
        lightness_slider,
        html.Div(style={"marginTop": "-30px"}),
    ]
)
pickers = html.Div([hue_picker, saturation_picker, lightness_picker])

store = dcc.Store(id="store", data={j: None for j in range(SWATCH_SIZE)})

msg_outputs = html.P(
    className="text-justify",
    children="""
        The output color swatch is given as hex-codes for easy use in applications.
        It is also plotted within LCH-space, to help with designing colour maps for data visualisation.
        For instance, a linear colourmap could be designed with a constant chroma/hue, and linearly changing lightness.
        It also could be designed with a constant lightness/hue, but linearly changing hue.
    """,
)

kwargs = {
    "className": "mb-1",
    "style": {"height": "25vh"},
    "config": {"staticPlot": True},
}
graph_l = dcc.Graph(id="graph-l", **kwargs)
graph_c = dcc.Graph(id="graph-c", **kwargs)
graph_h = dcc.Graph(id="graph-h", **kwargs)
graphs = html.Div(
    [
        html.Div("Lightness"),
        graph_l,
        html.Div("Chroma"),
        graph_c,
        html.Div("Hue"),
        graph_h,
    ]
)

label_swatch = dbc.Label("Swatch", html_for="slider")
progress_swatch_top = dbc.Progress(
    className="mb-1",
    multi=True,
    children=[
        dbc.Progress(
            id={"class": "swatch-light", "index": j},
            value=100 / SWATCH_SIZE,
            bar=True,
            animated=False,
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
            value=100 / SWATCH_SIZE,
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
            max=9,
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
            children="Select the active swatch element",
        ),
    ]
)
