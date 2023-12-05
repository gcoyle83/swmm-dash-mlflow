import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from dash import html
from dash import dcc
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
about_btn = html.Div(
            [
                dbc.Button(
                    "About",
                    href="about.md",
                    id="about-button",
                    n_clicks=0
                )
            ],
        )
header = dbc.Row(
            [
                dbc.Col([theme_button], width=2, className="bg-primary text-white p-2 mb-2 text-center"),
                dbc.Col([app_title], width=8, className="bg-primary text-white p-2 mb-2 text-center"),
                dbc.Col([about_btn], width=2, className="bg-primary text-white p-2 mb-2 text-center")
            ]
        )

loading_flows = dcc.Loading(
    id = "loading-flows", 
    children=[html.Div(id='flows-container',className="mb-4")], 
    type="circle"
)
loading_profile = dcc.Loading(
    id = "loading-profile", 
    children=[html.Div(id='profile-container',className="mb-4")], 
    type="circle"
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

tab0 = dbc.Tab(
    [
        nodes,
        loading_flows,
        tab0_output
    ],
    label="Simulated Flows"
)
# tab1 = dbc.Tab([html.Div(id="map-container",className="mb-4"), tab1_output], label="System Map")
tab2 = dbc.Tab([loading_profile, tab2_output], label="System Profile")

tabs = dbc.Card(dbc.Tabs(
    [
        tab0,   
        # tab1,
        tab2,
    ]
))