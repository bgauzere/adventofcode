import sys
import numpy as np

class Pos():
    def __init__(self, i, j):
        self.i = i
        self.j = j
    
    def south(self):
        return Pos(self.i+1, self.j)
    
    def east(self):
        return Pos(self.i, self.j+1)
    
    def west(self):
        return Pos(self.i, self.j-1)
    
    def north(self):
        return Pos(self.i-1, self.j)
    
    def south_east(self):
        return self.south().east()
    
    def south_west(self):
        return self.south().west()
    
    def north_east(self):
        return self.north().east()
    
    def north_west(self):
        return self.north().west()
    
    def __str__(self):
        return f"({self.i}, {self.j})"
    
    def copy(self):
        return Pos(self.i, self.j)
class Grid():

    def __init__(self, data):
        self.data = data
        self.max_i = len(data)
        self.max_j = len(data[0])

    def __getitem__(self, pos):
        return self.get(pos)
    
    def get(self, pos):
        if pos.i < 0 or pos.i >= self.max_i or pos.j < 0 or pos.j >= self.max_j:
            return None
        return self.data[pos.i][pos.j]

def search(grid, pos):
    """search for XMAS"""
    
    nb_xmas = 0
    if grid[pos] == "X":
        for direction in [Pos.south, Pos.east, Pos.west, Pos.north, Pos.south_east, 
                        Pos.south_west, Pos.north_east, Pos.north_west]:
            cur_pos = pos.copy()
            #print(direction.__name__,grid[direction(cur_pos)])
            if grid[direction(cur_pos)] == "M":
                cur_pos = direction(cur_pos)
                if grid[direction(cur_pos)] == "A":
                    cur_pos = direction(cur_pos)
                    if grid[direction(cur_pos)] == "S":
                        cur_pos = pos
                        nb_xmas   += 1
                        #print(pos, direction.__name__)
    return nb_xmas
def search_x(grid, pos):
    if grid[pos] == "A":
        #first_diag:
        if (grid[pos.north_west()] == "M" and grid[pos.south_east()] == "S") or (grid[pos.north_west()] == "S" and grid[pos.south_east()] == "M"):
            #second diag
            if (grid[pos.south_west()] == "M" and grid[pos.north_east()] == "S") or (grid[pos.south_west()] == "S" and grid[pos.north_east()] == "M"):
                return 1
    return 0

def second(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        grid = Grid(data)
        nb_xmas = 0
        for i in range(1,grid.max_i-1):
            for j in range(1,grid.max_j-1):
                pos = Pos(i, j)
                #print(grid[pos], end="")
                nb_xmas += search_x(grid, pos)
    print(nb_xmas)


def first(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        grid = Grid(data)
        pos = Pos(0, 0)
        nb_xmas = 0
        for i in range(grid.max_i):
            for j in range(grid.max_j):
                pos = Pos(i, j)
                #print(grid[pos], end="")
                nb_xmas += search(grid, pos)
    print(nb_xmas)
        
if __name__ == "__main__":
    second(sys.argv[1])