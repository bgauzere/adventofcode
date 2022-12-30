import sys
import re
import networkx as nx


def parse_path(line_path):
    nb_moves = [int(e) for e in re.findall(r'\d+', line_path)]
    directions = re.findall(r'[L,R]', line_path)
    return [(n, m) for n, m in zip(nb_moves, directions)]


def parse_data(filename):
    with open(filename, 'r') as f:
        content = f.readlines()
        path = parse_path(content[-1].strip())
        print(path)
        nodes = {}
        max_i = 0
        max_j = 0
        for i, line in enumerate(content):
            for j, cell in enumerate(line):
                if cell in [".", "#"]:
                    nodes[(i, j)] = cell
                    max_i = i if i > max_i else max_i
                    max_j = j if j > max_j else max_j
                elif cell == "#":
                    nodes[(i, j)] = 0

        return nodes, path, max_i, max_j


def get_limits(nodes, max_i, max_j):
    limit_line = [[max_i, 0] for _ in range(max_i+1)]
    limit_col = [[max_j, 0] for _ in range(max_j+1)]
    print(len(limit_col))
    for cell in nodes.keys():
        i, j = cell
        if limit_line[i][0] > j:
            limit_line[i][0] = j
        if limit_line[i][1] < j:
            limit_line[i][1] = j

        if limit_col[j][0] > i:
            limit_col[j][0] = i
        if limit_col[j][1] < i:
            limit_col[j][1] = i
    return limit_line, limit_col


class Cell():
    def __init__(self, i, j, stop):
        self.stop = stop
        self.i = i
        self.j = j
        self.neigbours = {}

    def neighboor(self, direction):
        return self.neigbours[direction]

    def __str__(self):
        return f"[{self.i},{self.j} ({self.stop})]"


class World():
    def __init__(self, nodes, max_i, max_j):
        self.nodes = nodes
        self.max = (max_i, max_j)
        self.limits_line, self.limits_col = get_limits(
            self.nodes, max_i, max_j)
        self.cells = {}
        for coords, node in nodes.items():
            stop = (node == "#")
            self.cells[coords] = Cell(i=coords[0], j=coords[1], stop=stop)

        for coords, cell in self.cells.items():
            cell.neigbours["W"] = self.west_neighboor(cell)
            cell.neigbours["E"] = self.east_neighboor(cell)
            cell.neigbours["N"] = self.north_neighboor(cell)
            cell.neigbours["S"] = self.south_neighboor(cell)

    def start(self):
        return self.cells[(0, self.limits_line[0][0])]

    def west_neighboor(self, cell):
        potential_col = cell.j+1
        if potential_col > self.limits_line[cell.i][1]:
            potential_col = self.limits_line[cell.i][0]

        neigh = self.cells[(cell.i, potential_col)]
        assert(neigh is not None)
        return neigh

    def east_neighboor(self, cell):
        potential_col = cell.j-1
        if potential_col < self.limits_line[cell.i][0]:
            potential_col = self.limits_line[cell.i][1]

        neigh = self.cells[(cell.i, potential_col)]
        assert(neigh is not None)
        return neigh

    def south_neighboor(self, cell):
        potential_line = cell.i+1
        if potential_line > self.limits_col[cell.j][1]:
            potential_line = self.limits_col[cell.j][0]

        neigh = self.cells[(potential_line, cell.j)]
        assert(neigh is not None)
        return neigh

    def north_neighboor(self, cell):
        potential_line = cell.i-1
        if potential_line < self.limits_col[cell.j][0]:
            potential_line = self.limits_col[cell.j][1]

        neigh = self.cells[(potential_line, cell.j)]
        assert(neigh is not None)
        return neigh


if __name__ == '__main__':
    filename = sys.argv[1]
    nodes, path, max_i, max_j = parse_data(filename)
    world = World(nodes, max_i, max_j)
    start = world.start()
    print(start)
    for d in ["W", "S", "E", "N"]:
        print(f"{d} : {start.neighboor(d)}")
    # clockwise
    directions = ["W", "S", "E", "N"]
    d = 0
    cur_cell = start
    for instruction in path:
        print(instruction)
        for _ in range(instruction[0]):
            print(cur_cell)
            next_cell = cur_cell.neighboor(directions[d])
            if next_cell.stop:
                break
            cur_cell = next_cell
        if instruction[1] == "R":
            d = (d+1) % 4
        else:
            d = (d-1) % 4
    print(f"final : {cur_cell}")
    print((cur_cell.i+1) * 1000 + (cur_cell.j + 1) * 4 + d)
