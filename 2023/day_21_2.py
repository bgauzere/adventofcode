from utils import read_content
import logging
import networkx as nx
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import numpy as np
from itertools import cycle
import pickle
from collections import defaultdict


@dataclass(frozen=True)
class Node():
    line:int
    col:int

    def get_neighbours(self):
        neighbours = [(self.line-1,self.col),(self.line+1,self.col),(self.line,self.col-1),(self.line,self.col+1)]
        return [Node(i,j) for (i,j) in neighbours]
    

class GardenMap():
    def __init__(self, map_lst):
        self.map = [list(line) for line in map_lst]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.reached = None
        self.rocks = set()
        self.marked = None
        for line, line_str in enumerate(map_lst):
            for col, point in enumerate(list(line_str)):
                if point == "#":
                    self.rocks.add(Node(line,col))
        
    def is_rock(self, node:Node):
        #return Node(node.line % self.height, node.col % self.width) in self.rocks
        return Node(node.line, node.col) in self.rocks
    
    def mark(self,node:Node):
        self.marked.append(node)

    def is_garden(self, node:Node):
        return not self.is_rock(node)
    
    def is_valid(self, node:Node):
        if node.line >= self.height or node.line < 0:
            return False
        if node.col >= self.width or node.col < 0:
            return False
        return True
    
    def propagate(self,start_point,nb_steps):
        self.reached = set()
        queue = [(start_point,0)]
        reach_at_step = defaultdict(int)
        while queue:
            node, dist = queue.pop(0)
            #if (node,dist) in self.reached or dist == nb_steps +1:
            if node in self.reached or dist == nb_steps +1:
                continue
            reach_at_step[dist] += 1
            #self.reached.add((node,dist))
            self.reached.add(node)
            for neighbour in node.get_neighbours():
                if self.is_garden(neighbour) and self.is_valid(neighbour):
                    queue.append((neighbour,dist+1))
        return reach_at_step
    
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
    # G = nx.Graph()
    # nodes  = []  
    start_node = None
    for line, line_str in enumerate(content):
        for col, point in enumerate(list(line_str)):
            if point == "S":# or point == "S":
                node = Node(line,col)
                # nodes.append(node)
                # if point == "S":
                start_node = node
    # G.add_nodes_from(nodes)
    # edges = []
    # for node in nodes:
        # for neighbour in node.get_neighbours(garden_map):
            # if garden_map.is_garden(neighbour):
            #    logging.info(f"{node} <-> {neighbour}")
                # edges.append((node,neighbour))
    #print(edges)
    #G.add_edges_from(edges)
    ##nx.draw_networkx(G)
    #plt.show()
    return garden_map, start_node

def firstV2(garden_map,start_node,nb_steps):
    #reached = [start_node]
    nb_reached = garden_map.propagate(start_node,nb_steps)
    #print(nb_reached)
    #print(garden_map.reached)
    return nb_reached


def analyse():
    #data = pickle.load(open("./test_21_2","rb"))
    data = {0: 1, 1: 4, 2: 6, 3: 16, 4: 20, 5: 35, 6: 41, 7: 60, 8: 72, 9: 91, 10: 105, 11: 126, 12: 147, 13: 173, 14: 198, 15: 223, 16: 254, 17: 283, 18: 316, 19: 340, 20: 378, 21: 411, 22: 453, 23: 486, 24: 532, 25: 573, 26: 620, 27: 664, 28: 712, 29: 757, 30: 810, 31: 866, 32: 923, 33: 980, 34: 1036, 35: 1099, 36: 1160, 37: 1225, 38: 1296, 39: 1359, 40: 1429, 41: 1493, 42: 1574, 43: 1637, 44: 1723, 45: 1783, 46: 1874, 47: 1936, 48: 2026, 49: 2098, 50: 2189, 51: 2277, 52: 2362, 53: 2457, 54: 2545, 55: 2634, 56: 2720, 57: 2815, 58: 2914, 59: 3020, 60: 3131, 61: 3238, 62: 3380, 63: 3499, 64: 3646, 65: 3759, 66: 3910, 67: 4027, 68: 4182, 69: 4269, 70: 4419, 71: 4519, 72: 4671, 73: 4773, 74: 4932, 75: 5049, 76: 5200, 77: 5303, 78: 5472, 79: 5587, 80: 5749, 81: 5856, 82: 6017, 83: 6148, 84: 6316, 85: 6450, 86: 6620, 87: 6747, 88: 6916, 89: 7046, 90: 7222, 91: 7362, 92: 7528, 93: 7668, 94: 7841, 95: 8002, 96: 8185, 97: 8346, 98: 8527, 99: 8689, 100: 8867, 101: 9035, 102: 9211, 103: 9393, 104: 9567, 105: 9757, 106: 9923, 107: 10117, 108: 10300, 109: 10471, 110: 10668, 111: 10837, 112: 11049, 113: 11220, 114: 11443, 115: 11630, 116: 11839, 117: 12026, 118: 12235, 119: 12440, 120: 12651, 121: 12860, 122: 13072, 123: 13298, 124: 13485, 125: 13717, 126: 13897, 127: 14138, 128: 14327, 129: 14567, 130: 14783, 131: 15012, 132: 15263, 133: 15464, 134: 15723, 135: 15916, 136: 16182, 137: 16371, 138: 16644, 139: 16861, 140: 17118, 141: 17353, 142: 17599, 143: 17856, 144: 18097, 145: 18351, 146: 18583, 147: 18859, 148: 19089, 149: 19365, 150: 19591, 151: 19874, 152: 20104, 153: 20379, 154: 20634, 155: 20895, 156: 21171, 157: 21438, 158: 21709, 159: 21979, 160: 22236, 161: 22515, 162: 22795, 163: 23089, 164: 23366, 165: 23652, 166: 23938, 167: 24236, 168: 24512, 169: 24834, 170: 25096, 171: 25406, 172: 25665, 173: 26006, 174: 26259, 175: 26601, 176: 26856, 177: 27204, 178: 27459, 179: 27802, 180: 28064, 181: 28398, 182: 28686, 183: 29028, 184: 29329, 185: 29659, 186: 29946, 187: 30278, 188: 30568, 189: 30916, 190: 31230, 191: 31610, 192: 31917, 193: 32349, 194: 32705, 195: 33157, 196: 33496, 197: 33945}
    data = list([data[k] for k in range(0,131+65+1)])
    import matplotlib.pyplot as plt
    
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
    # si le range du test est 11, celle ci doit etre 131...
    start = 65
    l = 131
    # for start in range(63,67):
    #     for l in range(130,133):
    #         a = diff_2[start:start+l] # 1
    #         b = diff_2[start+l:start+l+l] # 2
    #         c = diff_2[start+l+l:start+l+l+l] # 3
    #         print(b-a)
    #         print(c-b)
            
    #         if all((b-a) == (c-b)):
    #             print(start,l)
    #             breakpoint()
    # a = diff_2[49:60] # 1
    # b = diff_2[60:71] # 2
    # c = diff_2[71:82] # 3
    # d = diff_2[82:93] # 4
    # print(f"{a = }")
    # print((b-a)) # constante
    # print((c-b)) # constante
    
    # print(f"{seq_derive_second = }")
    
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

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, format=' %(message)s')
    content = read_content()
    # print(content)
    garden_map,start_node = parse_content(content)
    reached_at_step = firstV2(garden_map,start_node,250)
    #data = list([data[k] for k in range(0,131+65+1)])
    #pickle.dump(data,open("./test_21_2","wb"))
    #analyse()
    #print(garden_map.reached) 
    # inspiré de https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
    p1 = sum([v if k <= 64 and k %2 == 0 else 0 for k,v in reached_at_step.items()])
    print(f"{p1 = }")

    even_full = sum([v if k %2 == 0 else 0 for k,v in reached_at_step.items()])
    odd_full = sum ([v if k %2 == 1 else 0 for k,v in reached_at_step.items()])

    even_corners = sum([v if k %2 == 0 and k > 65 else 0 for k,v in reached_at_step.items()])
    odd_corners = sum([v if k %2 == 1 and k > 65 else 0 for k,v in reached_at_step.items()])
    n = int((26501365 - ((garden_map.height-1) / 2)) / (garden_map.height))
    print(f"{n = }")
    p2 = ((n+1)*(n+1)) * odd_full + (n*n) * even_full - (n+1) * odd_corners + n * even_corners
    print(f"{p2 = }")
    #start_node = Node(5,5)
    #firstV2(G,garden_map,start_node,1000)
