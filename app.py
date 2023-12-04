from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# quant imports
import swmmio
import random
import numpy as np
# custom elements
from controls import controls
from components import header, tabs
from utils import (
    update_flows_figure,
    run_no_control,
    run_simple_control,
    system_profile,
    cleanup_swmm_artifacts
)
# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
dash_app = Dash(
    __name__,
    prevent_initial_callbacks=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
dash_app.title="MWE SWMM Dashboard"
app = dash_app.server # added for azure deployment

# app layout
dbc_components = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col([controls], width=4),
                dbc.Col([tabs], width=8)
            ]
        ),
    ],
    fluid=True,
    className="dbc"
)
dash_app.layout = html.Div(
    [
        # create storage for browser memory
        dcc.Store(id='swmm-output'),
        dbc_components
    ],
    className="dbc"
)

# Define callback to run simulation and update graph
@dash_app.callback(
    [# @app.callback(Output("loading-flows", "children"))
        # Output("loading-output-1", "children"),
        Output('swmm-output', 'data'),
        # Output('flows-container','children', allow_duplicate=True),
        Output("loading-flows",'children',allow_duplicate=True),
        Output('profile-container','children')
    ],
    Input('run-button','n_clicks'),
    State('rain-switch','on'),
    State('orifice1', 'value'),
    State('orifice2', 'value'),
    State('orifice3', 'value'),
    State('nodes-dropdown','value')
)
def run_swmm(n_clicks, rain, orifice1, orifice2, orifice3, plot_nodes):
    # get current model rainfall
    baseline = swmmio.Model('swmm_files/DemoModel.inp')

    if rain:
        base_rain = baseline.inp.timeseries.Value.values
        new_rain = np.array([random.expovariate(0.5)*float(i) for i in base_rain])
        baseline.inp.timeseries.Value = new_rain
        baseline.inp.save()

    # create new model input file
    # not really necessary in this example, but preserving the functionality
    basepath = 'swmm_files/DemoModel'
    filext = '.inp'
    newfp = basepath + 'controls' + filext
    baseline.inp.save(newfp)
    
    # run simulations
    baseline_run = run_no_control('swmm_files/DemoModel.inp')
    new_run = run_simple_control(newfp, orifice1, orifice2, orifice3)
    profile = system_profile(newfp)
    run_output = {
        'baseline': baseline_run,
        'new': new_run
    }
    flows = update_flows_figure(run_output, plot_nodes)
    # cleanup
    cleanup_swmm_artifacts(newfp)
    return run_output, flows, profile

# Define callback to update graph when node selection changes
@dash_app.callback(
    [
        Output('flows-container','children', allow_duplicate=True),
    ],
    Input('nodes-dropdown','value'),
    State('swmm-output', 'data'),
)
def update_nodes_plotted(plot_nodes, swmm_output):
    flows = update_flows_figure(swmm_output, plot_nodes)
    return [flows]

# Run app and display result inline in the notebook
# dash_app.run_server(debug=True)
# dash_app.run_server()

if __name__ == '__main__':
    dash_app.run_server(debug=False)