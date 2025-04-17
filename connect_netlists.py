from functions import *

N1 = 'cell_example'
N2 = 'well_1d'
N3 = 'interface'

def connect(*netlists):
    inductances = []
    voltage_sources = []
    current_sources = []
    resistors = []
    capacitors = []
    josephson_junctions = []
    devices = []
    nodes = []
    junction_nodes = []
    all_symbols = []

    for netlist in netlists:
        get_devices_and_nodes(netlist,devices,nodes,junction_nodes,all_symbols,resistors,inductances,capacitors,current_sources,voltage_sources,josephson_junctions)
    print(all_symbols)

connect(N1,N2,N3)




