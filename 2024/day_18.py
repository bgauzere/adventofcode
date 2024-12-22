import sys 
import networkx as nx


def read_graph(filename, size, nb_bytes):
    with open(filename) as f:
        data = f.readlines()
        length = len(data)
        nodes = [tuple([int(n) for n in line.strip().split(",")]) for line in data]
        graph = nx.Graph()
        for i in range(size):
            for j in range(size):
                graph.add_node((i,j))
        
        for i in range(size):
            for j in range(size):
                if i + 1 < size:
                    graph.add_edge((i,j),(i+1,j))
                if j + 1 < size:
                    graph.add_edge((i,j),(i,j+1))
                if i -1 >= 0:
                    graph.add_edge((i,j),(i-1,j))
                if j - 1 >= 0:
                    graph.add_edge((i,j),(i,j-1))
        for i,j in nodes[:nb_bytes]:
            graph.remove_node((i,j))
        return graph, length, nodes

if __name__ == "__main__":
    filename = sys.argv[1]
    size = int(sys.argv[2])
    nb_bytes = int(sys.argv[3])
    graph, length, nodes = read_graph(filename, size, nb_bytes)

    print(nx.shortest_path_length(graph,(0,0),(size-1,size-1)))

    # recherche dichotomique de nb_bytes
    min_bytes = nb_bytes
    max_bytes = length

    while min_bytes < max_bytes:
        nb_bytes = (min_bytes + max_bytes) // 2
        graph, length, nodes= read_graph(filename, size, nb_bytes)
        print(nb_bytes)
        #print(nx.shortest_path_length(graph,(0,0),(size-1,size-1)))
        if not nx.has_path(graph,(0,0),(size-1,size-1)):
            max_bytes = nb_bytes
        else:
            min_bytes = nb_bytes + 1
    print(nodes[min_bytes-1])
    # graph, length = read_graph(filename, size, 2940)
    # print(nx.has_path(graph,(0,0),(size-1,size-1)))    
    # graph, length = read_graph(filename, size, 2941)
    # print(nx.has_path(graph,(0,0),(size-1,size-1)))
