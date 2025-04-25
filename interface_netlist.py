from functions import *

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


netlist_config={
    'title': TITLE,
    'sim_title': TITLE.lower(),
    'sim_out_path': SIM_OUT_PATH,

    'models': True,
    'transient': True,
    'simulation': True,
    'resistors': True,
    'inductances': True,
    'capacitors': True,
    'current_sources': True,
    'generators': True,
    'josephson_junctions': True,


    'model_names' : ['jj1'],
    'model_types' : ['jj(level=1, cap=5e-12, rn=0.7)'],
    'timestep' : '0.5p',
    'duration' : '325p',
    'trans_conf' : 'uic',  #use initial condition
    
    'R_nodes' : [(0,1),(53,54)],
    'R_values' : [3 for i in range(N_RESISTORS)],
    'R_symbols' : [f'R{i+1}' for i in range(N_RESISTORS)],

    'L_nodes' : [],
    'L_values' : [],
    'L_symbols' : [],

    'C_nodes' : [],
    'C_values' : [],
    'C_symbols' : [],

    'I_nodes' : [(0,1),(0,53)],
    'I_types' : ['pulse(0 0.1m 50p 1p 1p 10p 0 60p 120p 180p)', 'DC 666.67uA'],
    'I_symbols' : ['Iinp', 'Ib'],


    'JJ_nodes' : [(i+1, i+2,i+1000) for i in range(52)]+[(i+54, i+55,i+1054) for i in range(52)],
    'JJ_symbols' : None,
    'JJ_models' : None,
    'JJ_parameters' : None,

    'nodes_to_simulate_V' : None,
    'nodes_to_simulate_jjV' : None,
    'nodes_to_simulate_I' : None,
    'sim_types': ['v']
}

netlist_config['JJ_symbols']=[f'bJ{i+1}' for i in range(N_JJ)]
netlist_config['JJ_models'] = ['jj1' for i in range(N_JJ)]
netlist_config['JJ_parameters']= ['ics=400uA' for i in range(N_JJ)]
netlist_config['nodes_to_simulate_V']= [(nodes[0],nodes[1]) for nodes in netlist_config['JJ_nodes']]
netlist_config['nodes_to_simulate_jjV'] : [(nodes[2]) for nodes in netlist_config['JJ_nodes']]
netlist_config['nodes_to_simulate_I'] : [netlist_config['I_nodes'][1]]


# generate_netlist('../interface.cir','w')