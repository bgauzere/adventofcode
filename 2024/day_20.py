import sys
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter


def read_graph(filename):
    with open(filename) as f:
        content = f.readlines()
        graph = nx.Graph()
        for i,line in enumerate(content):
            for j, item  in enumerate(line.strip()):
                if item == "S":
                    start = (i,j)
                    graph.add_node(start)
                if item == "E":
                    end = (i,j)
                    graph.add_node(end)
                if item == ".":
                    graph.add_node((i,j))
                if item in [".","S","E"]:
                    for x,y in [(i+1,j),(i,j+1),(i-1,j),(i,j-1)]:
                        if 0 <= x < len(content) and 0 <= y < len(content[0]) and content[x][y] == ".":
                            graph.add_edge((i,j),(x,y))
        return graph, start, end
    
def find_shortcuts(graph, path, limit = 0):
    shortcuts = {}
    for k,node in enumerate(path):
        i,j = node
        for dir in [(0,1), (0,-1), (1,0), (-1,0)]:
            x,y = i+dir[0], j+dir[1]
            if (x,y) not in graph:
                x,y = x+dir[0], y+dir[1]
                if (x,y) in path[k:]:
                    index = path[k:].index((x,y))
                    length = index - 2
                    if length >= limit:
                        shortcuts[((i,j),(x,y))] = length
    return shortcuts
                   
if __name__ == "__main__":
    graph, start, end = read_graph(sys.argv[1])
    limit = 0
    if len(sys.argv) == 3:
        limit = int(sys.argv[2])
    #print(start, end)
    # nx.draw(graph, with_labels=True)
    # plt.show()
    path = nx.shortest_path(graph,start,end)
    print(len(path))
    shortcuts = find_shortcuts(graph, path, limit)
    print(len(shortcuts))
    # for key, value in shortcuts.items():
    #     print(f"{key} : {value}")
    # counter = Counter(shortcuts.values())
    # print(sorted(counter.items()))

"""Pour la partie 2, chercher un path dans le graph complémentaire (celui des #) de taille max 20 noeuds entre chaque noeud 
du path et l'ensemble des noeuds du path a partir de la position + 100
Donc 9000*9000 = 81 millions de paires de noeuds à testerd
"""