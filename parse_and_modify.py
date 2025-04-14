import pandas as pd
import re


def parse_and_modify(filepath):
    with open(filepath,'r+') as f:
        content = f.readlines()
    
    metadata = {}
    with open(filepath, 'w') as f:
        for line in content:
            if line[0]=='#':
                doubledot = line.find(':')
                metadata[line[1:doubledot]]=line[doubledot+1:].strip()
            elif line[0]=='"':
                line = line.replace('","',';')
                line = line.replace('"',"")
                f.write(line)
            else:
                comma_ids = [match.start() for match in re.finditer(',', line)]
                indices = [i for i in range(len(comma_ids)) if i%2==0]
                comma_ids_new = []
                for i in indices:
                    comma_ids_new.append(comma_ids[i])
            
                for comma_idx in comma_ids_new:
                    line_list = list(line)
                    line_list[comma_idx] = '.'
                    line = ''.join(line_list)
                line = line.replace(",",";")
                f.write(line)
    return metadata

# metadata = parse_and_modify(filepath)




