import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from dash import html
from controls import nodes

theme_button = html.Div(
            [
                ThemeChangerAIO(
                    aio_id="theme",
                    radio_props={"value":dbc.themes.LUX},
                    button_props={"className": "bg-primary text-white p-2 mb-2 text-center"}
                ),
            ],
        )
app_title = html.H4(
    "SWMM Operations Dashboard", 
    className="bg-primary text-white p-2 mb-2 text-center"
)
learn_button = html.Div(
            [
                dbc.Button(
                    "Learn More",
                    href="https://plot.ly/dash/pricing/",
                    id="learn-button",
                    n_clicks=0
                )
            ],
        )
header = dbc.Row(
            [
                dbc.Col([theme_button], width=2, className="bg-primary text-white p-2 mb-2 text-center"),
                dbc.Col([app_title], width=8, className="bg-primary text-white p-2 mb-2 text-center"),
                dbc.Col([learn_button], width=2, className="bg-primary text-white p-2 mb-2 text-center")
            ]
        )

# tabs
tab0_output = html.Div(
    title="Simulated Flows", 
    id='tab0-output-state',
    children=[],
    className="mb-4",
)
# tab1_output = html.Div(
#     title="System Map", 
#     id='tab1-output-state',
#     children=[],
#     className="mb-4",
# )
tab2_output = html.Div(
    title="System Profile", 
    id='tab2-output-state',
    children=[],
    className="mb-4",
)

tab0 = dbc.Tab([nodes, html.Div(id="flows-container",className="mb-4"), tab0_output], label="Simulated Flows")
# tab1 = dbc.Tab([html.Div(id="map-container",className="mb-4"), tab1_output], label="System Map")
tab2 = dbc.Tab([html.Div(id="profile-container",className="mb-4"), tab2_output], label="System Profile")
tabs = dbc.Card(dbc.Tabs(
    [
        tab0,   
        # tab1,
        tab2,
    ]
))