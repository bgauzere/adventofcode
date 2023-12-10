from dataclasses import dataclass
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.ifm

import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

@dataclass(frozen=True)
class Node():
    i:int
    j:int

    def __eq__(self,other):
        return self.i == other.i and self.j == other.j
    

def parse_pipe(pipe, i,j):
    neighbours = []
    # north
    if pipe in ["|","L","J"]:
         neighbours.append((i-1,j))
    if pipe in ["|","7","F"]: #south
        neighbours.append((i+1,j))
    if pipe in ["-","J","7"]: #west
        neighbours.append((i,j-1))
    if pipe in ["-","L","F"]:
        neighbours.append((i,j+1))
    return neighbours

def get_map(content):
    n = len(content)
    p = len(content[0])
    pipe_map = []
    start = None
    nodes = {}
    edges = []
    for i,line in enumerate(content):
        pipe_map.append([])
        for j, point in enumerate(line):
            if point == ".":
                pipe_map[i].append(None)
                continue
            elif point == "S":
                start = (i,j)
                pipe_map[i].append(("S"))
                
                nodes[(i,j)] = {'node' : Node(i,j), 'coords':[i,j], 'neigh': [],'start' : True}
            else: #pipe
                pipe_map[i].append(("P"))
                neighs = parse_pipe(point,i,j)
                print(f"{point=}, {i=},{j=},{neighs=}")
                nodes[(i,j)] = {'node':Node(i,j),'coords' : [i,j], 'neigh': neighs,'start' : False}
                for neigh in neighs:
                    edges.append((i,j),neigh)
                    
    return nodes, pipe_map, start, edges

def first():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        nodes, pipe_map, start = get_map(content)
        # print(pipe_map)
        # creation du graphe
        G= nx.DiGraph()
        for n,attr in nodes.items():
            # print(attr)
            G.add_node(attr['node'],attr=attr)
        for n,attr in nodes.items():
            for neigh in attr["neigh"]:
                if neigh in nodes:
                    G.add_edge(nodes[n]['node'],nodes[neigh]['node'])
                    if neigh == start :
                        G.add_edge(nodes[neigh]['node'],nodes[n]['node'])
        nb_l,nb_c = len(content), len(content[0])
        cycle_map = np.zeros((nb_l,nb_c))
        # for n in G.nodes():
        #     print(f"{n} : {G[n]}")
        start = nodes[start]['node']
        cycles = nx.cycle_basis(G,root=start)
        print(f"cycle from {start}")
        for cycle in cycles:
            if start in cycle:
                idx_start = cycle.index(start)
                len_cycle = len(cycle)
                print(len_cycle)
                print((len_cycle//2)+1)
            #cycle_map[e[1]] =1 
            
        #print(cycle_map)
        #nx.draw_networkx(G,with_labels=True)
        #plt.show()
        #print(G[start])
if __name__ == '__main__':
    res = first()
    print(res)
