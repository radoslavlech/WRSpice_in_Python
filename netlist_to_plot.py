import matplotlib.pyplot as plt
import ast
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib import animation as anm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import random as r
from functions import *
from classes import *



NETLIST = 'cell_example'
V_SIM_FILE = f'sim_outputs/{NETLIST}5.csv'
V_JJ_FILE = f'sim_outputs/{NETLIST}_jj_voltage5.csv'
I_SIM_FILE = f'sim_outputs/{NETLIST}_currents5.csv'

inductances = []
voltage_sources = []
current_sources = []
resistors = []
capacitors = []
josephson_junctions = []
devices = []
nodes = []
junction_nodes = []
all_symbols=[]

get_devices_and_nodes(NETLIST,devices,nodes,junction_nodes,all_symbols,resistors,inductances,capacitors,current_sources,voltage_sources,josephson_junctions)

colors_dict = {node.index: (r.randint(1,10)/10,r.randint(1,10)/10,r.randint(1,10)/10) for node in nodes}

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
# y_min = -5
# y_max = 5
# ax.set_ylim(y_min,y_max)
# x_min = 0
# x_max = 60
# ax.set_xlim(x_min,x_max)
# ax.set_position([0.1, 0.1, 0.9, 0.9])
chains = create_chains(ax,nodes)
assign_coords_and_draw(ax,nodes)

for junction_node in junction_nodes:
    junction_node.pos = (find_node(junction_node.between[0],nodes).pos+ find_node(junction_node.between[1],nodes).pos)/2

assign_subbranches(devices)
draw_by_device(ax,devices,nodes)
nodes_dict = {node.index : node.pos for node in nodes}
ax.axis('off')



#ADDING ANIMATION





#if necessary:
# parse_and_modify(V_SIM_FILE)
# parse_and_modify(I_SIM_FILE)
# parse_and_modify(V_JJ_FILE)
CHOSEN_JJ_NODE = 2


v_df = pd.read_csv(V_SIM_FILE,sep=';')
i_df = pd.read_csv(I_SIM_FILE,sep=';')
phase_df = pd.read_csv(V_JJ_FILE,sep=';')



v_columns = v_df.columns
i_columns = i_df.columns
phase_columns = phase_df.columns

time_vec = np.array(v_df[v_columns[0]])
dt=time_vec[1]-time_vec[0]

Voltage_ev_mtx = v_df[v_columns[1:]]
Voltage_ev_mtx = np.array(Voltage_ev_mtx)
Voltage_ev_mtx = np.array(Voltage_ev_mtx)*5e3 #5e-3 the best for interface

Current_ev_mtx = i_df[i_columns[1:]]
Current_ev_mtx = np.array(Current_ev_mtx)
print(Current_ev_mtx)


Phase_ev_mtx = phase_df[phase_columns[1:]]
Phase_ev_mtx = np.array(Phase_ev_mtx)
# Phase_ev_mtx = Phase_ev_mtx*1e-4



voltage_interesting_pairs = [ast.literal_eval(col.replace('v','').replace('units=V',"").strip()) for col in v_columns[1:]]
current_interesting_nodes = [col.replace('#branch','').replace('i(','').replace('units=A',"").replace(')','').strip() for col in i_columns[1:]]
jj_interesting_nodes = [ast.literal_eval(col.replace('v','').replace('units=V',"").strip()) for col in phase_columns[1:]]

x_space_v = []
x_space_i = []
x_space_jj = []

for pair in voltage_interesting_pairs:
    if isinstance(pair, tuple):
        x_space_v.append((nodes_dict[str(pair[0])][0] + nodes_dict[str(pair[1])][0])/2)
    else:
        x_space_v.append(nodes_dict[str(pair)][0])


for branch in current_interesting_nodes:
    print(branch)
    x_space_i.append(nodes_dict[find_device(branch,devices).fro][0])
    ax.scatter(nodes_dict[find_device(branch,devices).fro][0],nodes_dict[find_device(branch,devices).fro][1],color=colors_dict[find_device(branch,devices).fro])

for node in jj_interesting_nodes:
    x_space_jj.append(nodes_dict[str(node)][0])
    ax.scatter(nodes_dict[str(node)][0],nodes_dict[str(node)][1],color=colors_dict[str(node)])




offset =30
jj_offset = 500
def update_plot(nt):
    voltage.set_data(x_space_v, Voltage_ev_mtx[nt,:])

    current1.set_data(time_vec[nt:nt+offset], Current_ev_mtx[nt:nt+offset,0])
    current2.set_data(time_vec[nt:nt+offset], Current_ev_mtx[nt:nt+offset,1])
    current1_now.set_data([time_vec[nt],time_vec[nt-2]],[Current_ev_mtx[nt,0],Current_ev_mtx[nt,0]])
    current2_now.set_data([time_vec[nt],time_vec[nt-2]],[Current_ev_mtx[nt,1],Current_ev_mtx[nt,1]])

    phase1.set_data(time_vec[nt:nt+1000], Phase_ev_mtx[nt:nt+1000,CHOSEN_JJ_NODE])
    phase1_now.set_data([time_vec[nt],time_vec[nt-3]],[Phase_ev_mtx[nt,CHOSEN_JJ_NODE],Phase_ev_mtx[nt,CHOSEN_JJ_NODE]])

    inset1.set_xlim(dt*(nt-offset/4),(nt+offset)*dt)

    insetjj.set_xlim(dt*(nt-jj_offset/10),(nt+jj_offset)*dt)
    
    return  voltage, current1,phase1, phase1_now, current1_now, current2,current2_now,

voltage, = ax.plot([],[],color='r')

inset1 = inset_axes(ax, width="30%", height="30%", loc='upper left')
i_y_min = min(Current_ev_mtx[:,0])
i_y_max = max(Current_ev_mtx[:,0])

for i in range(len(Current_ev_mtx[0])) :
    if min(Current_ev_mtx[:,i])<i_y_min:
        i_y_min=min(Current_ev_mtx[:,i])

    if max(Current_ev_mtx[:,i])>i_y_max:
        i_y_max=max(Current_ev_mtx[:,i])
i_y_min-=0.2*i_y_max
i_y_max*=1.5

inset1.set_ylim(i_y_min,i_y_max)
inset1.vlines(0.0,i_y_min,i_y_max,linestyle='--',color='k',lw=0.5)
inset1.set_title("Input currents")

insetjj = inset_axes(ax, width="30%", height="30%", loc='upper right')
insetjj.set_title("Phase response of a chosen JJ")
jj_y_min = 0
jj_y_max = 100


insetjj.set_ylim(jj_y_min,jj_y_max)
insetjj.vlines(0.0,jj_y_min,jj_y_max,linestyle='--',color='k',lw=0.5)

current1, = inset1.plot([],[],color=colors_dict[find_device(current_interesting_nodes[0],devices).fro],lw=1,label=f'I({find_device(current_interesting_nodes[0],devices).fro})')   
current2, = inset1.plot([],[],color=colors_dict[find_device(current_interesting_nodes[1],devices).fro],lw=1,label=f'I({find_device(current_interesting_nodes[1],devices).fro})')
current1_now, = inset1.plot([],[],color=colors_dict[find_device(current_interesting_nodes[0],devices).fro],lw=10)
current2_now, = inset1.plot([],[],color=colors_dict[find_device(current_interesting_nodes[1],devices).fro],lw=10)
#   
phase1, = insetjj.plot([],[],color=colors_dict[str(jj_interesting_nodes[CHOSEN_JJ_NODE])],lw=1,label=f'I({find_device(current_interesting_nodes[0],devices).fro})')
phase1_now, = insetjj.plot([],[],color=colors_dict[str(jj_interesting_nodes[CHOSEN_JJ_NODE])],lw=10)

anim = anm.FuncAnimation(fig, update_plot, frames=len(time_vec), interval=20,repeat=True,blit=True)

inset1.set_xlabel('time')
inset1.legend()

anim.save(f"gifs/{V_SIM_FILE.split('/')[1][:-4]}.gif", writer='pillow', fps=20)
plt.show()