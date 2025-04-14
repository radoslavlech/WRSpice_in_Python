import matplotlib.pyplot as plt
import ast
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib import animation as anm
from functions import *
from classes import *
from parse_and_modify import parse_and_modify



NETLIST = 'cell_example'
SIM_FILE = f'sim_outputs/{NETLIST}.csv'

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


#ADDING ANIMATION

#if necessary:
# parse_and_modify(SIM_FILE)

df = pd.read_csv(SIM_FILE,sep=';')

columns = df.columns
time_vec = np.array(df[columns[0]])
Voltage_ev_mtx = df[columns[1:-1]]
Voltage_ev_mtx = np.array(Voltage_ev_mtx)
Voltage_ev_mtx = np.array(Voltage_ev_mtx)*5e3 #5e-3 the best for interface
nodes_dict = {node.index : node.pos for node in nodes}

interesting_pairs = [ast.literal_eval(col.replace('v','').replace('units=V',"").strip()) for col in columns[1:-1]]

x_space = []
for pair in interesting_pairs:
    if isinstance(pair, tuple):
        x_space.append((nodes_dict[str(pair[0])][0] + nodes_dict[str(pair[1])][0])/2)
    else:
        x_space.append(nodes_dict[str(pair)][0])

def update_plot(nt):
    voltage.set_data(x_space, Voltage_ev_mtx[nt,:])
    return voltage, 

voltage, = ax.plot([],[],color='r')

anim = anm.FuncAnimation(fig, update_plot, frames=len(time_vec), interval=20,repeat=True,blit=True)



plt.show()




