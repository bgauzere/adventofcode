from utils import read_content
import logging
import networkx as nx
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import numpy as np
from itertools import cycle

@dataclass(frozen=True)
class Node():
    line:int
    col:int

    def get_neighbours(self, garden_map):
        neighbours = [(self.line-1,self.col),(self.line+1,self.col),(self.line,self.col-1),(self.line,self.col+1)]
        return [Node(i,j) for (i,j) in neighbours]
    

class GardenMap():
    def __init__(self, map_lst):
        self.map = [list(line) for line in map_lst]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.reached = []
        self.rocks = []
        self.marked = []
        for line, line_str in enumerate(map_lst):
            for col, point in enumerate(list(line_str)):
                if point == "#":
                    self.rocks.append(Node(line,col))
        
    def is_rock(self, node:Node):
        return Node(node.line % self.height, node.col % self.width) in self.rocks
    
    def mark(self,node:Node):
        self.marked.append(node)

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
        #self.reached.extend(new_reached)
        #print(self.marked)
        #print(len(self.marked))
    
    def __str__(self):
        to_print = self.map.copy()
        print(id(to_print),id(self.map))
        for node in self.marked:
            to_print[node.line][node.col] = "O"

        return "\n".join(["".join([str(c) for c in l]) for l in to_print])



    
def parse_content(content):
    ### on va se créer un graphe
    n,p = len(content), len(content[0])
    # print(n,p)
    # n,p = n//3, p//3
    # content = [l[:p] for l in content[:n]]
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
                #logging.info(f"{node} <-> {neighbour}")
                edges.append((node,neighbour))
    #print(edges)
    #G.add_edges_from(edges)
    ##nx.draw_networkx(G)
    #plt.show()
    return G, garden_map, start_node

def firstV2(G,garden_map,start_node,nb_steps):
    #reached = [start_node]
    garden_map.mark(start_node)
    sequence = []
    for step in range(1,nb_steps):
        garden_map.propagate()
        sequence.append(len(set(garden_map.marked)))
        print(f"step {step} : {len(set(garden_map.marked))}")
        #print(len(set(garden_map.reached)))
        #print(garden_map)
    return sequence

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, format=' %(message)s')
    content = read_content()
    # print(content)
    #G,garden_map,start_node = parse_content(content)
    #data = firstV2(G,garden_map,start_node,100)
    #start_node = Node(5,5)
    #firstV2(G,garden_map,start_node,1000)

    import matplotlib.pyplot as plt
    with open("./test_21_2","r") as f:
        content = f.readlines()
        content = [l.split() for l in content]

        data = np.array([[int(l[1]), int(l[3])]  for l in content],dtype=int) 
        data = data[:,1]
        #plt.plot(data[:,0],data[:,1], 'o-')
        #print(np.diff(data[:,1]))
        
        #plt.yscale('log')
        #plt.show()
        diff = np.diff(data)
        plt.plot(diff, 'o-')
        plt.show()
        diff_2 = np.diff(diff)
        plt.plot(diff_2, 'o-')
        plt.show()
        
        a = diff_2[49:60] # 1
        b = diff_2[60:71] # 2
        c = diff_2[71:82] # 3
        d = diff_2[82:93] # 4
        print(f"{a = }")
        print((b-a)) # constante
        print((c-b)) # constante
        
        print(f"{seq_derive_second = }")
        l_seq = len(seq_derive_second)
        print(f"{l_seq = }")
        start_idx = 49
        start_value = data[start_idx]
        print(f"{seq_derive_second}")
        print("-----------------")
        cur = data[49]
        cur_diff = diff[49]
        cur_diff_2 = diff_2[49]
        idx = 49
        computed = list(data[:49])
        computed_diff = diff[:49]
        computed_diff_2 = diff_2[:49]
        iter_seq = cycle(seq_derive_second)
        # while(idx < 55):
        
        #     # cur_diff_2 = computed_diff_2[idx:idx+l_seq]
        #     # cur_diff = computed_diff[idx:idx+l_seq]
        #     # cur = computed[idx:idx+l_seq]
        #     item = next(iter_seq)
        #     cur_diff_2 = cur_diff_2 + item #diff_2[60:71]
        #     print(f"{cur_diff_2 = }, {diff_2[idx] = }, {item =}")
        #     #print(f"{next_diff_2 = }")
        #     cur_diff = cur_diff + cur_diff_2
        #     cur = cur + cur_diff
        #     computed.append(cur)
        #     idx += 1
        
        # for i,v in enumerate(computed[49:]):
        #     print(f"{i+1} : {v}")
        idx = 49
        next_diff_2 = diff_2[:idx+l_seq]
        #next_diff_2 = diff_2[idx:idx+l_seq] + seq_derive_second  
        next_diff = [diff[idx+l_seq]]
        next = [data[idx+l_seq,1],data[idx+l_seq+1,1]]
        while (idx < 26501365):
            next_diff_2 = [a+b for a,b in zip(next_diff_2[-l_seq:],seq_derive_second)]
            # print(f"v1  : { next_diff_2}")
            # next_diff_2 = diff_2[idx:idx+l_seq]
            # next_diff_2 = diff_2[idx:idx+l_seq] + seq_derive_second  
            # print(f"v2 : {next_diff_2}")
            
            next_diff = [next_diff[-1]]
            # print(f"V1 : {next_diff}")
            
            # next_diff = [diff[idx+l_seq]]
            # print(f"V2 : {next_diff}")
            
            #next_diff = [diff[60]]
            for d in next_diff_2:
                next_diff.append(next_diff[-1]+d)

            next = [next[-2]]
            # print(f"V1 : {next}")
            # next = [data[idx+l_seq,1]]
            # print(f"V2 : {next}")
            # # #next = [data[60,1]]
            for d in next_diff:
                #print(f"{next[-1] = }, {d =}")
                next.append(next[-1]+d)
            for i in range(l_seq):
                print(f"{idx+i+l_seq+1} : {next[i]}")
            
            idx = idx+l_seq
        # next_diff_2 = diff_2[:idx+l_seq]
        # next_diff_2 = diff_2[idx:idx+l_seq] + seq_derive_second  
        # next_diff = [diff[idx+l_seq]]
        
        # #next_diff = [diff[60]]
        # for d in next_diff_2:
        #      next_diff.append(next_diff[-1]+d)
        # next = [data[idx+l_seq,1]]
        # #next = [data[60,1]]
        # for d in next_diff:
        #      next.append(next[-1]+d)
        # print(next)
        # print(list(data[idx+l_seq:idx+l_seq*2,1]))

        # nnext_diff_2 = next_diff_2 + seq_derive_second
        # nnext_diff = [next_diff[-2]]
        # for i in range(1,11):
        #       nnext_diff.append(nnext_diff[-1]+nnext_diff_2[i-1])
        # nnext = [next[-2]]
        # for i in range(1,11):
        #       nnext.append(nnext[-1]+nnext_diff[i-1])
        # print(nnext)
        # print(data[71:82,1])
        
        
        # for i in range(1,10):

        #     print(f"{start_value + i*seq_derive_second[0] = }")
        
        # print(data[49,1],data[50,1])