from app import app
from layouts import make_layout

# important to have callbacks import after layouts
import callbacks  # noqa: F401

app.title = "Colourmap Generator"
app.layout = make_layout()

server = app.server  # zappa uses this variable for deployment

if __name__ == "__main__":
    app.run_server(debug=False)
