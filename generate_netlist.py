TITLE = 'Interface'
SIMULATION_TITLE = TITLE.lower()
SIM_OUT_PATH = 'C:/Users/radzi/Desktop/PRAKTYKA/SYMULACJE/WRSPICE_PYTHON/sim_outputs'

MODELS = 1
TRANSIENT = 1
SIMULATION = 1

N_RESISTORS = 2
N_INDUCTANCES = 0
N_CAPACITORS = 0
N_CURRENT_SOURCES = 2
N_GENERATORS = 0
N_JJ = 104
if N_JJ:
    MODELS =1


model_names = ['jj1']
model_types = ['jj(level=1, cap=5e-12, rn=0.7)']

timestep = '0.5p'
duration = '325p'
trans_conf = 'uic'  #use initial condition



R_nodes = [(0,1),(53,54)]
R_values = [3 for i in range(N_RESISTORS)]
R_symbols = [f'R{i+1}' for i in range(N_RESISTORS)]

L_nodes = []
L_values = []
L_symbols = []

C_nodes = []
C_values = []
C_symbols = []

I_nodes = [(0,1),(0,53)]
I_types = ['pulse(0 0.1m 50p 1p 1p 10p 0 60p 120p 180p)', 'DC 666.67uA']
I_symbols = ['Iinp', 'Ib']


JJ_nodes = [(i+1, i+2,i+1000) for i in range(52)]+[(i+54, i+55,i+1054) for i in range(52)]
JJ_symbols = [f'bJ{i+1}' for i in range(N_JJ)]
JJ_models = ['jj1' for i in range(N_JJ)]
JJ_parameters = ['ics=400uA' for i in range(N_JJ)]

nodes_to_simulate = [(nodes[0],nodes[1]) for nodes in JJ_nodes]
nodes_to_simulate2 = [(nodes[2]) for nodes in JJ_nodes]
sim_types = ['v']


print(R_symbols)


with open(f'../interface.cir','w') as f:
    f.write(f"*{TITLE}\n")
    if MODELS:
        f.write("\n*Model definitions\n")
        for i in range(MODELS):
            f.write(".model " + f"{model_names[i]} {model_types[i]}\n")

    if SIMULATION:
        f.write(f"\n*Simulation\n")
        f.write(f".control\nrun\n")
        f.write(f"write {SIM_OUT_PATH}/{SIMULATION_TITLE}.csv ")
        # f.write(f"plot ")
        for type in sim_types:
            for node in nodes_to_simulate:
                f.write(f"{type}{node} ")
        
        f.write(f"\nwrite {SIM_OUT_PATH}/{SIMULATION_TITLE}_jj_voltage.csv ")
        for node in nodes_to_simulate2:
                f.write(f"v({node}) ")

        f.write(f"\nedit\n.endc\n")
        

    if N_RESISTORS:
        f.write("\n*Resistances\n")
        for i in range(N_RESISTORS):
            f.write(f"{R_symbols[i]} {R_nodes[i][0]} {R_nodes[i][1]} {R_values[i]}\n")
    if N_INDUCTANCES:
        f.write("*Inductances\n")
        for i in range(N_INDUCTANCES):
            f.write(f"{L_symbols[i]} {L_nodes[i][0]} {L_nodes[i][1]} {L_values[i]}\n")
    if N_CAPACITORS:
        f.write("*Capacitances\n")
        for i in range(N_CAPACITORS):
            f.write(f"{C_symbols[i]} {C_nodes[i][0]} {C_nodes[i][1]} {C_values[i]}\n")

    if N_CURRENT_SOURCES:
        f.write("\n*Current sources (input and biases)\n")
        for i in range(N_CURRENT_SOURCES):
            f.write(f"{I_symbols[i]} {I_nodes[i][0]} {I_nodes[i][1]} {I_types[i]}\n")

    if N_JJ:
        f.write("\n*Josephson junctions\n")
        for i in range(N_JJ):
            f.write(f"{JJ_symbols[i]} {JJ_nodes[i][0]} {JJ_nodes[i][1]} {JJ_nodes[i][2]} {JJ_models[i]} {JJ_parameters[i]}\n")
    if TRANSIENT:
        f.write("\n*Transient analysis\n")
        f.write(f".tran {timestep} {duration} {trans_conf}\n")
    
    f.write("\n.end")