from utils import read_content
from dataclasses import dataclass
from enum import Enum
import sys


class Direction(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

@dataclass(frozen=True)
class Point():
    line: int
    col: int

    def move(self, direction):
        #print(f"Moving {direction} from {self.line},{self.col}")
        if direction == Direction.UP:
            return Point(self.line-1, self.col)
        elif direction == Direction.DOWN:
            return Point(self.line+1, self.col)
        elif direction == Direction.RIGHT:
            return Point(self.line, self.col+1)
        elif direction == Direction.LEFT:
            return Point(self.line, self.col-1)
        else:
            raise Exception("Invalid direction")

@dataclass(frozen=True)
class Beam():
    location: Point
    direction: Direction

class BeamMap():
    def __init__(self, map):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)
        self.already_visited = set()
    
    def __getitem__(self, point):
        return self.map[point.line][point.col]
    
    def visit(self, point,dir):
        self.already_visited.add(Beam(point, dir))
        #self.print_visited()

    def has_been_visited(self, point, dir):
        return Beam(point, dir) in self.already_visited
      
    def is_valid(self, point):
        return point.line >= 0 and point.line < self.height and point.col >= 0 and point.col < self.width
    
    def get_neighbours(self, point):
        neighbours = []
        for dir in Direction:
            neighbour = self.get_neighbour(point, dir)
            if neighbour:
                neighbours.append(neighbour)
        return neighbours
    
    def print_visited(self):
        
        for line in range(self.height):
            for col in range(self.width):
                if self[Point(line,col)] == ".":
                    if Beam(Point(line,col), Direction.UP) in self.already_visited:
                        print("^", end="")
                    elif Beam(Point(line,col), Direction.DOWN) in self.already_visited:
                        print("v", end="")
                    elif Beam(Point(line,col), Direction.RIGHT) in self.already_visited:
                        print(">", end="")
                    elif Beam(Point(line,col), Direction.LEFT) in self.already_visited:
                        print("<", end="")
                    else:
                        print(self.map[line][col], end="")
                else:
                    print(self.map[line][col], end="")
            print("")
    
    def print_energized(self):
        for line in range(self.height):
            for col in range(self.width):
                if Beam(Point(line,col), Direction.UP) in self.already_visited:
                    print("#", end="")
                elif Beam(Point(line,col), Direction.DOWN) in self.already_visited:
                    print("#", end="")
                elif Beam(Point(line,col), Direction.RIGHT) in self.already_visited:
                    print("#", end="")
                elif Beam(Point(line,col), Direction.LEFT) in self.already_visited:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")


def propagate_light(place : Point, dir:Direction , beam_map :BeamMap):
    print(place,dir,beam_map.has_been_visited(place, dir), beam_map[place])
    if beam_map.has_been_visited(place, dir):
        return
    beam_map.visit(place, dir)

    if beam_map[place] == ".":
        #print(f"{place} is a dot")
        place = place.move(dir)
        if beam_map.is_valid(place):
            propagate_light(place, dir, beam_map)
        return
    if beam_map[place] == "/":
        #print(f"{place} is a /")
        if dir == Direction.UP:
            dir = Direction.RIGHT
        elif dir == Direction.DOWN:
            dir = Direction.LEFT
        elif dir == Direction.RIGHT:
            dir = Direction.UP
        elif dir == Direction.LEFT:
            dir = Direction.DOWN
        place = place.move(dir)
        if beam_map.is_valid(place):
            propagate_light(place, dir, beam_map)
        return
    if beam_map[place] == "\\" :
        #print(f"{place} is a \\")
        
        if dir == Direction.UP:
            dir = Direction.LEFT
        elif dir == Direction.DOWN:
            dir = Direction.RIGHT
        elif dir == Direction.RIGHT:
            dir = Direction.DOWN
        elif dir == Direction.LEFT:
            dir = Direction.UP
        place = place.move(dir)
        if beam_map.is_valid(place):
            propagate_light(place, dir, beam_map)
        return
    if beam_map[place] == "|":
        #print(f"{place} is a |")
        
        if dir in [Direction.UP, Direction.DOWN]:
            place = place.move(dir)
            if beam_map.is_valid(place):
                propagate_light(place, dir, beam_map)
            return
        if dir in [Direction.LEFT, Direction.RIGHT]:
            directions = [Direction.UP, Direction.DOWN]
            for direction in directions:
                next_place = place.move(direction)
                if beam_map.is_valid(next_place):
                    propagate_light(next_place, direction, beam_map)
            return
    if beam_map[place] == "-":
        #print(f"{place} is a -")
        
        if dir in [Direction.LEFT, Direction.RIGHT]:
            place = place.move(dir)
            if beam_map.is_valid(place):
                propagate_light(place, dir, beam_map)
            return
        if dir in [Direction.UP, Direction.DOWN]:
            directions = [Direction.LEFT, Direction.RIGHT]
            for direction in directions:
                next_place = place.move(direction)
                if beam_map.is_valid(next_place):
                    propagate_light(next_place, direction, beam_map)
            return
    return 
    
def second():
    sys.setrecursionlimit(1000000) 

    content = read_content()
    beam_raw = [list(l) for l in content]
    n, p = len(beam_raw), len(beam_raw[0])
    max = 0
    indexes = []
    col = 0
    for line in range(n):
        indexes.append((Point(line,col), Direction.RIGHT))
    col = p-1
    for line in range(n):
        indexes.append((Point(line,col), Direction.LEFT))
    line = 0
    for col in range(p):
        indexes.append((Point(line,col), Direction.DOWN))
    line = n-1
    for col in range(p):
        indexes.append((Point(line,col), Direction.UP))
        
    for start_point,start_dir in indexes:
        print(f"Start point {start_point} and dir {start_dir}")
        beam_map = BeamMap(beam_raw)
        propagate_light(start_point, start_dir, beam_map)
        #beam_map.print_energized()
        nb_energized = len(set([beam.location for beam in beam_map.already_visited]))
        print(f"Start point {start_point} and dir {start_dir} gives {nb_energized}")
        if nb_energized > max:
            max = nb_energized
    return max

def first():
    sys.setrecursionlimit(1000000) 

    content = read_content()
    beam_map = [list(l) for l in content]
    beam_map = BeamMap(beam_map)
    start_point = Point(0, 0)
    start_dir = Direction.RIGHT
    propagate_light(start_point, start_dir, beam_map)
    #beam_map.print_energized()
    
    return len(set([beam.location for beam in beam_map.already_visited]))


    
    
if __name__ == '__main__':
    print(second())
