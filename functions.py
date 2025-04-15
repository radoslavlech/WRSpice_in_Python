import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

LINECOLOR = 'black'
LINEWEIGHT = 0.5
NODESIZE = 0.5


def exists(idx,nodelist):
    for node in nodelist:
        if node.index == idx:
            return 1
    return 0

def find_node(idx,nodelist):
    for node in nodelist:
        if node.index == idx:
            return node
        
def find_device(sym,devicelist):
    for dev in devicelist:
        if dev.symbol == sym:
            return dev

def rotate(r0,vec,angle):
    theta = angle/360*2*np.pi
    
    vec = list(vec)
    vec.append(0)
    vec = np.array(vec)

    x0 = r0[0]
    y0 = r0[1]

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    rotation = np.array([[cos_theta, -sin_theta, x0 - x0*cos_theta + y0*sin_theta], [sin_theta,  cos_theta, y0 - x0*sin_theta - y0*cos_theta]])@vec
    return np.asarray(rotation).flatten()[:2]


def rotate_correct(r0,vec,angle):
    theta = angle/360*2*np.pi
    
    vec = list(vec)
    vec.append(1)
    vec = np.array(vec)

    x0 = r0[0]
    y0 = r0[0]

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    rotation = np.array([[cos_theta, -sin_theta, x0 - x0*cos_theta + y0*sin_theta], [sin_theta,  cos_theta, y0 - x0*sin_theta - y0*cos_theta],[0,0,1]])@vec
    return np.asarray(rotation).flatten()[:2]


def is_loop(chain1,chain2):
    chains = (chain1,chain2)
    lengths = (len(chain1),len(chain2))
    shorter_chain = chains[lengths.index(min(lengths))]
    longer_chain = chains[lengths.index(max(lengths))]

    section1 = shorter_chain[1:-1]
    section2 = longer_chain[1:len(shorter_chain)]
    if shorter_chain[0]==longer_chain[0] and shorter_chain[-1]==longer_chain[len(shorter_chain)] and section1 !=section2:
        return 1
    else:
        return 0

def delete_zero(nodelist):
    newlist=[]
    for node in nodelist:
        if node.index != '0':
            newlist.append(node)
    return newlist

def remove_duplicates(nodelist):
    newlist = []
    used = []
    for node in nodelist:
        if node.index not in used:
            newlist.append(node)
            used.append(node.index)
    return newlist

def no_splits(node):
    return len(node.to)

def no_subbranches(node1,node2):
    count1 = node1.to.count(node2) 
    count2 = node2.to.count(node1) 
    return max(count1,count2)

def assign_subbranches(devices):
    used = []
    for device1 in devices:
        for device2 in devices:
            if device1!=device2 and device1 not in used and device1.fro==device2.fro and device1.to==device2.to:
                device1.no_subbranches+=1
                device2.no_subbranches+=1
                device2.subbranch +=1
                used.append(device2)
    

def find_start_nodes(nodelist):
    newlist=[]
    for node in nodelist:
        if node.fro == ['0']:
            newlist.append(node)
    return newlist

def find_longest(list):
    max = 1
    for element in list:
        if len(element)>max:
            max = len(element)
            longest = element
    return longest
    
def display(chain):
    indices =[]
    for node in chain:
        indices.append(node.index)
    print(indices)

def get_chains(all_sequences):
    chains = []
    for sequence in all_sequences:
        used = []
        new_chain = []
        for node in sequence:
            if node.index in used:
                new_chain = []
            new_chain.append(node)
            used.append(node.index) 
            chains.append(new_chain)
    #some dirty postprocessing :/
    chains_new = []
    for chain in chains:
        if chain not in chains_new:
            chains_new.append(chain)
    chains = chains_new
    chains_new = []

 
    main_chain = find_longest(chains)
    chains_new.append(main_chain)
    for chain in chains:
        overlap = set(chain) & set(main_chain)
        if len(overlap)!=len(chain):
            chains_new.append(chain)

    chains = chains_new.copy()

    #REMOVING THE CHAINS WHICH TOTALLY OVERLAP WITH OTHERS
    for i,chain in enumerate(chains):
        for chain2 in chains[:i]+chains[i+1:]:
            overlap = set(chain) & set(chain2)
            if len(overlap)==len(chain):
                try: 
                    chains_new.remove(chain)
                except:
                    continue

    for chain in chains_new:
        if chain!=main_chain:
            overlap = [item for item in main_chain if item in chain]
            if len(overlap)>1:
                if chain.index(overlap[0])==0:
                    for el in overlap[:-1]:
                        chain.remove(el)
                elif chain.index(overlap[0])>0:
                    for el in overlap[1:]:
                        chain.remove(el)
    return chains_new



def concatenate(start_node,ax,chain_empty_list):
    start_node.to = remove_duplicates(start_node.to)
    for i, next in enumerate(start_node.to):
        if start_node.index !='0':
            chain_empty_list.append(start_node)
            concatenate(next,ax,chain_empty_list)
    chain_empty_list.append(start_node)



def create_chains(ax, nodes):
    start_nodes = nodes
    all_sequences = []
    for start_node in start_nodes:
        max_len = 1
        sequence = []
        concatenate(start_node,ax,sequence)
        if len(sequence)>max_len:
            max_len = len(sequence)
            longest_interconnected=sequence
            all_sequences.append(longest_interconnected)
    chains = get_chains(all_sequences)
    return chains

def draw_jj(ax,pos1,pos2):
    midpoint = (pos1+pos2)/2

    stroke_len = 0.3

    # one_end = inter1 + rotate(inter1,delta,-90)*total_width/2
    stroke1_beg = midpoint+stroke_len*np.array([-1,0])/2
    stroke1_end = midpoint+stroke_len*np.array([1,0])/2
    stroke2_beg = midpoint+stroke_len*np.array([0,-1])/2
    stroke2_end = midpoint+stroke_len*np.array([0,1])/2
    stroke1_beg = rotate_correct(midpoint,stroke1_beg,5)
    stroke1_end = rotate_correct(midpoint,stroke1_end,5)
    stroke2_beg = rotate_correct(midpoint,stroke2_beg,5)
    stroke2_end = rotate_correct(midpoint,stroke2_end,5)
    ax.plot([pos1[0],pos2[0]],[pos1[1],pos2[1]],lw=LINEWEIGHT,color=LINECOLOR)
    ax.plot([stroke1_beg[0],stroke1_end[0]],[stroke1_beg[1],stroke1_end[1]],lw=LINEWEIGHT,color=LINECOLOR)
    ax.plot([stroke2_beg[0],stroke2_end[0]],[stroke2_beg[1],stroke2_end[1]],lw=LINEWEIGHT,color=LINECOLOR)


def draw_device(ax,pos1,pos2,type):
    ax.plot([pos1[0],pos2[0]],[pos1[1],pos2[1]],color=LINECOLOR,lw=LINEWEIGHT)

def draw_scheleton(ax,chain,rot_angle,r0):
    delta = np.array([1.0, 0.0])
    ax.scatter(chain[0].pos[0],chain[0].pos[1], color = LINECOLOR,s=NODESIZE)
    ax.text(chain[0].pos[0]+0.1,chain[0].pos[1]+0.1,chain[0].index, ha='center')

    for i,link in enumerate(chain[1:]):
        link.pos+=(i+1)*delta
        elementary_width= 0.2
        total_width = (no_splits(link)-1)*elementary_width

        inter1 = link.pos+0.15*delta
        inter2 = link.pos+0.85*delta
        one_end = inter1 - total_width/2*np.array([0,1])

        link.pos = rotate(chain[0].pos,link.pos,rot_angle)
        inter1 = rotate(chain[0].pos,inter1,rot_angle)
        inter2 = rotate(chain[0].pos,inter2,rot_angle)

        ax.scatter(link.pos[0],link.pos[1], color = LINECOLOR,s=NODESIZE)
        ax.text(link.pos[0]+0.1,link.pos[1]+0.1,link.index, ha='center')

        # if i<len(chain)-1:
        #     # ax.plot([link.pos[0],inter1[0]],[link.pos[1],inter1[1]],color = LINECOLOR)
        #     # ax.plot([inter2[0],link.pos[0]+1],[inter2[1],link.pos[1]],color = LINECOLOR)
        #     for subbranch in range(no_splits(link)):
        #         one_end_rot = rotate(np.array([0,0]),one_end,rot_angle)+r0
        #         other_end = rotate(np.array([0,0]),one_end + delta*0.7,rot_angle)+r0
        #         # ax.plot([one_end_rot[0],inter1[0]],[one_end_rot[1],inter1[1]],color = LINECOLOR)
        #         # ax.plot([one_end_rot[0],other_end[0]],[one_end_rot[1],other_end[1]],color = LINECOLOR)
        #         # ax.plot([inter2[0],other_end[0]],[inter2[1],other_end[1]],color = LINECOLOR)
        #         one_end += elementary_width*np.array([0,1])

def assign_coords_and_draw(ax, nodes):
    chains = create_chains(ax,nodes)
    main_chain = find_longest(chains)
    

    delta = np.array([1,0])
    for chain in chains:
        if chain==main_chain:
            draw_scheleton(ax,chain,0,np.array([0,0]))
        elif chain!=main_chain and not is_loop(main_chain,chain):
            common_link = list(set(chain) & set(main_chain))[0]
            pos = common_link.pos
            
            if common_link == chain[0]:
                # draw_scheleton(ax,chain,-90,pos)
               for i,link in enumerate(chain[1:]):
                    link.pos+=(i+1)*delta
                    link.pos = rotate(np.array([0,0]),link.pos,-90)+pos

                    ax.scatter(link.pos[0],link.pos[1], color = LINECOLOR,s=NODESIZE)
                    ax.text(link.pos[0]+0.1,link.pos[1]+0.1, link.index, ha='center')

            elif common_link == chain[-1]:
                for i,link in enumerate(reversed(chain[:-1])):
                    link.pos=(i+1)*delta
                    link.pos = rotate(np.array([0,0]),link.pos,90)+pos
                    ax.scatter(link.pos[0],link.pos[1], color = LINECOLOR,s=NODESIZE)
                    ax.text(link.pos[0]+0.1,link.pos[1]+0.1, link.index, ha='center')

    ax.set_aspect('equal')
    ax.axis('off')

    
def draw_by_device(ax,devices,nodes):
    legend=[]
    for device in devices:
        pos1 = find_node(device.fro,nodes).pos
        pos2 = find_node(device.to,nodes).pos
        delta = pos2-pos1
        el_width = 0.24
        total_width = (device.no_subbranches-1)*el_width

        inter1 = pos1+0.15*delta
        inter2 = pos1+0.85*delta

        one_end = inter1 + rotate(inter1,delta,-90)*total_width/2
        offset = rotate(inter1,delta,90)*el_width
        one_end += device.subbranch*offset
        other_end = one_end+0.7*delta
        legend.append(device.symbol)


        ax.plot([pos1[0],inter1[0]],[pos1[1],inter1[1]],color=LINECOLOR,lw=LINEWEIGHT)
        ax.plot([inter2[0],pos2[0]],[inter2[1],pos2[1]],color=LINECOLOR,lw=LINEWEIGHT)
        ax.plot([inter1[0],one_end[0]],[inter1[1],one_end[1]],color=LINECOLOR,lw=LINEWEIGHT)
        ax.plot([other_end[0],inter2[0]],[other_end[1],inter2[1]],color=LINECOLOR,lw=LINEWEIGHT)
        draw_device(ax,one_end,other_end,device.type)

