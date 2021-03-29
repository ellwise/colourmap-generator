import colorsys

from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_html_components as html
from colormath.color_objects import sRGBColor, LCHuvColor, HSLColor
from colormath.color_conversions import convert_color
import pandas as pd
import plotly.express as px

from app import app, PICKER_SIZE


@app.callback(
    Output("store", "data"),
    [
        Input("slider-hue", "value"),
        Input("slider-saturation", "value"),
        Input("slider-lightness", "value"),
    ],
    [State("slider-swatch", "value"), State("store", "data")],
)
def update_store(hue, saturation, lightness, value, data):
    k = str(value)
    if not data[k]:
        data[k] = {}
    hsl_colour = HSLColor(360 * hue, saturation, lightness)
    rgb_colour = convert_color(hsl_colour, sRGBColor)

    hex_colour = "#" + "".join(
        f"{int(j * 255):02x}" for j in rgb_colour.get_value_tuple()
    )
    lch_colour = convert_color(hsl_colour, LCHuvColor)

    data[k]["hsl"] = hsl_colour.get_value_tuple()
    data[k]["hex"] = hex_colour
    data[k]["lch"] = lch_colour.get_value_tuple()
    return data


@app.callback(
    [
        Output("slider-hue", "value"),
        Output("slider-saturation", "value"),
        Output("slider-lightness", "value"),
    ],
    Input("slider-swatch", "value"),
    State("store", "data"),
)
def update_colour_picker(value, data):
    if data[str(value)]:
        h, s, l = data[str(value)]["hsl"]
        h = h / 360
        return h, s, l
    else:
        return 0.5, 0.5, 0.5


@app.callback(
    [
        Output("graph-l", "figure"),
        Output("graph-c", "figure"),
        Output("graph-h", "figure"),
    ],
    Input("store", "data"),
)
def update_graphs(data):
    x_values = [int(x) for x in data.keys()]
    l_values = [v["lch"][0] if v else None for v in data.values()]
    c_values = [v["lch"][1] if v else None for v in data.values()]
    h_values = [v["lch"][2] if v else None for v in data.values()]
    hex_values = [v["hex"] if v else None for v in data.values()]

    df = pd.DataFrame(
        {
            "Colour": x_values,
            "Hex": hex_values,
            "Lightness": l_values,
            "Chroma": c_values,
            "Hue": h_values,
        }
    )
    df["Hex"] = df["Hex"].fillna("")

    kwargs = {
        "data_frame": df,
        "x": "Colour",
        "color": "Hex",
        "color_discrete_map": {hex: hex for hex in hex_values},
        "template": "plotly_dark",
    }
    figs = [
        px.scatter(
            y="Lightness",
            range_y=[0, 1.1 * df["Lightness"].max()],
            **kwargs,
        ),
        px.scatter(
            y="Chroma",
            range_y=[0, 1.1 * df["Chroma"].max()],
            **kwargs,
        ),
        px.scatter(
            y="Hue",
            range_y=[0, 360],
            **kwargs,
        ),
    ]
    for fig in figs:
        kwargs = {
            "showgrid": False,  # thin lines in the background
            "zeroline": False,  # thick line at x=0
            "visible": False,  # numbers below
        }
        fig.update_xaxes(**kwargs)
        fig.update_yaxes(**kwargs)
        fig.update_layout(
            {
                "margin": dict(l=0, r=0, t=0, b=0),
                "showlegend": False,
            }
        )
        fig.update_traces(
            marker_size=12,  # same as slider handle minus marker_line_width
            marker_line_color="#adb5bd",  # colour from DARKLY theme
            marker_line_width=2,
        )
    return figs


@app.callback(
    [
        Output({"class": "swatch-light", "index": MATCH}, "color"),
        Output({"class": "swatch-dark", "index": MATCH}, "color"),
        Output({"class": "swatch-light", "index": MATCH}, "children"),
        Output({"class": "swatch-dark", "index": MATCH}, "children"),
    ],
    Input("store", "data"),
    State({"class": "swatch-light", "index": MATCH}, "id"),
)
def update_block_bg(data, id):
    k = str(id["index"])
    value = data[k]["hex"] if data[k] else None

    label = value if value else ""
    label_light = html.Div(label, style={"color": "white"})
    label_dark = html.Div(label, style={"color": "black"})

    return value, value, label_light, label_dark


@app.callback(
    Output({"class": "bar-hue", "index": ALL}, "color"),
    [
        Input({"class": "bar-hue", "index": ALL}, "id"),
        Input("slider-saturation", "value"),
        Input("slider-lightness", "value"),
    ],
)
def update_bar_hue(ids, saturation, lightness):
    hues = [id["index"] / (PICKER_SIZE - 1) for id in ids]
    rgbs = [colorsys.hls_to_rgb(hue, lightness, saturation) for hue in hues]
    return ["#" + "".join(f"{int(j * 255):02x}" for j in rgb) for rgb in rgbs]


@app.callback(
    Output({"class": "bar-saturation", "index": ALL}, "color"),
    [
        Input({"class": "bar-saturation", "index": ALL}, "id"),
        Input("slider-hue", "value"),
        Input("slider-lightness", "value"),
    ],
)
def update_bar_hue(ids, hue, lightness):
    saturations = [id["index"] / (PICKER_SIZE - 1) for id in ids]
    rgbs = [
        colorsys.hls_to_rgb(hue, lightness, saturation) for saturation in saturations
    ]
    return ["#" + "".join(f"{int(j * 255):02x}" for j in rgb) for rgb in rgbs]


@app.callback(
    Output({"class": "bar-lightness", "index": ALL}, "color"),
    [
        Input({"class": "bar-lightness", "index": ALL}, "id"),
        Input("slider-hue", "value"),
        Input("slider-saturation", "value"),
    ],
)
def update_bar_hue(ids, hue, saturation):
    lightnesses = [id["index"] / (PICKER_SIZE - 1) for id in ids]
    rgbs = [
        colorsys.hls_to_rgb(hue, lightness, saturation) for lightness in lightnesses
    ]
    return ["#" + "".join(f"{int(j * 255):02x}" for j in rgb) for rgb in rgbs]
