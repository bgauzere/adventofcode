from utils import read_content
import logging
import networkx as nx
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import numpy as np

@dataclass(frozen=True)
class Node():
    line:int
    col:int

    def get_neighbours(self, garden_map):

        neighbours = [(self.line-1,self.col),(self.line+1,self.col),(self.line,self.col-1),(self.line,self.col+1)]
        good_neighbours = []
        for (i,j) in neighbours:
            potential_neighbour = Node(i,j)
            if garden_map.is_valid(potential_neighbour):
                good_neighbours.append(potential_neighbour)
            else:
                # wrap around 
                i,j = potential_neighbour.line, potential_neighbour.col
                if i < 0:
                    i = garden_map.height-1
                if i >= garden_map.height:
                    i = 0
                if j >= garden_map.width:
                    j = 0
                if j < 0:
                    j = garden_map.width-1
                good_neighbours.append(Node(i,j))
        return good_neighbours
    

class GardenMap():
    def __init__(self, map_lst):
        self.map = [list(line) for line in map_lst]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.marked = None
        self.rocks = []
        for line, line_str in enumerate(map_lst):
            for col, point in enumerate(list(line_str)):
                if point == "#":
                    self.rocks.append(Node(line,col))
        
    def is_rock(self, node:Node):
        return node in self.rocks
    
    def mark(self,node:Node):
        if self.marked is None:
            self.marked = [node]
        else:
            self.marked.append(node)

    def is_valid(self, node:Node):
        if node.line >= self.height or node.line < 0:
            return False
        if node.col >= self.width or node.col < 0:
            return False
        return True
        
    def is_garden(self, node:Node):
        return not self.is_rock(node)

    def propagate(self):
        assert(self.marked is not None)
        new_reached = []
        for start in self.marked:
            for neighbour in start.get_neighbours(self):
                if self.is_garden(neighbour):
                    new_reached.append(neighbour)
        self.marked = list(set(new_reached))
        print(self.marked)
        print(len(self.marked))
    
    def __str__(self):
        to_print = self.map.copy()
        print(id(to_print),id(self.map))
        for node in self.marked:
            to_print[node.line][node.col] = "O"

        return "\n".join(["".join([str(c) for c in l]) for l in to_print])



    
def parse_content(content):
    ### on va se créer un graphe
    n,p = len(content), len(content[0])
    print(n,p)
    n,p = n//3, p//3
    content = [l[:p] for l in content[:n]]
    garden_map = GardenMap(content)
    G = nx.Graph()
    nodes  = []  
    start_node = None
    for line, line_str in enumerate(content):
        for col, point in enumerate(list(line_str)):
            if point == "." or point == "S":
                node = Node(line,col)
                nodes.append(node)
                if point == "S":
                    start_node = node
    G.add_nodes_from(nodes)
    edges = []
    for node in nodes:
        for neighbour in node.get_neighbours(garden_map):
            if garden_map.is_garden(neighbour):
                logging.info(f"{node} <-> {neighbour}")
                edges.append((node,neighbour))
    #print(edges)
    G.add_edges_from(edges)
    nx.draw_networkx(G)
    plt.show()
    return G, garden_map, start_node

def firstV2(G,garden_map,start_node,nb_steps):
    #reached = [start_node]
    garden_map.mark(start_node)
    for step in tqdm(range(nb_steps)):
        #print(f"step {step} :")
        garden_map.propagate()
        #print(garden_map)
    
def first(G,garden_map,start_node):
    nb_steps = 6
    adj = nx.adjacency_matrix(G,nodelist=G.nodes())
    adj_power = adj
    #for i in range(nb_steps-1):
    #    adj_power = adj_power@adj
    while (nb_steps > 1):
         print(nb_steps)
         adj_power = adj_power@adj_power
         nb_steps = nb_steps/2
    #adj_power = adj_power @ adj
    #print("done !")
    adj_m_power = np.linalg.matrix_power(adj.todense(), 2)
    #adj_m_power = adj_steps.todense()
    print("done !")
    idx_start = list(G.nodes()).index(start_node)
    adj_power = adj_power.todense()
    print(adj_power[idx_start,idx_start])
    print(adj_power[:,idx_start])
    print(adj_power[idx_start,:])
    print(np.sum(adj_power[idx_start,:] > 0) - adj_power[idx_start,idx_start])
    #print(np.sum(adj_m_power[idx_start,:] > 0))
    #print(np.allclose(adj_power, adj_m_power))

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, format=' %(message)s')
    content = read_content()
    # print(content)
    G,garden_map,start_node = parse_content(content)
    # firstV2(G,garden_map,start_node,64)
    start_node = Node(6,5)
    firstV2(G,garden_map,start_node,64)

    # import matplotlib.pyplot as plt

    # test_21 = np.loadtxt("./test_21",delimiter=",",dtype=int)
    # x = test_21
    # plt.plot(x[:,0],x[:,1], 'o-')
    # #plt.yscale('log')
    # plt.show()
