import sys
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict
import heapq
from tqdm import tqdm


def read_graph(filename):
    with open(filename) as f:
        content = f.readlines()
        graph = nx.Graph()
        comp_graph = nx.Graph()
        for i, line in enumerate(content):
            for j, item in enumerate(line.strip()):
                if item == "S":
                    start = (i, j)
                    graph.add_node(start)
                if item == "E":
                    end = (i, j)
                    graph.add_node(end)
                if item == ".":
                    graph.add_node((i, j))
                if item in [".", "S", "E"]:
                    for x, y in [
                        (i + 1, j),
                        (i, j + 1),
                        (i - 1, j),
                        (i, j - 1),
                    ]:
                        if (
                            0 <= x < len(content)
                            and 0 <= y < len(content[0])
                            and content[x][y] == "."
                        ):
                            graph.add_edge((i, j), (x, y))
                if item == "#":
                    for x, y in [
                        (i + 1, j),
                        (i, j + 1),
                        (i - 1, j),
                        (i, j - 1),
                    ]:
                        if (
                            0 <= x < len(content)
                            and 0 <= y < len(content[0])
                            and content[x][y] == "#"
                        ):
                            comp_graph.add_edge((i, j), (x, y))
        return graph, comp_graph, start, end


def find_shortcuts(graph, path, limit=0):
    shortcuts = {}
    for k, node in enumerate(path):
        i, j = node
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = i + dir[0], j + dir[1]
            if (x, y) not in graph:
                x, y = x + dir[0], y + dir[1]
                if (x, y) in path[k:]:
                    index = path[k:].index((x, y))
                    length = index - 2
                    if length >= limit:
                        shortcuts[((i, j), (x, y))] = length
    return shortcuts


def read_data(filename):
    with open(filename) as f:
        content = f.readlines()
        data = []
        for line in content:
            data.append(line.strip())
    return data


def find_bigger_shortcuts(data, path, limit, max_length=20):
    # dictionnaire pour le path qui a chaque noeud associe sa position
    path_dict = {node: i for i, node in enumerate(path)}
    shortcuts_lengths = {}

    for i, node in tqdm(enumerate(path)):
        shortcuts_d = find_s_path2(data, node, max_depth=max_length)
        for (
            reached_node,
            len_s,
        ) in shortcuts_d.items():
            len_shortcut = path_dict[reached_node] - i - len_s
            if len_shortcut >= limit:
                shortcuts_lengths[len_shortcut] = (
                    shortcuts_lengths.get(len_shortcut, 0) + 1
                )
                # print(
                #     f"{node}({i}) -> {reached_node}{(path_dict[reached_node])} : {len_s, len_shortcut}"
                # )
    return shortcuts_lengths


def find_s_path2(data, start, max_depth=20):
    rows, cols = len(data), len(data[0])
    distances = {
        start: 0
    }  # Distance minimale pour chaque noeud "#" atteignable
    pq = [(0, start)]  # File de priorité (distance actuelle, noeud)
    reachable_d = {}  # set()  # Noeuds "#" atteignables
    while pq:
        current_distance, current_node = heapq.heappop(pq)

        # Si la distance actuelle dépasse le seuil de profondeur, on ignore ce noeud
        if current_distance > max_depth:
            continue

        # Vérifier les voisins
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current_node[0] + dir[0], current_node[1] + dir[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                cell_value = data[neighbor[0]][neighbor[1]]
                new_distance = current_distance + 1
                # Si la nouvelle distance est meilleure et ne dépasse pas max_depth
                if new_distance <= max_depth and new_distance < distances.get(
                    neighbor, float("inf")
                ):
                    #   if cell_value == "#": ! a shortcut can go through a "."
                    heapq.heappush(pq, (new_distance, neighbor))
                    distances[neighbor] = new_distance
                    if cell_value in [".", "S", "E"]:
                        if neighbor not in reachable_d:
                            reachable_d[neighbor] = new_distance

    return reachable_d


def find_s_path(data, start, visited=None, reachable=None, length=20):
    # a special path s_path is a path that start with a "." and ends with a ".", all intermediate nodes are "#"
    # the path isof length max_length
    # start is assumed to be a "." node
    if length == 0:
        return

    if visited is None:
        visited = {start}
    else:
        visited.add(start)

    if reachable is None:
        reachable = set()

    for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_node = (start[0] + dir[0], start[1] + dir[1])
        if 0 <= new_node[0] < len(data) and 0 <= new_node[1] < len(data[0]):
            if data[new_node[0]][new_node[1]] in [".", "S", "E"]:
                reachable.add((new_node, length))
                # if new_node not in reachable:
                #     reachable[new_node] = length
                # else:
                #    reachable[new_node] = max(reachable[new_node], length)
            if (
                data[new_node[0]][new_node[1]] == "#"
                and new_node not in visited
            ):
                find_s_path(data, new_node, visited, reachable, length - 1)
                # find_s_path2(data, new_node, length - 1)
    return reachable


if __name__ == "__main__":
    graph, comp_graph, start, end = read_graph(sys.argv[1])
    limit = 0
    if len(sys.argv) == 3:
        limit = int(sys.argv[2])
    # print(start, end)
    # nx.draw(graph, with_labels=True)
    # plt.show()
    path = nx.shortest_path(graph, start, end)
    print(len(path))

    ## Part 1
    shortcuts = find_shortcuts(graph, path, limit)
    print(len(shortcuts))
    # for key, value in shortcuts.items():
    #     print(f"{key} : {value}")
    # counter = Counter(shortcuts.values())

    # print(sorted(counter.items()))

    ## Part 2
    data = read_data(sys.argv[1])
    # path_dict = {node: i for i, node in enumerate(path)}
    # for i, node in enumerate(path):
    #     print(f"{i=} {node=}, {path_dict[node]=}")
    # cur_node = path[6]
    # shortcuts_d, shortcuts_s = find_s_path2(data, cur_node)
    # nodes = sorted(shortcuts_d.keys())
    # for node in nodes:
    #     print(
    #         f"{node=} : {path_dict[cur_node]}, {path_dict[node]}, {shortcuts_d[node]}, {path_dict[node] - path_dict[cur_node] - shortcuts_d[node]}"
    #     )
    # print("---------")
    # for node, length in shortcuts_s:
    #     print(f"{node=} : {length}")
    shortcuts_lengths = find_bigger_shortcuts(data, path, limit, max_length=20)
    lengths = sorted(shortcuts_lengths.keys())
    nb_shortcuts = sum(shortcuts_lengths.values())
    print(f"{nb_shortcuts}")
    # for l in lengths:
    #     print(f"{l} : {shortcuts_lengths[l]}")

    """Pour la partie 2, chercher un path dans le graph complémentaire (celui
    des #) de taille max 20 noeuds entre chaque noeud du path et l'ensemble des
    noeuds du path a partir de la position + 100 Donc 9000*9000 = 81 millions de
    paires de noeuds à testerd """
