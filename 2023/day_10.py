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

def is_valid(i,j,max_l,max_c):
    return (i>= 0) and (j>=0) and (i < max_l) and (j < max_c)

def expand(i,j,cycle_map):
    n,p = cycle_map.shape
    queue = [(i,j)]
    to_mark = [(i,j)]
    cycle_map[i,j] = 3
    border_cycle = True 
    while(queue):
        to_check = queue.pop()
        if cycle_map[to_check] == 0:
            to_mark.append(to_check)
            cycle_map[to_check] = 3
        i,j = to_check
        for neigh in [(i-1,j), (i+1,j),(j-1,i),(j+1,i)]:
            if not is_valid(*neigh, n,p):
                border_cycle = False
            else:
                if cycle_map[neigh] == 0:
                    queue.append(neigh)
                if cycle_map[neigh]==-1:
                    border_cycle = False
                    
    return to_mark, border_cycle
    # pour chaque noeud non marqué, extension.
    # si l'ensemble de la bordure est dans le cycle -> ca compte
    # sinon, marqué + ça compte pas 
    
    
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
                    edges.append(((i,j),neigh))
                    
    return nodes, pipe_map, start, edges

def first():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        nodes, pipe_map, start,edges = get_map(content)
        # print(pipe_map)
        # creation du graphe
        G= nx.Graph()
        for n,attr in nodes.items():
            # print(attr)
            G.add_node(n,attr=attr)
        # nettoyage des aretes
        clean_edges = []
        for e in edges:
            if (e[1],e[0]) in edges:
                clean_edges.append(e)
            if e[1] == start:
                clean_edges.append(e)
        G.add_edges_from(clean_edges)
        for n in G.nodes():
             print(f"{n} : {G[n]}")
        #start = nodes[start]['node']
        #cycles = nx.cycle_basis(G,root=start)
        # print(f"cycle from {start}")
        cycle = nx.find_cycle(G,source=start)
        print(cycle)
        nodes_cycle = [e[0] for e in cycle]

        # https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
        from matplotlib.path import Path
        nb_inside= 0
        polygon = Path(nodes_cycle)
        nb_l,nb_c = len(content), len(content[0])
        for i in range(nb_l):
            for j in range(nb_c):
                if (i, j) in nodes_cycle:
                    continue
                if polygon.contains_point((i, j)):
                    nb_inside  += 1

        print(nb_inside)
        # for cycle in cycles:
        #     if start in cycle:
        #         idx_start = cycle.index(start)
        # len_cycle = len(cycle)
        # print(len_cycle)
        # print((len_cycle//2))
        # nb_l,nb_c = len(content), len(content[0])
        # cycle_map = np.zeros((nb_l,nb_c))
        # for e in cycle:
        #     cycle_map[e[1]] =1 
        # # parcours des neouds non inclus dans le cycle
        # # pour chaque noeud non marqué, extension.
        # print("extension")
        # nb_inside = 0
        # for i in range(nb_l):
        #     for j in range(nb_c):
        #         if cycle_map[i,j] == 0:
        #             to_mark, border_cycle = expand(i,j,cycle_map)
        #             #print(to_mark,border_cycle)
        #             marker = -1
        #             if border_cycle:
        #                 nb_inside += len(to_mark)
        #                 marker = 2
        #             for c in to_mark:
        #                 cycle_map[c]=marker
                        
        # # si l'ensemble de la bordure est dans le cycle -> ca compte
        # # sinon, marqué + ça compte pas 
        # #print(cycle_map)
        # print(nb_inside)
        # plt.matshow(cycle_map)
        # plt.colorbar()
        # plt.show()
        # np.save("./map",cycle_map)
        #nx.draw_networkx(G,with_labels=True)
        #plt.show()
        #print(G[start])
if __name__ == '__main__':
    res = first()
    print(res)
