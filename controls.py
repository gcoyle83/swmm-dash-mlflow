import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_daq as daq

sliders =  html.Div(
                [
                    html.H5("Orifice Controls"),
                    "Drag the sliders to adjust the percent-open fraction of the orifice controls.",
                    html.Hr(), # horizontal line
                    "Percent open if depth at Junction 2 exceeds 4.5 feet:",
                    dcc.Slider(min=0.0, max=1.0, step=0.1, value=1.0, id='orifice1',className="dcc_control"),
                    # html.Hr(), # horizontal line
                    "Percent open if depth at Junction 2 less than 4.0 feet:",
                    dcc.Slider(min=0.0, max=1.0, step=0.1, value=0.25, id='orifice2',className="dcc_control"),
                    # html.Hr(), # horizontal line
                    "Percent open if depth at Junction 2 less than 2.0 feet:",
                    dcc.Slider(min=0.0, max=1.0, step=0.1, value=0.15, id='orifice3',className="dcc_control"),
                    # html.Hr(), # horizontal line
                ],
                id='slider_div',
                style={"display": "flex", "flex-direction": "column", "margin-bottom": "10px"}
            )
nodes = html.Div(
    [
        "Select nodes to view:",
        dcc.Dropdown(
            id='nodes-dropdown',
            options = [
                {'label': 'Flooding at J1', 'value': 'J1'},
                {'label': 'Cumulative inflows at J8', 'value': 'J8'},
                {'label': 'Cumulative inflows at OF1', 'value': 'OF1'},
                {'label': 'Cumulative inflows at OF2', 'value': 'OF2'},
                {'label': 'Cumulative inflows at OF3', 'value': 'OF3'},
            ],
            value=['J1'],
            multi=True
        )
    ],
    id='nodes_div',
    style={"display": "flex", "flex-direction": "column", "margin-bottom": "5px"}
)
rainfall = html.Div(
    [
        daq.BooleanSwitch(id='rain-switch', on=False, label="Generate new rainfall?")
    ],
    id='rainfall_div',
    style={"display": "flex", "flex-direction": "column", "margin-bottom": "5px"}
)
run = html.Div(
    [
        dbc.Button("Run Simulation",id="run-button",n_clicks=0)
    ],
    id='run_div',
    style={"display": "flex", "flex-direction": "column", "margin-bottom": "10px"}
)

controls = dbc.Card(
    id='control-card',
    children=[
        sliders,
        rainfall,
        run
    ],
    body=True,
)