
from enum import Enum


class ShapeType(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Shape():

    def __init__(self, code: str, other_play=None):
        if other_play is None:
            self.shapetype = self._determineshape(code)
        else:
            if code == 'X':  # needs to lose
                self.shapetype = self.shape_to_lose(other_play)
            elif code == 'Y':
                self.shapetype = other_play.shapetype
            else:  # win !
                self.shapetype = self.shape_to_win(other_play)

    @classmethod
    def shape_to_win(cls, otherplay):
        if otherplay.shapetype == ShapeType.ROCK:
            return ShapeType.PAPER
        if otherplay.shapetype == ShapeType.PAPER:
            return ShapeType.SCISSORS
        if otherplay.shapetype == ShapeType.SCISSORS:
            return ShapeType.ROCK

    @classmethod
    def shape_to_lose(cls, otherplay):
        if otherplay.shapetype == ShapeType.ROCK:
            return ShapeType.SCISSORS
        if otherplay.shapetype == ShapeType.PAPER:
            return ShapeType.ROCK
        if otherplay.shapetype == ShapeType.SCISSORS:
            return ShapeType.PAPER

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
    print(my_play.shapetype.value, score)
    return score + my_play.shapetype.value


def compute_total_score():
    total_score = 0
    with open("input_day2.txt", "r") as f:
        for line in f:
            other_play = Shape(line[0])
            my_play = Shape(line[2], other_play)

            #print(line[2], line[0])
            total_score += compute_score(my_play, other_play)
    return total_score


if __name__ == '__main__':
    print(compute_total_score())
