import sys
import math


class Elf():
    def __init__(self, position):
        self.line = position[0]
        self.col = position[1]

    def __str__(self):
        return f"elf ({self.line},{self.col})"

    def surrounding_pos(self):
        positions = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == 0 and j == 0):
                    positions.append((self.line+i,
                                      self.col+j))
        return positions

    def north_positions(self):
        positions = []
        for i in [-1, 0, 1]:
            positions.append((self.line-1,
                              self.col+i))
        return positions

    def south_positions(self):
        positions = []
        for i in [-1, 0, 1]:
            positions.append((self.line+1,
                              self.col+i))
        return positions

    def west_positions(self):
        positions = []
        for j in [-1, 0, 1]:
            positions.append((self.line+j,
                              self.col-1))
        return positions

    def east_positions(self):
        positions = []
        for j in [-1, 0, 1]:
            positions.append((self.line+j,
                              self.col+1))
        return positions

    def move(self, new_position):
        self.line = new_position[0]
        self.col = new_position[1]


class World():
    def __init__(self, elves):
        "docstring"
        self.elves = elves
        self.gather_positions()
        self.get_limits()
        self.directions = ["N", "S", "W", "E"]

    def gather_positions(self):
        self.positions = set()
        for e in self.elves:
            position = tuple([e.line, e.col])
            self.positions.add(position)

    def is_elf_alone(self, elf):
        for p in elf.surrounding_pos():
            if p in self.positions:
                return False
        return True

    def round(self):
        # print(self.directions)
        potential_positions = {}
        for e in self.elves:
            if not self.is_elf_alone(e):

                potential_position = self.find_potential_new_position(e)
                #print(f"potential : {e} -> {potential_position}")
                if potential_position not in potential_positions:
                    potential_positions[potential_position] = [e]
                else:
                    potential_positions[potential_position].append(e)
        # print("-----")
        nb_moves = 0
        for position, elves in potential_positions.items():
            if len(elves) == 1:
                #print(f"elf moving {elves[0]} -> {position}")
                elves[0].move(position)
                nb_moves += 1
        self.gather_positions()
        self.get_limits()
        self.permut_directions()
        # self.print_world()
        return nb_moves

    def print_world(self):
        for e in world.elves:
            print(e, world.is_elf_alone(e))

        min_line, min_col, max_line, max_col = self.limits
        world_str = []
        for i in range(max_line-min_line+1):
            cur_line = []
            for j in range(max_col-min_col+1):
                cur_line.append('.')
            world_str.append(cur_line)
        for p in self.positions:
            world_str[p[0]-min_line][p[1]-min_col] = '#'
        cols = [str(abs(i)) for i in range(min_col, max_col+1)]
        print("    " + "".join(cols))
        for i, l in enumerate(world_str):
            print(f"{min_line+i:3}:"+"".join(l))

    def permut_directions(self):
        len_d = len(self.directions)
        self.directions = [self.directions[(i+1) % len_d]
                           for i in range(len_d)]

    def explore(self, elf, elf_positions, new_position):
        ok = True
        for p in elf_positions:
            if p in self.positions:
                ok = False
        if ok:
            return True, (elf.line+new_position[0],
                          elf.col+new_position[1])
        else:
            return False, tuple([elf.line, elf.col])

    def explore_north(self, elf):
        return self.explore(elf, elf.north_positions(), (-1, 0))

    def explore_south(self, elf):
        return self.explore(elf, elf.south_positions(), (+1, 0))

    def explore_west(self, elf):
        return self.explore(elf, elf.west_positions(), (0, -1))

    def explore_east(self, elf):
        return self.explore(elf, elf.east_positions(), (0, +1))

    def find_potential_new_position(self, elf):
        # check north
        for direction in self.directions:
            match direction:
                case 'N':
                    ok, new_position = self.explore_north(elf)
                case 'S':
                    ok, new_position = self.explore_south(elf)
                case 'W':
                    ok, new_position = self.explore_west(elf)
                case 'E':
                    ok, new_position = self.explore_east(elf)
            if ok:
                return new_position
        return tuple([elf.line, elf.col])

    def get_limits(self):
        min_line, min_col, max_line, max_col = math.inf, math.inf, -math.inf, -math.inf
        for p in self.positions:
            line, col = p
            min_line = line if line < min_line else min_line
            min_col = col if col < min_col else min_col
            max_line = line if line > max_line else max_line
            max_col = col if col > max_col else max_col
        self.limits = min_line, min_col, max_line, max_col
        return self.limits

    def world_rectangle_surf(self):
        self.gather_positions()
        self.get_limits()
        min_line, min_col, max_line, max_col = self.limits
        return (max_line-min_line+1) * (max_col - min_col+1)


def parse_data(filename):
    elves = []
    with open(filename, "r") as f:
        content = [line.strip() for line in f.readlines()]
        for i, line in enumerate(content):
            for j, cell in enumerate(line):
                if cell == "#":
                    elf = Elf([i, j])
                    elves.append(elf)
    return World(elves)


if __name__ == '__main__':
    if __name__ == '__main__':
        filename = sys.argv[1]
        world = parse_data(filename)
        i = 1
        while world.round() > 0:
            i += 1
        print(i)
        #print(world.world_rectangle_surf() - len(world.elves))
