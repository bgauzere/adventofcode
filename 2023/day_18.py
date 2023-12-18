import numpy as np
from utils import read_content
from enum import Enum
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.path import Path

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def from_str(label):
        if label == "U":
            return Direction.UP
        elif label == "D":
            return Direction.DOWN
        elif label == "L":
            return Direction.LEFT
        elif label == "R":
            return Direction.RIGHT
        else:
            raise Exception("Invalid direction")

    def from_int(label):
        if label == 0:
            return Direction.RIGHT
        elif label == 1:
            return Direction.DOWN
        elif label == 2:
            return Direction.LEFT
        elif label == 3:
            return Direction.UP
        else:
            raise Exception("Invalid direction")

@dataclass(frozen=True)
class Point():
    line: int
    col: int

    def move(self, direction:Direction, distance:int):
        if direction == Direction.UP:
            return Point(self.line-distance, self.col)
        elif direction == Direction.DOWN:
            return Point(self.line+distance, self.col)
        elif direction == Direction.RIGHT:
            return Point(self.line, self.col+distance)
        elif direction == Direction.LEFT:
            return Point(self.line, self.col-distance)
        else:
            raise Exception("Invalid direction")

def parse_contentV2(content):
    tranchees = []
    
    for l in content:
        _, _, color = l.split()
        distance = color[2:7]
        #print(color, distance, color[-2])
        
        dir_int = int(color[-2])
        
        direction = Direction.from_int(dir_int)
        distance = int(distance,16)
        
        #print(direction, distance)
        tranchees.append((direction, distance))
        
    return tranchees


def parse_content(content):
    """
    Retourne la séquence des tranchées
    """
    # pas besoin des couleurs pour la part 1
    tranchees = []
    nb_trous = 0
    for l in content:
        dir_str, distance, color = l.split()
        direction = Direction.from_str(dir_str)
        distance = int(distance)
        nb_trous += distance

        tranchees.append((direction, distance))
        nb_trous += distance
    return tranchees,nb_trous

class Polygon():
    def __init__(self, points):
        self.points = points
        # get limits
        self.min_line = min([p.line for p in points])
        self.max_line = max([p.line for p in points])
        self.min_col = min([p.col for p in points])
        self.max_col = max([p.col for p in points])

        self.inside = None
        

    def __repr__(self):
        return f"Polygon({self.points})"

    def nb_inside(self):
        self.inside = []
        path_poly = Path([(p.line,p.col) for p in self.points], closed=True)
        
        for i in range(self.min_line, self.max_line):
            for j in range(self.min_col, self.max_col):
                if path_poly.contains_point((i,j),radius=1):
                    self.inside.append(Point(i,j))
        nb_contour = 0
        for p1,p2 in zip(self.points[:-1], self.points[1:]):
            lg_segment = (np.abs(p1.line - p2.line) +1)  * (np.abs(p1.col - p2.col) +1)
            #print(lg_segment)
            nb_contour += lg_segment
        print(f"perimetre : {nb_contour - len(self.points) +1 }")
        print(f"{len(self.inside) = }")
        print(f"{len(self.points) = }")
        
        return len(self.inside) + nb_contour  - len(self.points) +1 

    def perimetre(self):
        nb_contour = 0
        for p1,p2 in zip(self.points[:-1], self.points[1:]):
            if p1.line == p2.line:
                lg_segment = np.abs(p1.col - p2.col) 
            elif p1.col == p2.col:
                lg_segment = np.abs(p1.line - p2.line)
            #lg_segment = (np.abs(p1.line - p2.line) +1 )  * (np.abs(p1.col - p2.col) +1)
            #print(lg_segment)
            nb_contour += lg_segment
        return nb_contour
    
    def area(self):
        # Calculate the area of the polygon AFAIK methd
        area = 0.0
        for p,p1 in  zip(self.points, self.points[1:] + [self.points[0]]):
            x0,x1 = p.line, p1.line
            y0,y1 = p.col, p1.col
            
            cur_area = (x0) * (y1) - (x1)*(y0)
            area += cur_area
        area = abs(area) / 2
        print(len(self.points))
        return area
    def __str__(self):
        width = self.max_col - self.min_col + 1
        height = self.max_line - self.min_line + 1
        self.map = np.full((height, width), ".", dtype=str)
        
        for p in self.points:
            self.map[p.line-self.min_line,p.col-self.min_col] = "#"
        for p in self.inside:
            self.map[p.line-self.min_line,p.col-self.min_col] = "x"
            
        return str(self.map)


def first(content):
    # parse 
    tranchees,nb_trous = parse_content()
    start = Point(0,0)
    polygon = [start]
    for t in tranchees:
        next_point = polygon[-1].move(*t)
        polygon.append(next_point)
    
    # test
    #polygon = [Point(1,6),Point(3,1),Point(7,2),Point(4,4), Point(8,5)]
    #polygon = [Point(0,0),Point(0,4),Point(1,4),Point(1,2),Point(2,2),Point(2,4),Point(4,4),Point(4,0)]
    
    #polygon = [Point(0,0),Point(0,1),Point(1,1),Point(1,0)]
    #polygon = [polygon[0], polygon[1], Point(polygon[-2].line,polygon[1].col), polygon[-2]]
    poly = Polygon(polygon)
    #print(f"{poly.points=}")
    
    #nb_inside = poly.nb_inside()
    #print(poly)
    aera = poly.area()
    print(f"{aera=}")
    #return nb_inside        
    #print(f"{poly.perimetre()=}")
    total_exter = 0
    for dir,dist in tranchees:
        if dir == Direction.LEFT or dir == Direction.DOWN:
            total_exter += dist
    print(total_exter)
    print(total_exter+aera+1)

def second(content):
    tranchees = parse_contentV2(content)
    start = Point(0,0)
    polygon = [start]
    for t in tranchees:
        next_point = polygon[-1].move(*t)
        polygon.append(next_point)
    poly = Polygon(polygon)

    area = poly.area()
    print(f"{area=}")
    #return nb_inside        
    #print(f"{poly.perimetre()=}")
    total_exter = 0
    for dir,dist in tranchees:
        if dir == Direction.LEFT or dir == Direction.DOWN:
            total_exter += dist
    print(total_exter)
    print(total_exter+area+1)
    return total_exter+area+1

if __name__ == "__main__":
    content = read_content()
    print(second(content))
    #print(first(content))


