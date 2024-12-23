import sys
import networkx as nx

def read_graph(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        edges = [e.strip().split("-") for e in data]
        network = nx.Graph()
        network.add_edges_from(edges)
        return network

if __name__ == "__main__":
    network = read_graph(sys.argv[1])
    nodes = network.nodes()
    cliques = set()
    for n in nodes:
        if n.startswith("t"):
            # find a clique of size 3
            neighbors = list(network.neighbors(n))
            for i in range(len(neighbors)):
                for j in range(i+1, len(neighbors)):
                    if network.has_edge(neighbors[i], neighbors[j]):
                        print(f"Found a clique of size 3 : {n} - {neighbors[i]} - {neighbors[j]}")
                        clique = [n, neighbors[i], neighbors[j]]
                        clique.sort()
                        cliques.add(tuple(clique))
    print(cliques)
    print(len(cliques))

    cliques = list(nx.clique.find_cliques(network))
    biggest = max(cliques, key=len)
    biggest.sort()
    print(",".join(biggest))
