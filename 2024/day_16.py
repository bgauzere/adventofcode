import sys
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import heapq

import matplotlib.pyplot as plt


def read_content_part2(file):
    lab = nx.DiGraph()
    start, end = None, None

    with open(file, "r") as f:
        content = f.readlines()
        for i, l in enumerate(content):
            if "S" in l:
                start = (i, l.index("S"))
                content[i] = content[i].replace("S", ".")
            if "E" in l:
                end = (i, l.index("E"))
                content[i] = content[i].replace("E", ".")
        height = len(content)
        for i in range(1, len(content) - 1):
            line = content[i].strip()
            # print(f"--{line}--")
            if "S" in line:
                start = (i, line.index("S"))
            for j in range(1, len(line) - 1):
                width = len(line)
                if content[i][j] == ".":
                    lab.add_node((i, j))
                    # check for neighbours:
                    if content[i - 1][j] == ".":
                        lab.add_edge((i, j), (i - 1, j), dir=1)
                    if content[i + 1][j] == ".":
                        lab.add_edge((i, j), (i + 1, j), dir=3)
                    if content[i][j - 1] == ".":
                        lab.add_edge((i, j), (i, j - 1), dir=2)
                    if content[i][j + 1] == ".":
                        lab.add_edge((i, j), (i, j + 1), dir=0)
    return lab, start, end, height, width


def read_content(file):
    lab = nx.DiGraph()
    start, end = None, None

    with open(file, "r") as f:
        content = f.readlines()
        for i, l in enumerate(content):
            if "S" in l:
                start = (i, l.index("S"))
                content[i] = content[i].replace("S", ".")
            if "E" in l:
                end = (i, l.index("E"))
                content[i] = content[i].replace("E", ".")
        height = len(content)
        for i in range(1, len(content) - 1):
            line = content[i].strip()
            # print(f"--{line}--")
            if "S" in line:
                start = (i, line.index("S"))
            for j in range(1, len(line) - 1):
                width = len(line)
                if content[i][j] == ".":
                    lab.add_node((i, j))
                    # check for neighbours:
                    if content[i - 1][j] == ".":
                        lab.add_edge((i, j), (i - 1, j), dir=1)
                    if content[i + 1][j] == ".":
                        lab.add_edge((i, j), (i + 1, j), dir=3)
                    if content[i][j - 1] == ".":
                        lab.add_edge((i, j), (i, j - 1), dir=2)
                    if content[i][j + 1] == ".":
                        lab.add_edge((i, j), (i, j + 1), dir=0)
    return lab, start, end, height, width


def next_dir(dir):
    return (dir + 1) % 4


def diff_dir(cur_dir, next_dir):
    return abs(next_dir - cur_dir) % 2


def shortest_path(lab, start, end):
    distances = {
        (node, dir): float("inf") for node in lab.nodes for dir in range(4)
    }
    distances[(start, 0)] = 0
    priority_queue = [(0, start, 0)]

    map_directions = {node: "." for node in lab.nodes}
    pred = {}
    while priority_queue:
        cur_dist, cur_node, cur_dir = heapq.heappop(priority_queue)
        # print(f"cur_node {cur_node} cur_dist {cur_dist}, {distances[cur_node,cur_dir]}")
        if cur_node == end:
            print(f"Shortest path is {distances[end,cur_dir]}, {cur_dist}")
            return distances, map_directions, pred
        if cur_dist > distances[cur_node, cur_dir]:
            continue
        for next_node in lab.neighbors(cur_node):
            next_dir = lab[cur_node][next_node][
                "dir"
            ]  # Get the direction of the next edge
            turn_cost = (
                diff_dir(cur_dir, next_dir) * 1000
            )  # Compute the cost of turning
            new_distance = cur_dist + turn_cost + 1  # Add movement cost
            if (
                new_distance < distances[next_node, next_dir]
            ):  # Update if we found a shorter path
                distances[next_node, next_dir] = new_distance
                map_directions[next_node] = next_dir  # Save the direction
                pred[next_node, (next_dir + 2) % 2] = cur_node
                heapq.heappush(
                    priority_queue, (new_distance, next_node, next_dir)
                )  # Push the updated direction
    return distances, map_directions, pred


def all_shortest_paths(lab, start, end):
    print(start, end)
    distances = {
        (node, dir): float("inf") for node in lab.nodes for dir in range(4)
    }
    distances[(start, 0)] = 0

    priority_queue = [(0, start, 0)]

    map_directions = {node: "." for node in lab.nodes}
    paths = defaultdict(set)
    paths[(start, 0)] = {(start, 0)}
    pred = {}
    path = set()
    min_dist = float("inf")
    while priority_queue:
        cur_dist, cur_node, cur_dir = heapq.heappop(priority_queue)
        # print(f"cur_node {cur_node} cur_dist {cur_dist}, {distances[cur_node,cur_dir]}")
        if cur_node == end:
            if cur_dist < min_dist:
                min_dist = cur_dist
                path = paths[(end, cur_dir)]
                path.add((end, cur_dir))

                print(paths[(end, cur_dir)])
                print("Shortest path is ", cur_dist)
            if cur_dist == min_dist:
                path.update(paths[(end, cur_dir)])
                path.add((end, cur_dir))

                print("Shortest path is ", cur_dist)

        if cur_dist > distances[cur_node, cur_dir]:
            continue
        for next_node in lab.neighbors(cur_node):
            next_dir = lab[cur_node][next_node][
                "dir"
            ]  # Get the direction of the next edge
            turn_cost = (
                diff_dir(cur_dir, next_dir) * 1000
            )  # Compute the cost of turning
            new_distance = cur_dist + turn_cost + 1  # Add movement cost
            if new_distance <= distances[next_node, next_dir]:
                if new_distance < distances[next_node, next_dir]:
                    paths[(next_node, next_dir)] = paths[
                        (cur_node, cur_dir)
                    ].copy()
                else:
                    # Update if we found a shorter path
                    paths[(next_node, next_dir)].update(
                        paths[(cur_node, cur_dir)]
                    )
                distances[next_node, next_dir] = new_distance
                paths[(next_node, next_dir)].add((cur_node, cur_dir))
                map_directions[next_node] = next_dir  # Save the direction
                pred[next_node, (next_dir + 2) % 2] = cur_node
                heapq.heappush(
                    priority_queue, (new_distance, next_node, next_dir)
                )  # Push the updated direction
    return distances, map_directions, pred, path


def dir_to_str(dir):
    if dir == 0:
        return ">"
    if dir == 1:
        return "^"
    if dir == 2:
        return "<"
    if dir == 3:
        return "v"


def display(lab, map_directions, pred, end, start, height, width):
    print(map_directions)

    map_to_display = []
    for i in range(height):
        line = []
        for j in range(width):
            if (i, j) in lab.nodes:
                line.append(".")
            else:
                line.append("#")
        map_to_display.append(line)
    for k in map_directions:
        if map_directions[k] != ".":
            map_to_display[k[0]][k[1]] = "*"
    # to_explore = {(end, 5)}
    # explored = set()
    # while to_explore:
    #     print(to_explore)
    #     cur_node,cur_d = to_explore.pop()
    #     explored.add((cur_node,cur_d))
    #     #if != start:
    #     map_to_display[cur_node[0]][cur_node[1]] = "*" #dir_to_str(map_directions[cur_node])
    #     for d in range(4):
    #         if (cur_node,d) in pred:
    #             next_node = pred[cur_node,d]
    #             if (next_node,d) not in explored:
    #                 to_explore.add((next_node,d))

    for i in range(height):
        print("".join(map_to_display[i]))
    # plt.matshow(map_to_display)
    # plt.savefig("maze.svg")
    # plt.show()


def main():
    lab, start, end, height, width = read_content(sys.argv[1])
    # nx.draw(lab, with_labels=True)
    # plt.show()
    cur_node = start
    cur_dir = 0
    result, directions, pred = shortest_path(lab, start, end)
    for dir in range(4):
        print(result[end, dir])
        # print(result)
        # dijsktra in python  on lab without networkx
    display(lab, directions, pred, end, start, height, width)


def main_part2():

    lab, start, end, height, width = read_content(sys.argv[1])
    # nx.draw(lab, with_labels=True)
    # plt.show()
    _, _, _, path = all_shortest_paths(lab, start, end)

    result = set()
    for p in path:
        result.add(p[0])
    result = list(result)
    result.sort()
    print(result)
    print(len(result))


if __name__ == "__main__":
    main_part2()
