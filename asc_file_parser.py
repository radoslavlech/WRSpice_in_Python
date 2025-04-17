import matplotlib.pyplot as plt
import numpy as np

ASC_FILE = '3dbasiccell.asc'


fig = plt.figure()
ax = fig.add_subplot(111)


types = []

with open(f'../{ASC_FILE}') as netlist:
    g_counter = 0
    for line in netlist:
        if line[0] in ['*','.']:
            continue
        else: 
            first_space = line.find(' ')
            second_space = line.find(' ',first_space+1)
            third_space = line.find(' ',second_space+1)
            fourth_space = line.find(' ',third_space+1)
            fifth_space = line.find(' ',fourth_space+1)
            type = line[:first_space]
            if type=="WIRE":
                x_space = [int(line[first_space:second_space].strip()),int(line[third_space:fourth_space].strip())]
                y_space = [-int(line[second_space:third_space].strip()),-int(line[fourth_space:fifth_space].strip())]
                ax.plot(x_space,y_space,color='k')



ax.set_aspect('equal')
plt.show()



def add_asc_to_plot(ax,asc_file):
    pass