import sys
import math


class Me():
    def __init__(self, position):
        self.line = position[0]
        self.col = position[1]

    def move(self, position):
        self.line = position[0]
        self.col = position[1]

    def copy(self):
        moi2 = Me([self.line, self.col])
        return moi2

    @property
    def position(self):
        return [self.line, self.col]


WALL = "#"
FREE = "."
BLIZZ_D = "v"
BLIZZ_U = "^"
BLIZZ_R = ">"
BLIZZ_L = "<"


class Blizzard():
    def __init__(self, position, direction, max_row, max_col):
        self.direction = direction
        self.position = position  # row, col
        self.max_row = max_row
        self.max_col = max_col

    def move(self):
        if self.direction == BLIZZ_D:
            if self.position[0]+1 <= self.max_row:
                self.position[0] = self.position[0]+1
            else:
                self.position[0] = 1
        if self.direction == BLIZZ_U:
            if self.position[0]-1 >= 1:
                self.position[0] = self.position[0]-1
            else:
                self.position[0] = self.max_row
        if self.direction == BLIZZ_R:
            if self.position[1]+1 <= self.max_col:
                self.position[1] = self.position[1]+1
            else:
                self.position[1] = 1
        if self.direction == BLIZZ_L:
            if self.position[1]-1 >= 1:
                self.position[1] = self.position[1]-1
            else:
                self.position[1] = self.max_col

        return self.position


class Valley():
    def __init__(self, data):
        self.content = data
        self.blizzards = []
        for row, line in enumerate(self.content):
            for col, cell in enumerate(line):
                if cell in [BLIZZ_D, BLIZZ_L, BLIZZ_U, BLIZZ_R]:
                    blizz = Blizzard([row, col], cell, self.height, self.width)
                    self.blizzards.append(blizz)
        self.gather_blizz_pos()

    def copy(self):
        valley_c = Valley(self.content)
        valley_c.blizzards = self.blizzards.copy()
        valley_c.blizz_positions = self.blizz_positions.copy()
        return valley_c

    def gather_blizz_pos(self):
        self.blizz_positions = {}
        for blizz in self.blizzards:
            t_pos = tuple(blizz.position)
            if t_pos not in self.blizz_positions:
                self.blizz_positions[t_pos] = [blizz]
            else:
                self.blizz_positions[t_pos].append(blizz)

    @property
    def start(self):
        pos = [0, self.content[0].index(FREE)]
        return pos

    @property
    def exit(self):
        pos = [len(self.content)-1, self.content[-1].index(FREE)]
        return pos

    @property
    def width(self):
        return len(self.content[0]) - 2

    @property
    def height(self):
        return len(self.content) - 2

    def is_free(self, position):
        if position == self.exit:
            return True
        if position[0] <= 0:
            return False
        if position[0] > self.height:
            return False
        if position[1] == 0:
            return False
        if position[1] > self.width:
            return False
        if tuple(position) in self.blizz_positions:
            return False
        return True

    def print_valley(self):
        print(self.content[0])
        for row in range(1, self.height+1):
            cur_line = []
            for col in range(1, self.width+1):
                cur_pos = tuple([row, col])
                if cur_pos not in self.blizz_positions:
                    cur_line.append(FREE)
                else:
                    loc_blizz = self.blizz_positions[cur_pos]
                    if len(loc_blizz) == 1:
                        cur_line.append(loc_blizz[0].direction)
                    else:
                        cur_line.append(str(len(loc_blizz)))
            print("#"+"".join(cur_line)+"#")

        print(self.content[-1])

    def one_minute(self):
        for blizz in self.blizzards:
            blizz.move()
        self.gather_blizz_pos()


def parse_data(filename):
    with open(filename, "r") as f:
        content = [line.strip() for line in f.readlines()]
        valley = Valley(content)
        return valley


def find_exit(moi, valley, nb_minute):
    #print(moi.position, nb_minute)
    if moi.position == valley.exit:
        return True, nb_minute
    # go down
    if nb_minute > 40:
        return False, math.inf
    ok = False
    valley.one_minute()
    nb_minute += 1

    results = []
    for offset in [(0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)]:
        tentative_pos = [moi.position[0]+offset[0],
                         moi.position[1]+offset[1]]
        if valley.is_free(tentative_pos):
            ok, nb_minute_d = find_exit(
                Me(tentative_pos), valley.copy(), nb_minute)
            if ok:
                results.append(nb_minute_d)
    if len(results) == 0:
        return False, math.inf
    else:
        return True, min(results)


def find_exit_ite(moi, valley):
    positions = {tuple(moi.position)}
    nb_minutes = 0
    while tuple(valley.exit) not in positions:
        print(len(positions), nb_minutes)
        valley.one_minute()
        nb_minutes += 1
        next_mois = set()
        for pos in positions:
            for offset in [(0, 1), (0, -1), (-1, 0), (1, 0), (0, 0)]:
                tentative_pos = (pos[0]+offset[0],
                                 pos[1]+offset[1])
                if tentative_pos == tuple(valley.exit):
                    return nb_minutes
                if valley.is_free(tentative_pos):
                    next_mois.add(tentative_pos)
        positions = next_mois
    return nb_minutes


if __name__ == '__main__':
    filename = sys.argv[1]
    valley = parse_data(filename)
    print(valley.height, valley.width)
    valley.print_valley()

    moi = Me(valley.start)
    print(moi)
    print(valley.exit)
    nb_minute = find_exit_ite(moi, valley)
    print(nb_minute)
