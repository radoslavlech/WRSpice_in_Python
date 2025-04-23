from matplotlib import pyplot as plt 
import numpy as np
from classes import *

GRID_W = 80
GRID_H = 80

parameters ={
    'w_grid' : GRID_W,
    'h_grid' : GRID_H,
    'well1_shape': 'circle',
    'well2_shape': 'circle',
    'r_well1':12.5,
    'r0_well1': np.array([30,40]),
    'r_well2':10,
    'r0_well2': np.array([60,40])
}

print(parameters)

def plot_grid(ax,parameters_dict):
    w_grid = parameters_dict['w_grid']
    h_grid = parameters_dict['h_grid']
    r_well1 =parameters_dict['r_well1']
    r0_well1 =parameters_dict['r0_well1']
    r_well2 =parameters_dict['r_well2']
    r0_well2 =parameters_dict['r0_well2']


    start_node_label = 1111
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
    
    inside_well = (x_flat-r0_well1[0])**2 + (y_flat-r0_well1[1])**2 <= r_well1**2 
    x_out = x_flat[outside_well]
    y_out = y_flat[outside_well]
    x_in = x_flat[inside_well]
    y_in = y_flat[inside_well]

    ax.scatter(x_out, y_out, s=0.5, color='black')
    ax.scatter(x_in, y_in, s=0.5, color='red')



def generte_netlist(): 
    pass
        

fig = plt.figure()
ax=fig.add_subplot(111)

plot_grid(ax,parameters)


ax.set_aspect('equal')
plt.show()