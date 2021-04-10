from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_html_components as html
import plotly.express as px
import numpy as np
from skimage.color import lch2lab, lab2rgb, rgb2lab, lab2lch

from app import app, PICKER_SIZE


def lch2rgb(colour):
    return lab2rgb(lch2lab(colour))


def rgb2lch(colour):
    return lab2lch(rgb2lab(colour))


# from 1010-1018 of colorconv.py in skimage.color
def outside_gamut(lch):
    lab = lch2lab(lch)
    L, _, b = lab[..., 0], lab[..., 1], lab[..., 2]
    y = (L + 16.0) / 116.0
    z = y - (b / 200.0)
    invalid = np.nonzero(z < 0)
    return invalid


@app.callback(
    Output("store", "data"),
    [
        Input("slider-hue", "value"),
        Input("slider-chroma", "value"),
        Input("slider-lightness", "value"),
    ],
    [State("slider-swatch", "value"), State("store", "data")],
)
def update_store(hue, chroma, lightness, value, data):
    k = str(value)
    if not data[k]:
        data[k] = {}
    lch = np.array([[lightness, chroma, hue]])
    rgb = lch2rgb(lch)
    invalid = outside_gamut(lch)
    rgb[invalid] = None

    hex_colour = (
        "#" + "".join(f"{int(j * 255):02x}" for j in rgb[0])
        if not np.isnan(rgb[0]).any()
        else None
    )

    data[k]["hex"] = hex_colour
    data[k]["lch"] = lch[0]
    return data


@app.callback(
    [
        Output("slider-lightness", "value"),
        Output("slider-chroma", "value"),
        Output("slider-hue", "value"),
    ],
    Input("slider-swatch", "value"),
    [
        State("store", "data"),
        State("slider-lightness", "value"),
        State("slider-chroma", "value"),
        State("slider-hue", "value"),
    ],
)
def update_colour_picker(value, data, lightness, chroma, hue):
    if data[str(value)]:
        lightness, chroma, hue = data[str(value)]["lch"]
    return lightness, chroma, hue


@app.callback(
    [
        Output({"class": "swatch-light", "index": MATCH}, "style"),
        Output({"class": "swatch-dark", "index": MATCH}, "style"),
        Output({"class": "swatch-light", "index": MATCH}, "children"),
        Output({"class": "swatch-dark", "index": MATCH}, "children"),
    ],
    Input("store", "data"),
    [State({"class": "swatch-light", "index": MATCH}, "id"),
    State({"class": "swatch-light", "index": MATCH}, "style"),
    State({"class": "swatch-dark", "index": MATCH}, "style")],
)
def update_block_bg(data, id, style_light, style_dark):
    k = str(id["index"])
    colour = data[k]["hex"] if data[k] else None

    label = colour if colour else ""
    label_light = html.Div(label, style={"color": "white"})
    label_dark = html.Div(label, style={"color": "black"})

    style_light["backgroundColor"] = colour
    style_dark["backgroundColor"] = colour

    return style_light, style_dark, label_light, label_dark


@app.callback(
    Output({"class": "bar-hue", "index": ALL}, "style"),
    [
        Input({"class": "bar-hue", "index": ALL}, "id"),
        Input("slider-chroma", "value"),
        Input("slider-lightness", "value"),
    ],
    State({"class": "bar-hue", "index": ALL}, "style"),
)
def update_bar_hue(ids, chroma, lightness, styles):
    hues = [id["index"] * 2 * np.pi / (PICKER_SIZE - 1) for id in ids]
    lch = [[lightness, chroma, hue] for hue in hues]
    rgb = lch2rgb(lch)
    invalid = outside_gamut(lch)
    rgb[invalid] = None
    colours = [
        "#" + "".join(f"{int(j * 255):02x}" for j in colour)
        if not np.isnan(colour).any()
        else ""
        for colour in rgb
    ]
    return [{**style, "backgroundColor": colour} for style, colour in zip(styles, colours)]


@app.callback(
    Output({"class": "bar-chroma", "index": ALL}, "style"),
    [
        Input({"class": "bar-chroma", "index": ALL}, "id"),
        Input("slider-hue", "value"),
        Input("slider-lightness", "value"),
    ],
    State({"class": "bar-chroma", "index": ALL}, "style"),
)
def update_bar_chroma(ids, hue, lightness, styles):
    chromas = [id["index"] * 136 / (PICKER_SIZE - 1) for id in ids]
    lch = [[lightness, chroma, hue] for chroma in chromas]
    rgb = lch2rgb(lch)
    invalid = outside_gamut(lch)
    rgb[invalid] = None
    colours = [
        "#" + "".join(f"{int(j * 255):02x}" for j in colour)
        if not np.isnan(colour).any()
        else ""
        for colour in rgb
    ]
    return [{**style, "backgroundColor": colour} for style, colour in zip(styles, colours)]


@app.callback(
    Output({"class": "bar-lightness", "index": ALL}, "style"),
    [
        Input({"class": "bar-lightness", "index": ALL}, "id"),
        Input("slider-hue", "value"),
        Input("slider-chroma", "value"),
    ],
    State({"class": "bar-lightness", "index": ALL}, "style"),
)
def update_bar_lightness(ids, hue, chroma, styles):
    lightnesses = [id["index"] * 100 / (PICKER_SIZE - 1) for id in ids]
    lch = [[lightness, chroma, hue] for lightness in lightnesses]
    rgb = lch2rgb(lch)
    invalid = outside_gamut(lch)
    rgb[invalid] = None
    colours = [
        "#" + "".join(f"{int(j * 255):02x}" for j in colour)
        if not np.isnan(colour).any()
        else ""
        for colour in rgb
    ]
    return [{**style, "backgroundColor": colour} for style, colour in zip(styles, colours)]


@app.callback(
    Output("graph-ch", "figure"),
    [
        Input("slider-lightness", "value"),
        Input("slider-chroma", "value"),
        Input("slider-hue", "value"),
    ],
)
def update_ch_plane(lightness, chroma, hue):
    cs = np.linspace(0, 136, num=137)
    hs = np.linspace(0, 2 * np.pi, num=361)
    lch = np.array([[[lightness, chroma, hue] for chroma in cs] for hue in hs])
    rgb = lch2rgb(lch)
    invalid = outside_gamut(lch)
    rgb[invalid] = None
    fig = px.imshow(
        img=rgb,
        x=cs,
        y=hs * 180 / np.pi,
        labels={"x": "Chroma", "y": "Hue"},
        aspect="auto",
        template="plotly_dark",
    )
    fig.add_hline(y=hue * 180 / np.pi)
    fig.add_vline(x=chroma)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig


@app.callback(
    Output("graph-lh", "figure"),
    [
        Input("slider-lightness", "value"),
        Input("slider-chroma", "value"),
        Input("slider-hue", "value"),
    ],
)
def update_lh_plane(lightness, chroma, hue):
    chroma = chroma
    ls = np.linspace(0, 100, num=101)
    hs = np.linspace(0, 2 * np.pi, num=361)
    lch = np.array(
        [[[lightness, chroma, hue] for lightness in ls] for hue in hs]
    )
    rgb = lch2rgb(lch)
    invalid = outside_gamut(lch)
    rgb[invalid] = None
    fig = px.imshow(
        img=rgb,
        x=ls,
        y=hs * 180 / np.pi,
        labels={"x": "Lightness", "y": "Hue"},
        aspect="auto",
        template="plotly_dark",
    )
    fig.add_hline(y=hue * 180 / np.pi)
    fig.add_vline(x=lightness)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig


@app.callback(
    Output("graph-lc", "figure"),
    [
        Input("slider-lightness", "value"),
        Input("slider-chroma", "value"),
        Input("slider-hue", "value"),
    ],
)
def update_lc_plane(lightness, chroma, hue):
    ls = np.linspace(0, 100, num=101)
    cs = np.linspace(0, 136, num=137)
    lch = np.array(
        [[[lightness, chroma, hue] for lightness in ls] for chroma in cs]
    )
    rgb = lch2rgb(lch)
    invalid = outside_gamut(lch)
    rgb[invalid] = None
    fig = px.imshow(
        img=rgb,
        x=ls,
        y=cs,
        labels={"x": "Lightness", "y": "Chroma"},
        # aspect="auto",
        template="plotly_dark",
    )
    fig.add_hline(y=chroma)
    fig.add_vline(x=lightness)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig
