import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_JJ(Node1,Node2,ax):
    pass


def draw_resistor(ax, x, y, length=1.0):
    # Simple zigzag line
    ax.plot([x, x+length/4], [y, y], color='black')
    ax.plot([x+length/4, x+length/2], [y, y+0.2], color='black')
    ax.plot([x+length/2, x+3*length/4], [y+0.2, y-0.2], color='black')
    ax.plot([x+3*length/4, x+length], [y-0.2, y], color='black')

def draw_capacitor(ax, x, y, spacing=0.2):
    ax.plot([x, x + spacing], [y, y], color='black')
    ax.plot([x + spacing, x + spacing], [y - 0.3, y + 0.3], color='black')
    ax.plot([x + spacing*2, x + spacing*2], [y - 0.3, y + 0.3], color='black')
    ax.plot([x + spacing*2, x + spacing*3], [y, y], color='black')

def draw_ground(ax, x, y):
    ax.plot([x - 0.1, x + 0.1], [y, y], color='black')
    ax.plot([x - 0.07, x + 0.07], [y - 0.05, y - 0.05], color='black')
    ax.plot([x - 0.04, x + 0.04], [y - 0.1, y - 0.1], color='black')

fig = plt.figure()
ax=fig.add_subplot(111)
draw_resistor(ax,0,0)
plt.show()