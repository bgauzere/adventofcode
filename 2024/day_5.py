import sys
import numpy as np

import networkx as nx

import matplotlib.pyplot as plt


def first(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        g = nx.DiGraph()
        i = 0
        flag_first_part = True
        # parse first part, define the graph
        while flag_first_part:
            line = data[i].strip()
            if len(line) == 0:
                flag_first_part = False
                i += 1
                break
            line = line.split("|")
            g.add_edge(line[0], line[1])
            print(f"edge : {line[0]}, {line[1]}")
            i += 1
        # print(nx.is_directed_acyclic_graph(g))
        # for p in nx.simple_cycles(g):
        #     print(p)
        #nx.draw(g, with_labels=True)
        #plt.show()
        #ordered_nodes = list(nx.topological_sort(g))
        #print(ordered_nodes)
        #nodes_to_pos = {node:i for i,node in enumerate(ordered_nodes)}
        # parse second part, check the lists
        result = 0
        while i < len(data):
            line = data[i].strip()
            nodes = line.split(",")
            if check_path(g,nodes):#,nodes_to_pos):
                #print(f"Path {nodes} is valid")
                middle = int(nodes[len(nodes)//2])
                print(f"{nodes},Middle node : {middle}")
                result += int(nodes[len(nodes)//2])
            #else:
                #print(f"Path {nodes} is invalid")
            i += 1
    print(result)

def check_path(g, nodes):#, nodes_to_pos):
    cur_g = nx.subgraph(g, nodes)
    for i in range(len(nodes)-1):
        if not nx.has_path(cur_g, nodes[i], nodes[i+1]):
            return False
    return True

def correct_path(g, nodes): #, nodes_to_pos):
    cur_g = nx.subgraph(g, nodes)
    ordered_nodes = list(nx.topological_sort(cur_g))
    return int(ordered_nodes[len(ordered_nodes)//2])

def second(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        g = nx.DiGraph()
        i = 0
        flag_first_part = True
        # parse first part, define the graph
        while flag_first_part:
            line = data[i].strip()
            if len(line) == 0:
                flag_first_part = False
                i += 1
                break
            line = line.split("|")
            g.add_edge(line[0], line[1])
            print(f"edge : {line[0]}, {line[1]}")
            i += 1
       
        result = 0
        while i < len(data):
            line = data[i].strip()
            nodes = line.split(",")
            if not check_path(g,nodes):
                result += correct_path(g,nodes)
            i += 1
    print(result)

if __name__ == "__main__":
    second(sys.argv[1])