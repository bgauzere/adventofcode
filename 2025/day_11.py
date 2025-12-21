import sys
import networkx as nx
import logging
import matplotlib.pyplot as plt
from tqdm import tqdm 

logging.basicConfig(level=logging.DEBUG)

def second():
    # Read the graph
    graph = {}
    with open(sys.argv[2],"r") as f:
        contents = f.readlines()
        for l in contents:
            l=l.strip()
            start = l.split(":")[0]
            neighbors = l.split(" ")[1:]
            graph[start] = neighbors
    
    # degrees = {n:len(graph[n]) for n in graph.keys()}
    # print(sorted(degrees.items(), key=lambda x: x[1], reverse=True))

    # in_degrees = {}
    # for node, neighbors in graph.items():
    #     for neigh in neighbors:
    #         if neigh not in in_degrees:
    #             in_degrees[neigh] = 0
    #         in_degrees[neigh] += 1
    # logging.debug(sorted(in_degrees.items(), key=lambda x: x[1], reverse=True))
    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neigh in neighbors:
            G.add_edge(node, neigh)
    
    nodes = list(G.nodes)
    adj_matrix = nx.adjacency_matrix(G, nodelist=nodes)
    
    id_dac = nodes.index("dac")
    id_fft = nodes.index("fft")
    print(adj_matrix[id_dac, id_fft])
    p_adj_matrix = adj_matrix.copy()
    nb_paths_svr_to_fft = 0
    nb_paths_fft_to_dac = 0
    nb_paths_dac_to_out = 0
    
    for _ in tqdm(range(1000)):
        p_adj_matrix = p_adj_matrix@ adj_matrix
        if p_adj_matrix[id_fft, id_dac] > 0:
            nb_paths_fft_to_dac += p_adj_matrix[id_fft, id_dac]
        if p_adj_matrix[id_dac, nodes.index("out")] > 0:
            nb_paths_dac_to_out += p_adj_matrix[id_dac, nodes.index("out")]
        if p_adj_matrix[nodes.index("svr"), id_fft] > 0:
            nb_paths_svr_to_fft += p_adj_matrix[nodes.index("svr"), id_fft]
    logging.debug(f"nb_paths_svr_to_fft: {nb_paths_svr_to_fft}")
    logging.debug(f"nb_paths_fft_to_dac: {nb_paths_fft_to_dac}")
    logging.debug(f"nb_paths_dac_to_out: {nb_paths_dac_to_out}")
    return nb_paths_svr_to_fft * nb_paths_fft_to_dac * nb_paths_dac_to_out
    # nx.draw_networkx(G)
    # plt.show()
    # queue = ["fft"]
    # nb_paths = 0
    # while queue:
    #     current = queue.pop()
    #     if current == "out":
    #         nb_paths += 1
    #         logging.debug(nb_paths)
    #     else:
    #         queue.extend(graph[current])
    # return nb_paths


def first():
    # Read the graph
    graph = {}
    with open(sys.argv[1],"r") as f:
        contents = f.readlines()
        for l in contents:
            l=l.strip()
            start = l.split(":")[0]
            neighbors = l.split(" ")[1:]
            graph[start] = neighbors
            
    # DFS to find the paths
    
    logging.debug(graph["you"])
    queue = ["you"]
    nb_paths = 0
    while queue:
        current = queue.pop()
        if current == "out":
            nb_paths += 1
        else:
            queue.extend(graph[current])
    return nb_paths
if __name__ == "__main__":
    print(first())
    print(second())