from ast import Tuple
from utils import read_content
import numpy as np
from enum import Enum
from dataclasses import dataclass
import sys
from queue import PriorityQueue
from itertools import cycle
import string

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

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
    
    def __lt__(self, other):
        return self.line < other.line or (self.line == other.line and self.col < other.col)

@dataclass(frozen=True)
class DijstraItem():
    point: Point
    direction : Direction
    heat: int
    left_to_turn : int 
    path : Tuple = None

    def __eq__(self, other):
        return self.point == other.point and self.direction == other.direction
    def __lt__(self, other):
        return self.heat < other.heat
    def __hash__(self):
        return hash((self.point, self.direction,self.left_to_turn))
   
    
class HeatMap():
    def __init__(self, map):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)
        
    def __getitem__(self, point):
        return self.map[point.line][point.col]
      
    def is_valid(self, point):
        return point.line >= 0 and point.line < self.height and point.col >= 0 and point.col < self.width
    
    def __str__(self) -> str:
        return "\n".join(["".join([str(c) for c in l]) for l in self.map])
    
    def copy(self):
        return HeatMap([[c for c in l] for l in self.map])

def dijkstra_k(start_item, heat_map,visited):
    
    n,p = heat_map.height, heat_map.width

    to_explore = PriorityQueue()
    to_explore.put((start_item.heat,start_item))
    while (not to_explore.empty()):
        #print(f"{to_explore.qsize() =}")
        current_heat,current_item = to_explore.get()
        #print(current_item)
        #print(f"Exploring {current_item}")
        if current_item in visited:
            continue
        visited.add(current_item)
        if current_item.point == Point(n-1,p-1):
            return current_item.heat, current_item.path
        
        #current_heat = current_item.heat
        next_directions = []
        current_path = current_item.path
        if  current_item.direction in [Direction.UP, Direction.DOWN]:
            next_directions = [Direction.LEFT, Direction.RIGHT]
        else:
            next_directions = [Direction.UP, Direction.DOWN]

        for dir in next_directions:
            next_point = current_item.point.move(dir)
            if heat_map.is_valid(next_point):
                next_item = DijstraItem(next_point,dir,
                                        current_heat+heat_map[next_point],
                                        left_to_turn=2,
                                        path=current_path+tuple([next_point]))
                #if next_item not in visited:
                to_explore.put((next_item.heat,next_item))
        
        left_to_turn = current_item.left_to_turn
        if left_to_turn > 0: #turn !
            dir = current_item.direction
            next_point = current_item.point.move(dir)
            if heat_map.is_valid(next_point):
                next_item = DijstraItem(next_point,dir,
                                        current_heat+heat_map[next_point],
                                        left_to_turn-1,
                                        current_path+tuple([next_point]))
                #if next_item not in visited:
                to_explore.put((next_item.heat,next_item))
    return None   

def first(content):
    heat_map = [[int(c) for c in l] for l in content]
    heat_map = HeatMap(heat_map)
    min_heat = [] 
    start = Point(0,0)
    for direction in [Direction.RIGHT, Direction.DOWN]:
        visited = set()
        cur_path = tuple([start])
        start_item = DijstraItem(start,
                                 direction,
                                 0, #heat_map[start],
                                 left_to_turn=2,
                                 path=cur_path)
        #visited.add(start)
        cur_heat,opt_path = dijkstra_k(start_item,heat_map, visited)
        min_heat.append(cur_heat)
        draw_map = heat_map.copy()
        print(f"{cur_heat =}")

        letters = cycle(string.ascii_lowercase)
        for p in opt_path:
            draw_map.map[p.line][p.col] = next(letters)
        print(draw_map)

    return min(min_heat)

if __name__ == "__main__":
    #sys.setrecursionlimit(1000000) 

    content = read_content()
    
    print(first(content))