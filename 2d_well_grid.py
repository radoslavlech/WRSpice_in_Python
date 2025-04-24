from matplotlib import pyplot as plt 
import numpy as np
import ast
import pandas as pd
from matplotlib import animation as anm
from classes import *
from functions import *

TITLE = '2_wells_2d'
V_SIM_FILE = f'sim_outputs/2_wells_2d.csv'

GRID_W = 80
GRID_H = 50


f= 10e3           
T = 1 / f           # Period = 1 ms
n_cycles = 10
t_end = n_cycles * T
dt = T / 100        # 100 points per cycle
A = 5.0             # Amplitude
t = np.arange(0, t_end + dt, dt)
v = A * np.sin(2 * np.pi * f * t)

pwl_str = "PWL(" + " ".join(f"{ti:.6f} {vi:.6f}" for ti, vi in zip(t, v)) + ")"


parameters ={
    'w_grid' : GRID_W,
    'h_grid' : GRID_H,
    'well1_shape': 'circle',
    'well2_shape': 'circle',
    'r_well1': 5,
    'r0_well1': np.array([35,25]),
    'r_well2':7.5,
    'r0_well2': np.array([50,25]),
    'l1' : 1e-3,
    'l': 1e-3,
    'c1': 1e-6
}


netlist_config={
    'title': TITLE,
    'sim_title': TITLE.lower(),
    'sim_out_path': 'C:/Users/radzi/Desktop/PRAKTYKA/SYMULACJE/WRSPICE_PYTHON/sim_outputs',
    'models': False,
    'transient': True,
    'simulation': True,
    'resistors': False,
    'inductances': True,
    'capacitors': True,
    'current_sources': False,
    'generators': True,
    'josephson_junctions': False,
    'model_names' : [],
    'model_types' : [],
    'timestep' : f'{1/f/5}',
    'duration' : f'{1/f*100}',
    'trans_conf' : 'uic',  #use initial condition
    'R_nodes' : [],
    'R_values' : [],
    'R_symbols' : [],
    'L_nodes' : [],
    'L_values' : [],
    'L_symbols' : [],
    'C_nodes' : [],
    'C_values' : [],
    'C_symbols' : [],

    'I_nodes' : [],
    'I_types' : [],
    'I_symbols' : [],
    'V_nodes' : [(111111+1000*29+parameters['r0_well1'][1],0)],
    'V_types' : [pwl_str],
    'V_symbols' : ['V_inp'],
    'JJ_nodes' : [],
    'JJ_symbols' : None,
    'JJ_models' : None,
    'JJ_parameters' : None,
    'nodes_to_simulate_V' : [f'({111111+1000*x+parameters['r0_well1'][1]})' for x in range(GRID_W)],
    'nodes_to_simulate_jjV' : None,
    'nodes_to_simulate_I' : None,
    'sim_types': ['v']
}


def plot_grid(ax,parameters_dict,netlist_config):

    w_grid = parameters_dict['w_grid']
    h_grid = parameters_dict['h_grid']
    r_well1 =parameters_dict['r_well1']
    r0_well1 =parameters_dict['r0_well1']
    r_well2 =parameters_dict['r_well2']
    r0_well2 =parameters_dict['r0_well2']
    l1 = parameters_dict['l1']
    c1 = parameters_dict['c1']
    l = parameters_dict['l']


    start_node_index = 111111
    start_node_coords = np.array([0,0])

    x = np.arange(w_grid)
    y = np.arange(h_grid)
    xx, yy = np.meshgrid(x, y)
    x_flat = xx.flatten()
    y_flat = yy.flatten()


    outside_well1 = list(map(int, (x_flat-r0_well1[0])**2 + (y_flat-r0_well1[1])**2 > r_well1**2))
    outside_well2 = list(map(int, (x_flat-r0_well2[0])**2 + (y_flat-r0_well2[1])**2 > r_well2**2))
    outside_well = list(np.array(outside_well1)*np.array(outside_well2))
    outside_well = list(map(bool,outside_well))
    
    inside_well1 = list(map(int, (x_flat-r0_well1[0])**2 + (y_flat-r0_well1[1])**2 <= r_well1**2))
    inside_well2 = list(map(int, (x_flat-r0_well2[0])**2 + (y_flat-r0_well2[1])**2 <= r_well2**2))
    inside_well = list(np.array(inside_well1)+np.array(inside_well2))
    inside_well = list(map(bool,inside_well))

    x_out = x_flat[outside_well]
    y_out = y_flat[outside_well]


    x_in = x_flat[inside_well]
    y_in = y_flat[inside_well]

    l_count = 1
    c_count = 1
    for x in range(w_grid):
        for y in range(h_grid):
            node_index = start_node_index+1000*x+y
            netlist_config['L_nodes'].append((node_index,node_index+1))
            netlist_config['L_symbols'].append(f'L{l_count}')
            netlist_config['L_values'].append(l)
            l_count+=1
            netlist_config['L_nodes'].append((node_index,node_index+1000))
            netlist_config['L_symbols'].append(f'L{l_count}')
            netlist_config['L_values'].append(l)
            l_count+=1
            
            netlist_config['C_nodes'].append((node_index,0))
            netlist_config['C_symbols'].append(f'C{c_count}')
            netlist_config['C_values'].append(c1)
            c_count+=1

            if outside_well[x*h_grid+y]==1:
                netlist_config['L_nodes'].append((node_index,0))        
                netlist_config['L_symbols'].append(f'L{l_count}')
                netlist_config['L_values'].append(l1)
                l_count+=1




    ax.scatter(x_out, y_out, s=0.5, color='black')
    ax.scatter(x_in, y_in, s=0.5, color='red')



        

fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_aspect('equal')

plot_grid(ax,parameters,netlist_config)
generate_netlist('../2_wells_2d.cir',netlist_config)
parse_and_modify(V_SIM_FILE)

#ANIMATING


fig2 = plt.figure()
ax2=fig2.add_subplot(111)
ax2.set_xlim(0,GRID_W)
ax2.set_ylim(-1,1)

df = pd.read_csv(V_SIM_FILE,sep=';')
columns = df.columns
v_interesting_nodes = [ast.literal_eval(col.replace('v','').replace('units=V',"").strip()) for col in columns[1:]]

time_vec = np.array(df[columns[0]])

dt=time_vec[1]-time_vec[0]
Voltage_ev_mtx = df[columns[1:]]
Voltage_ev_mtx = np.array(Voltage_ev_mtx)
print(Voltage_ev_mtx)

x_space = [i for i in range(GRID_W)]
print(len(v_interesting_nodes), len(x_space))
voltage, = ax2.plot([],[],color='r')

def update_plot(nt):
    voltage.set_data(x_space, Voltage_ev_mtx[nt,:])
    return  voltage, 

print(v_interesting_nodes)
anim = anm.FuncAnimation(fig2, update_plot, frames=len(time_vec), interval=20,repeat=True,blit=False)


plt.show()