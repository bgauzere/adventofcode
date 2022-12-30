import sys
from dataclasses import dataclass
import networkx as nx
import string
import matplotlib.pyplot as plt


def char_to_int(letter):
    if letter == 'S':
        return 0
    if letter == "E":
        return 25

    index = ord(letter)-ord('a')
    return index


def find_starts(content):
    starts = []
    for i, line in enumerate(content):
        if "S" in line:
            starts.append((i, line.index("S")))
        if "a" in line:
            starts.extend([(i, j) for j in range(len(line)) if line[j] == 'a'])
    return starts


def find_end(content):
    for i, line in enumerate(content):
        if "E" in line:
            return (i, line.index("E"))


def parse_grid(content):
    content = [line.strip() for line in content]
    grid = [[char_to_int(c) for c in line] for line in content]
    return grid


@ dataclass(frozen=True)
class Node():
    altitude: int
    row: int
    col: int

    def __str__(self):
        return f"({self.row},{self.col}) [{self.altitude}]"


def valid_case(i, j, nb_lines, nb_cols):
    return (i >= 0) & (i < nb_lines) & (j >= 0) & (j < nb_cols)


def get_neighbours_id(i, j, nb_lines, nb_cols):
    neighs = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    neighs = [neigh for neigh in neighs if valid_case(
        *neigh, nb_lines, nb_cols)]
    return neighs


def from_grid_to_graph(grid):
    graph = nx.DiGraph()
    nb_lines = len(grid)
    nb_cols = len(grid[0])
    node_map = {}
    # creation des noeuds
    for i in range(nb_lines):
        for j in range(nb_cols):
            node = Node(grid[i][j], i, j)
            node_map[(i, j)] = node
            graph.add_node(node)
    for node in graph.nodes(data=True):
        node = node[0]
        indexes = get_neighbours_id(node.row, node.col, nb_lines, nb_cols)
        current_alt = node.altitude
        for neigh in indexes:
            if node_map[neigh].altitude - current_alt <= 1:
                #print(f"edge between {node} and {node_map[neigh]}")
                graph.add_edge(node, node_map[neigh])
    return graph, node_map


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        visited = []

        content = f.readlines()
        grid = parse_grid(content)
        starts = find_starts(content)
        print(starts)
        end = find_end(content)
        graph, node_map = from_grid_to_graph(grid)
        positions = {node: (node.row, node.col) for node in graph.nodes()}
        # print(positions)
        #nx.draw_networkx(graph, pos=positions, with_labels=False)
        # plt.show()
        sp_length = []
        for start in starts:
            try:
                sp_length.append(nx.shortest_path_length(
                    graph, node_map[start], node_map[end]))
            except nx.exception.NetworkXNoPath:
                print("Pas de chemin ici !")
        print(min(sp_length))
