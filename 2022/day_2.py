
from enum import Enum


class ShapeType(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Shape():

    def __init__(self, code: str):
        self.shapetype = self._determineshape(code)

    def _determineshape(self, code: str) -> ShapeType:
        if code in ['A', 'X']:
            return ShapeType.ROCK
        if code in ['B', 'Y']:
            return ShapeType.PAPER
        if code in ['C', 'Z']:
            return ShapeType.SCISSORS

    def play(self, other_play):
        '''
        return 1 if win, 0 for draw, -1 for losing
        '''
        if self.shapetype == other_play.shapetype:
            return 0
        if self.shapetype == ShapeType.ROCK:
            return 1 if other_play.shapetype == ShapeType.SCISSORS else -1
        if self.shapetype == ShapeType.PAPER:
            return 1 if other_play.shapetype == ShapeType.ROCK else -1
        if self.shapetype == ShapeType.SCISSORS:
            return 1 if other_play.shapetype == ShapeType.PAPER else -1


def compute_score(my_play: Shape, other_play: Shape):
    """
    a_round is two shapes
    """
    result = my_play.play(other_play)
    score = 0
    if result == 0:
        score = 3
    elif result == 1:
        score = 6
    else:
        score = 0
    #print(my_play.shapetype.value, score)
    return score + my_play.shapetype.value


def compute_total_score():
    total_score = 0
    with open("input_day2.txt", "r") as f:
        for line in f:
            my_play = Shape(line[2])
            other_play = Shape(line[0])
            #print(line[2], line[0])
            total_score += compute_score(my_play, other_play)
    return total_score


if __name__ == '__main__':
    print(compute_total_score())
