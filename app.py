# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from layout import create_layout as create_crm_layout
import callbacks                
from dashboard import create_dashboard_layout
import dashboard_callbacks      

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True  
)
app.title = "CRM - Junix"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),            
    dcc.Store(id='filtered-data', storage_type='session'),  
    html.Div(id='page-content')                       
])

dashboard_callbacks.register_dashboard_callbacks(app)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/dashboards':
        return create_dashboard_layout()
    return create_crm_layout(app)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8053)
