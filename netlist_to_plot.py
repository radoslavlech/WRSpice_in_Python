import matplotlib.pyplot as plt
import ast
import matplotlib.patches as patches
from parse_and_modify import parse_and_modify
import numpy as np
import pandas as pd
from matplotlib import animation as anm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import random as r
from functions import *
from classes import *




NETLIST = 'cell_example'
V_SIM_FILE = f'sim_outputs/{NETLIST}.csv'
V_JJ_FILE = f'sim_outputs/{NETLIST}_jj_voltage.csv'
I_SIM_FILE = f'sim_outputs/{NETLIST}_currents.csv'

inductances = []
voltage_sources = []
current_sources = []
resistors = []
capacitors = []
josephson_junctions = []
keywords = ['run', 'plot', 'edit','wrdata','write',' ']

devices = []
nodes = []
junction_nodes = []
with open(f'../{NETLIST}.cir') as netlist:
    g_counter = 0
    for line in netlist:
        if line[0] in ['*','.']:
            continue
        else: 
            first_space = line.find(' ')
            second_space = line.find(' ',first_space+1)
            third_space = line.find(' ',second_space+1)
            device = line[:first_space]
            if device and device not in keywords:
                fro = line[first_space:second_space].replace(" ","")
                to = line[second_space:third_space].replace(" ","")
                
                if fro=="0":
                    fro = 'g'+str(g_counter)
                    g_counter+=1
                if to=="0":
                    to = 'g'+str(g_counter)
                    g_counter+=1

                symbol = device 
                if device[0]=='b':
                    josephson_junctions.append(device)
                    fourth_space = line.find(' ',third_space+1)
                    device = JJ()
                    device.type = 'josephson_junction'
                    junction_node = line[third_space:fourth_space]
                    device.junction_node = junction_node.strip()
                    junction_node_idx = junction_node.strip()
                    junction_node = Node()
                    junction_node.index = junction_node_idx
                    junction_node.between=(fro,to)
                    nodes.append(junction_node)
                    junction_nodes.append(junction_node)

                elif device[0]=='I':
                    current_sources.append(device)
                    fourth_space = line.find(' ',third_space+1)
                    device = Current_Source()
                    current_type = line[third_space:fourth_space]
                    device.type = "current_source"
                    device.current_type = current_type
                else:
                    if device[0]=='L':
                        inductances.append(device)
                        device = Device()
                        device.type = "inductance"
                    elif device[0]=='V':
                        voltage_sources.append(device)
                        device = Device()
                        device.type = "voltage_source"
                    elif device[0]=='C':
                        capacitors.append(device)
                        device = Device()
                        device.type = "capacitor"
                    elif device[0]=='R':
                        resistors.append(device)
                        device = Device()
                        device.type = "resistor"
                device.symbol = symbol
                device.fro = fro
                device.to = to
                devices.append(device)
                fro_idx = fro
                to_idx = to
 
                #1 checking if node with idx fro exists
                #if YES add .to to it 
                #if NOT create
                if exists(fro_idx,nodes):
                    fro = find_node(fro_idx,nodes)
                    if exists(to_idx,nodes):
                        to = find_node(to_idx,nodes)
                        to.fro.append(fro)
                        fro.to.append(to)
                    else:
                        to = Node()
                        nodes.append(to)
                        to.index = to_idx
                        to.fro.append(fro)
                        fro.to.append(to) 
                else: 
                    fro = Node()
                    nodes.append(fro)
                    fro.index = fro_idx
                    if exists(to_idx,nodes):
                        to = find_node(to_idx,nodes)
                        to.fro.append(fro)
                        fro.to.append(to)
                    else:
                        to = Node()
                        nodes.append(to)
                        to.index = to_idx
                        to.fro.append(fro)
                        fro.to.append(to) 



colors_dict = {node.index: (r.randint(1,10)/10,r.randint(1,10)/10,r.randint(1,10)/10) for node in nodes}


fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
y_min = -5
y_max = 5
ax.set_ylim(y_min,y_max)
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


v_df = pd.read_csv(V_SIM_FILE,sep=';')
i_df = pd.read_csv(I_SIM_FILE,sep=';')

print(i_df)

v_columns = v_df.columns
i_columns = i_df.columns
time_vec = np.array(v_df[v_columns[0]])
dt=time_vec[1]-time_vec[0]

Voltage_ev_mtx = v_df[v_columns[1:]]
Voltage_ev_mtx = np.array(Voltage_ev_mtx)
Voltage_ev_mtx = np.array(Voltage_ev_mtx)*5e3 #5e-3 the best for interface

Current_ev_mtx = i_df[i_columns[1:]]
Current_ev_mtx = np.array(Current_ev_mtx)
Current_ev_mtx=Current_ev_mtx*1e2
print(Current_ev_mtx)

voltage_interesting_pairs = [ast.literal_eval(col.replace('v','').replace('units=V',"").strip()) for col in v_columns[1:]]
current_interesting_nodes = [col.replace('#branch','').replace('i(','').replace('units=A',"").replace(')','').strip() for col in i_columns[1:]]


print(current_interesting_nodes)


x_space_v = []
for pair in voltage_interesting_pairs:
    if isinstance(pair, tuple):
        x_space_v.append((nodes_dict[str(pair[0])][0] + nodes_dict[str(pair[1])][0])/2)
    else:
        x_space_v.append(nodes_dict[str(pair)][0])

x_space_i = []
for branch in current_interesting_nodes:
    x_space_i.append(nodes_dict[find_device(branch,devices).fro][0])
    ax.scatter(nodes_dict[find_device(branch,devices).fro][0],nodes_dict[find_device(branch,devices).fro][1],color=colors_dict[find_device(branch,devices).fro])






offset =30
def update_plot(nt):
    voltage.set_data(x_space_v, Voltage_ev_mtx[nt,:])
    current1.set_data(time_vec[nt:nt+offset], Current_ev_mtx[nt:nt+offset,0])
    current2.set_data(time_vec[nt:nt+offset], Current_ev_mtx[nt:nt+offset,1])
    inset1.set_xlim(dt*(nt-offset/4),(nt+offset)*dt)
    return  current1, voltage, current2,

voltage, = ax.plot([],[],color='r')

inset1 = inset_axes(ax, width="30%", height="30%", loc='upper left')
insetjj = inset_axes(ax, width="30%", height="30%", loc='upper right')

current1, = inset1.plot([],[],color=colors_dict[find_device(current_interesting_nodes[0],devices).fro],lw=1,label=f'i({find_device(current_interesting_nodes[0],devices).fro})')   
current2, = inset1.plot([],[],color=colors_dict[find_device(current_interesting_nodes[1],devices).fro],lw=1,label=f'i({find_device(current_interesting_nodes[1],devices).fro})')

jj_list=[]
jj, = inset1.plot([],[],color=colors_dict[find_device(current_interesting_nodes[0],devices).fro],lw=1,label=f'i({find_device(current_interesting_nodes[0],devices).fro})')   
jj_list.append(jj)
print(jj_list)

anim = anm.FuncAnimation(fig, update_plot, frames=len(time_vec), interval=20,repeat=True,blit=True)

inset1.set_xlabel('time')
inset1.legend()

plt.show()