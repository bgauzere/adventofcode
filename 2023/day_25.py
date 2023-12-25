from utils import read_content
import networkx as nx 
import matplotlib.pyplot as plt
import numpy as np

def first(content):
    G = nx.Graph()
    for line in content:
        node, edges = line.split(":")
        print(f"{node}")
        G.add_node(node)
        for edge in edges.strip().split(" "):
            G.add_edge(node, edge)
            print(f"\t {node}-{edge}")
    
    L = nx.laplacian_matrix(G)
    values, vectors = np.linalg.eigh(L.todense())
    print(values)
    features = vectors[:,1]
    features = [1 if f > 0 else 0 for f in features]
    
    #nx.draw_networkx(G, with_labels=True,node_color=features, cmap=plt.cm.Blues)
    #plt.show()

    for node, feat in zip(G.nodes, features):
        print(f"{node} : {feat}")
    
    components, nb = np.unique(features, return_counts=True)
    
    return  nb[0] * nb[1]

if __name__ == "__main__":
    content = read_content()
    print(first(content))