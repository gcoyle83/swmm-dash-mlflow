import os
import plotly.graph_objects as go 
from plotly.tools import mpl_to_plotly
from dash import dcc
import pyswmm
import swmmio

def cleanup_swmm_artifacts(input_file):
    """
    Remove file artifacts associated with SWMM `input_file`.
    """
    fp = input_file.strip('inp')
    os.remove(input_file)
    os.remove(fp+'out')
    os.remove(fp+'rpt')

# def update_figure(ts_base, node_base, ts_new, node_new):
def update_flows_figure(run_output, nodes=['J1','J8']):
    """
    Update system flows figure with latest SWMM run output.
    """
    # unpack output
    ts_base = run_output.get('baseline').get('ts')
    ts_new = run_output.get('new').get('ts')

    fig = go.Figure()
    # trace nodes
    for node in nodes:
        node_base = run_output.get('baseline').get(node)
        node_new = run_output.get('new').get(node)
        fig.add_trace(go.Line(x=ts_base,y=node_base,
                            mode='lines',
                            name=f"No Controls: {node}"))
        # trace new
        fig.add_trace(go.Line(x=ts_new,y=node_new,
                            mode='lines',
                            name=f"Latest: {node}"))
        
    fig.update_layout(transition_duration=50)
    graph = dcc.Graph(id='sim-plot',figure=fig)
    return graph

def run_no_control(input_file):
    """
    Run SWMM input file without control rules. 
    Returns dict of timeseries, flooding at J1 and cumulative inflows for other nodes. 
    """
    with pyswmm.Simulation(input_file) as sim:
        system_stats = pyswmm.SystemStats(sim)

        # Interceptor nodes to observe
        J1 = pyswmm.Nodes(sim)["J1"]

        # Overflows to Observe
        OF1 = pyswmm.Nodes(sim)["OF1"]
        OF2 = pyswmm.Nodes(sim)["OF2"]
        OF3 = pyswmm.Nodes(sim)["OF3"]
        J8 = pyswmm.Nodes(sim)["J8"]

        # Initializing Data Arrays for timeseries plot
        ts_no_control=[]
        flooding_no_control=[]
        of1_no_control=[]
        of2_no_control=[]
        of3_no_control=[]
        j8_no_control=[]

        sim.step_advance(300)
        for ind, step in enumerate(sim):
            ts_no_control.append(sim.current_time)
            flooding_no_control.append(J1.flooding)
            of1_no_control.append(OF1.cumulative_inflow)
            of2_no_control.append(OF2.cumulative_inflow)
            of3_no_control.append(OF3.cumulative_inflow)
            j8_no_control.append(J8.cumulative_inflow)
            pass
        # Get Results for Post Processing Table
        # no_control_J8 = J8.cumulative_inflow
        # no_control_total_overflow = OF1.cumulative_inflow \
        #                         + OF2.cumulative_inflow \
        #                         + OF3.cumulative_inflow
        # no_controls = system_stats.routing_stats
    summary = {
        'ts': ts_no_control,
        'J1': flooding_no_control,
        'OF1': of1_no_control,
        'OF2': of2_no_control,
        'OF3': of3_no_control,
        'J8': j8_no_control
    }
    return summary
    
def run_simple_control(input_file, control1=0.2, control2=0.4, control3=1.0):
    """
    Run input file with simple control rules. 
    `control1` is the percent open of all orifices when flow is high in wet weather.
    `control2` is the percent open "" when flow is medium in wet weather.
    `control3` is the percent open during dry weather with low flow.
    For control values, enter as pct in 0-1 (e.g., 50% open is 0.5).
    Returns dict of timeseries, flooding at J1 and cumulative inflows for other nodes. 
    """
    with pyswmm.Simulation(input_file) as sim:
        # system_stats = pyswmm.SystemStats(sim)

        # Instantiating the Orifices to Control
        OR1 = pyswmm.Links(sim)["OR1"]
        OR2 = pyswmm.Links(sim)["OR2"]
        OR3 = pyswmm.Links(sim)["OR3"]

        # Interceptor Nodes to Observe
        J1 = pyswmm.Nodes(sim)["J1"]
        J2 = pyswmm.Nodes(sim)["J2"]
        J8 = pyswmm.Nodes(sim)["J8"]

        # Storage Tanks to Observe
        SU1 = pyswmm.Nodes(sim)['SU1']
        SU2 = pyswmm.Nodes(sim)['SU2']
        SU3 = pyswmm.Nodes(sim)['SU3']

        # Overflows to Observe
        OF1 = pyswmm.Nodes(sim)["OF1"]
        OF2 = pyswmm.Nodes(sim)["OF2"]
        OF3 = pyswmm.Nodes(sim)["OF3"]

        # Initializing Data Arrays for timeseries plot
        ts_w_control=[]
        flooding_w_control=[]
        of1=[]
        of2=[]
        of3=[]
        j8=[]

        sim.step_advance(300)
        # Launch a simulation!
        in_wet_weather = False
        for ind, step in enumerate(sim):
            ts_w_control.append(sim.current_time)
            flooding_w_control.append(J1.flooding)
            of1.append(OF1.cumulative_inflow)
            of2.append(OF2.cumulative_inflow)
            of3.append(OF3.cumulative_inflow)
            j8.append(J8.cumulative_inflow)

            # set controls
            if J2.depth > 4.5 and in_wet_weather == False:
                OR1.target_setting = control1
                OR2.target_setting = control1
                OR3.target_setting = control1
                in_wet_weather = True
            elif J2.depth <= 4 and in_wet_weather == True:
                OR1.target_setting = control2
                OR2.target_setting = control2
                OR3.target_setting = control2
            elif J2.depth < 2:
                OR1.target_setting = control3
                OR2.target_setting = control3
                OR3.target_setting = control3
                in_wet_weather = False

        # Performance Analysis (KPI Compare)
        # w_control_J8 = J8.cumulative_inflow
        # w_control_total_overflow = OF1.cumulative_inflow \
        #                         + OF2.cumulative_inflow \
        #                         + OF3.cumulative_inflow
        # w_controls = system_stats.routing_stats
    summary = {
        'ts': ts_w_control,
        'J1': flooding_w_control,
        'OF1': of1,
        'OF2': of2,
        'OF3': of3,
        'J8': j8
    }
    return summary

import swmmio
import matplotlib.pyplot as plt

def system_profile(input_file):
    # Profile Plotter Demo
    rpt_file = input_file.strip('inp')+'rpt'
    rpt = swmmio.rpt("swmm_files/DemoModel.rpt")
    profile_depths_no_control = rpt.node_depth_summary.MaxNodeDepthReported
    rpt = swmmio.rpt(rpt_file)
    profile_depths_w_control = rpt.node_depth_summary.MaxNodeDepthReported

    mymodel = swmmio.Model("swmm_files/DemoModel.inp")
    fig = plt.figure(figsize=(11,9))
    fig.suptitle("Max HGL")
    ax = fig.add_subplot(6,1,(1,3))
    path_selection = swmmio.find_network_trace(mymodel, 'J1', 'J8')
    profile_config = swmmio.build_profile_plot(ax, mymodel, path_selection)
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_no_control, label="No Control")
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_w_control, color='green',label="With Control")
    swmmio.add_node_labels_plot(ax, mymodel, profile_config)
    swmmio.add_link_labels_plot(ax, mymodel, profile_config)
    leg = ax.legend()
    ax.grid('xy')
    ax.get_xaxis().set_ticklabels([])

    ax = fig.add_subplot(6,1,4)
    path_selection = swmmio.find_network_trace(mymodel, 'J22', 'J1')
    profile_config = swmmio.build_profile_plot(ax, mymodel, path_selection)
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_no_control, label="No Control")
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_w_control, color='green',label="With Control")
    swmmio.add_node_labels_plot(ax, mymodel, profile_config)
    ax.grid('xy')
    ax.get_xaxis().set_ticklabels([])

    ax = fig.add_subplot(6,1,5)
    path_selection = swmmio.find_network_trace(mymodel, 'J10', 'J3')
    profile_config = swmmio.build_profile_plot(ax, mymodel, path_selection)
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_no_control, label="No Control")
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_w_control, color='green',label="With Control")
    swmmio.add_node_labels_plot(ax, mymodel, profile_config)
    ax.grid('xy')
    ax.get_xaxis().set_ticklabels([])

    ax = fig.add_subplot(6,1,6)
    path_selection = swmmio.find_network_trace(mymodel, 'J15', 'J6')
    profile_config = swmmio.build_profile_plot(ax, mymodel, path_selection)
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_no_control, label="No Control")
    swmmio.add_hgl_plot(ax, profile_config, depth=profile_depths_w_control, color='green',label="With Control")
    swmmio.add_node_labels_plot(ax, mymodel, profile_config)

    ax.grid('xy')
    fig.tight_layout()
    plotly_fig = mpl_to_plotly(fig)
    graph = dcc.Graph(id='profile-plot',figure=plotly_fig)
    return graph