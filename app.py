import dash
import dash_bootstrap_components as dbc

SWATCH_SIZE = 9
PICKER_SIZE = 20

# some kwargs are needed for it to work with zappa - otherwise get js loading errors, DashRenderer not found, etc...
zappa_kwargs = {
    "compress": False,
    #'requests_pathname_prefix': '/production/', # this is needed if deployed without a domain mapping
    "serve_locally": False,
}

app = dash.Dash(
    __name__,
    title="Colourmap Generator",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],  # to improve mobile views
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    **zappa_kwargs,
)
