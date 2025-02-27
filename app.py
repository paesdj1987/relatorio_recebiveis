#app.py
from dash import Dash
from layout import create_layout
import callbacks
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],  
    assets_folder='assets'  
)
app.title = "CRM - Junix"
app.layout = create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port='8053')
