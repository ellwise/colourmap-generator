from app import app
from layouts import layout
import callbacks  # important to have this after layouts

app.title = "Colourmap Generator"
app.layout = layout

server = app.server  # zappa uses this variable for deployment

if __name__ == "__main__":
    app.run_server(debug=True)
