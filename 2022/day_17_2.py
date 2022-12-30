import sys
from abc import ABC
from enum import Enum, auto
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


class TypeRock(Enum):
    HLINE: auto()
    PLUS: auto()
    L: auto()
    VLINE: auto()
    SQUARE: auto()


class Rock(ABC):
    pass


class HLineRock(Rock):
    def __init__(self):
        self.width = 4
        self.height = 1
        self.shape = np.array([[1, 1, 1, 1]])


class PlusRock(Rock):
    def __init__(self):
        self.width = 3
        self.height = 3
        self.shape = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]])


class LRock(Rock):
    def __init__(self):
        self.width = 3
        self.height = 3
        self.shape = np.array([[0, 0, 1],
                               [0, 0, 1],
                               [1, 1, 1]])


class VLineRock(Rock):
    def __init__(self):
        self.width = 1
        self.height = 4
        self.shape = np.array([[1], [1], [1], [1]])


class SquareRock(Rock):
    def __init__(self):
        self.width = 2
        self.height = 2
        self.shape = np.array([[1, 1],
                               [1, 1]])


def deliver_rocks():
    rocks = [HLineRock, PlusRock, LRock, VLineRock, SquareRock]
    for i in range(0, 1000000000):
        yield rocks[i % 5]()


class Chamber():
    def __init__(self, jets):
        self.jets = jets
        self.rocks = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 1, 1, 1]]

    @property
    def height(self):
        return len(self.rocks)

    @property
    def highest_rock(self):
        return self.height - self.index_highest - 1

    @property
    def index_highest(self):
        for i, line in enumerate(self.rocks):
            if sum(line) > 0:
                return i

    def let_fall_a_rock(self, rock):
        rock_position = self.a_rock_appears(rock)
        # print(rock_position)
        is_stuck = False
        while not is_stuck:
            direction = self.jets.pop()
            self.jets.insert(0, direction)
            # print(rock_position, direction)
            rock_position = self.push_rock(
                rock, rock_position, direction)
            # print(rock_position)
            if not self.is_stuck(rock, rock_position):
                rock_position = self.fall_down(rock, rock_position)
            else:
                is_stuck = True
        # ajout du rock dans la chambre
        # print(f"adding rock {rock_position}")
        self.add_rock(rock, rock_position)

    def add_rock(self, rock, position):
        offset = [position[0]-rock.height+1, position[1]]
        for i in range(rock.height):
            for j in range(rock.width):
                if rock.shape[i][j] == 1:
                    self.rocks[offset[0]+i][offset[1]+j] = 1

    def print_chamber(self):
        def rock_to_str(data):
            if data == 0:
                return "."
            else:
                return "#"

        for line in self.rocks:
            str_line = [rock_to_str(i) for i in line]
            print("|"+"".join(str_line)+"|")

    def a_rock_appears(self, rock: Rock):
        # rock_position : bottom left
        rock_position = [self.index_highest-3-1, 2]
        while rock_position[0]-rock.height < 0:
            self.rocks.insert(0, [0, 0, 0, 0, 0, 0, 0])
            rock_position[0] += 1
        return rock_position

    def push_rock(self, rock, position, direction):
        potential_position = position.copy()
        if direction == ">":
            potential_position[1] += 1
        else:
            potential_position[1] -= 1
        if self.is_possible(rock, potential_position):
            return potential_position
        else:
            return position

    def is_possible(self, rock, position):
        # on verifie qu'il n'y a pas de depassement ou de surperposition avec rocks
        if position[1] < 0:
            return False
        if position[1]+rock.width > 7:
            return False
        if position[0] >= self.height:
            return False
        # superposition
        np_chamber = np.array(
            self.rocks[position[0]-rock.height+1:position[0]+1])

        test_np = np_chamber[:, position[1]
            :position[1]+rock.width] + rock.shape
        # print(test_np, position)
        return not np.any(test_np == 2)

    def is_stuck(self, rock, position):
        next_position = position.copy()
        next_position[0] += 1
        if self.is_possible(rock, next_position):
            return False
        else:
            return True

    def fall_down(self, rock, position):
        """
        returns true if the rock has fallen on another rock
        """
        next_position = position.copy()
        next_position[0] = next_position[0] + 1
        return next_position


def parse_jets(filename):
    with open(filename, "r") as f:
        jets = f.readlines()
    return list(jets[0].strip())[::-1]


if __name__ == '__main__':
    filename = sys.argv[1]
    jets = parse_jets(filename)
    chamber = Chamber(jets)
    prev = 0
    diff = []

    seq_length = 1755
    generator = deliver_rocks()
    for i, rock in enumerate(generator, start=1):
        # print(f"rock: {rock}")
        chamber.let_fall_a_rock(rock)
        # chamber.print_chamber()
        if i % (seq_length) == 0:
            # print(i, chamber.highest_rock, chamber.highest_rock - prev)
            diff.append(chamber.highest_rock - prev)
            prev = chamber.highest_rock
        if len(diff) > 2:
            if diff[-1] == diff[-2]:
                break
        # if i == seq_length:
        #     break

    # print("recherche...")
    # for seq_length in tqdm(range(200, 4000)):
    #     for offset in range(5000):
    #         if diff[offset:offset+seq_length] == diff[offset+seq_length:offset+seq_length*2]:
    #             print(f"{offset = }, {seq_length = }")

    remaining = 1000000000000 - i
    nb = remaining // (seq_length)
    reste = remaining % (seq_length)-1
    print(reste)
    for i, rock in enumerate(generator):
        # print(f"rock: {rock}")
        chamber.let_fall_a_rock(rock)
        if i == reste:
            break
    print(chamber.highest_rock + nb*diff[-1])
