import os
# viz imports
import plotly.graph_objects as go 
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
# quant imports
import pyswmm
import swmmio
from swmm.toolkit.shared_enum import NodeAttribute
import random
import pandas as pd
import numpy as np

# Build App
dash_app = Dash(__name__)
app = dash_app.server # added for azure deployment
dash_app.layout = html.Div([
    html.H1("MWE SWMM Dashboard",style={'textAlign': 'center', 'font-family': "Arial Narrow"}),
    html.P("Select a node to view flooding. Click the 'New Rainfall' button to generate simulation with new rainfall.",style={'textAlign': 'center', 'font-family': "Arial Narrow"}),
    dcc.RadioItems(['J1', 'J8', 'OF1', 'OF2', 'OF3'], 'J1', id='node-selection', inline=True, style={'font-family':"Arial Narrow"}),
    html.H3(id='figure-title',style={'textAlign': 'center','font-family': "Arial Narrow"}),
    dcc.Graph(id='graph'),
    html.Button(id='rain-button', n_clicks=0, children='New Rainfall')
])

# Define callback to update graph
@dash_app.callback(
    [Output('figure-title','children'),
     Output('graph', 'figure')
     ],
    Input('rain-button','n_clicks'),
    Input('node-selection', 'value')
)
def update_rain(n_clicks, node_value, file_cnt=2):

    # get current model rainfall
    baseline = swmmio.Model('swmm_files/DemoModel.inp')
    rain = baseline.inp.timeseries.Value.values

    # induce noise
    new_rain = np.array([random.expovariate(0.5)*float(i) for i in rain])
    baseline.inp.timeseries.Value = new_rain
    # save back to new model input file
    basepath = 'swmm_files/DemoModel'
    filext = '.inp'
    newfp = basepath + str(n_clicks+1) + filext
    baseline.inp.save(newfp)
    # construct name for new output file
    # newop = basepath+str(n_clicks+1)+'.out'
    # execute new simulation
    # with pyswmm.Simulation(newfp) as sim:
    #     sim.execute()
    ts_base, node_base = run_no_control('swmm_files/DemoModel.inp', node_value)
    ts_new, node_new = run_no_control(newfp, node_value, baseline=False)
    fig_title = "Flooding at {}".format(node_value)
    # return updated figure from new output file
    return fig_title, update_figure(node_value, ts_base, node_base, ts_new, node_new)

def update_figure(node, ts_base, node_base, ts_new, node_new):
    # import plotly.graph_objects as go

    fig = go.Figure()

    # trace baseline
    fig.add_trace(go.Line(x=ts_base,y=node_base,
                        mode='lines',
                        name='Baseline'))
    # trace new
    fig.add_trace(go.Line(x=ts_new,y=node_new,
                        mode='lines',
                        name='Latest'))
    fig.update_layout(transition_duration=50)
    return fig

def run_no_control(input_file, node, baseline=True):
    # print("Running the Model without Control")
    with pyswmm.Simulation(input_file) as sim:
        system_stats = pyswmm.SystemStats(sim)

        # Interceptor nodes to observe
        J1 = pyswmm.Nodes(sim)["J1"]

        # Overflows to Observe
        OF1 = pyswmm.Nodes(sim)["OF1"]
        OF2 = pyswmm.Nodes(sim)["OF2"]
        OF3 = pyswmm.Nodes(sim)["OF3"]
        J8 = pyswmm.Nodes(sim)["J8"]

        # dict for node selection
        nodes = {
            "J1": J1,
            "OF1": OF1,
            "OF2": OF2,
            "OF3": OF3,
            "J8": J8
        }

        # Initializing Data Arrays for timeseries plot
        ts_no_control=[]
        flooding_no_control=[]

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            ts_no_control.append(sim.current_time)
            flooding_no_control.append(nodes.get(node).flooding)
            pass
        # Get Results for Post Processing Table
        # no_control_J8 = J8.cumulative_inflow
        # no_control_total_overflow = OF1.cumulative_inflow \
        #                         + OF2.cumulative_inflow \
        #                         + OF3.cumulative_inflow
        # no_controls = system_stats.routing_stats

        # clean up artifacts (eventually log and then clean)
    if not baseline:
        fp = input_file.strip('inp')
        os.remove(input_file)
        os.remove(fp+'out')
        os.remove(fp+'rpt')
            
    return (ts_no_control, flooding_no_control)
    
# Run app and display result inline in the notebook
# app.run_server()

if __name__ == '__main__':
    dash_app.run_server(debug=False)