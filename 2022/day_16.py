import sys
import networkx as nx
import re
import matplotlib.pyplot as plt


def find_pressure(data):
    return int(re.findall(r'\d+', data)[0])


def find_valves(data):
    return re.findall(r"[A-Z][A-Z]", data)


def parse_data(content):
    g = nx.DiGraph()

    for node in content:
        valves = find_valves(node)
        pressure = find_pressure(node)
        print(valves[0])
        g.add_node(node_for_adding=valves[0], pressure=pressure)
        g.add_edges_from([(valves[0], other_valve)
                         for other_valve in valves[1:]])

    return g


def print_graph(g):
    labels = {node: (node, g.nodes[node]['pressure']) for node in g.nodes()}
    nx.draw_networkx(g, with_labels=True, labels=labels)
    plt.show()


def total_pressure(open_valves):
    return sum(open_valves.values())


def find_max_path(g, cur_node, open_valves, time, pressure_so_far):
    # open valve:
    if (len(open_valves.keys()) == g.order()):
        return pressure_so_far + total_pressure(open_valves)*time

    if time > 0:

        current_pressure = total_pressure(open_valves)

        next_pressure = 0
        for neigh in list(g[cur_node]):
            travel_time = g_r[cur_node][neigh]['time']
            cand_pressure = find_max_path(
                g, neigh, open_valves.copy(), time-travel_time, current_pressure*travel_time)

            if cand_pressure > next_pressure:
                next_pressure = cand_pressure

        for neigh in list(g[cur_node]):
            if cur_node not in open_valves.keys():
                time -= 1
                open_valves[cur_node] = g.nodes[cur_node]["pressure"]

            travel_time = g_r[cur_node][neigh]['time']
            cand_pressure = find_max_path(
                g, neigh, open_valves.copy(), time-travel_time, current_pressure*travel_time)

            if cand_pressure > next_pressure:
                next_pressure = cand_pressure

        return pressure_so_far + next_pressure

    else:
        return pressure_so_far


def find_best_perm(non_open_valves,
                   cur_valve,
                   sp,
                   pressures,
                   open_valves,
                   minute,
                   cur_pressure
                   ):
    if minute > 30:
        return cur_pressure

    non_open_valves.remove(cur_valve)
    open_valves.append(cur_valve)
    minute += 1
    cur_pressure += pressures[cur_valve]*(30-minute+1)

    if len(non_open_valves) > 0:
        highest_pressure = cur_pressure
        for next_valve in non_open_valves:
            cur_non_open_valves = non_open_valves.copy()
            cur_open_valves = open_valves.copy()
            time_travel = len(sp[cur_valve][next_valve])-1
            if (minute+time_travel <= 30):
                path_pressure = find_best_perm(cur_non_open_valves,
                                               next_valve,
                                               sp,
                                               pressures,
                                               cur_open_valves,
                                               minute+time_travel,
                                               cur_pressure)
                if (path_pressure > highest_pressure):
                    highest_pressure = path_pressure
        return highest_pressure
    else:
        return cur_pressure


def transform_graph(g):
    non_zero_nodes = [node for node in g.nodes() if g.nodes[node]
                      ['pressure'] > 0]

    non_zero_nodes.append('AA')
    g_reduced = nx.Graph()
    for node in non_zero_nodes:
        g_reduced.add_node(node, pressure=g.nodes[node]['pressure'])
    sp = dict(nx.all_pairs_shortest_path(g))
    # print(len(sp['AA']['JJ']))
    for i, u in enumerate(non_zero_nodes):
        for v in non_zero_nodes[i+1:]:
            g_reduced.add_edge(u, v, time=len(sp[u][v]))

    return g_reduced, non_zero_nodes, sp


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = [line.strip() for line in f.readlines()]
        g = parse_data(content)
        g_r, non_zero_nodes, sp = transform_graph(g)
        pressures = {node: g.nodes[node]["pressure"] for node in g_r.nodes()}
        best_pressure = find_best_perm(non_zero_nodes,
                                       'AA',
                                       sp,
                                       pressures,
                                       open_valves=[],
                                       minute=0,
                                       cur_pressure=0)
        print(best_pressure)
