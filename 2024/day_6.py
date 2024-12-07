import sys
import numpy as np

import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def move(cur_pos, direction):
        # check if we are on the edge
        next_pos = None
        if direction == Direction.UP:
            next_pos = (cur_pos[0]-1, cur_pos[1])
        elif direction == Direction.RIGHT:
            next_pos = (cur_pos[0], cur_pos[1]+1)
        elif direction == Direction.DOWN:
            next_pos = (cur_pos[0]+1, cur_pos[1])
        elif direction == Direction.LEFT:
            next_pos = (cur_pos[0], cur_pos[1]-1)
        return next_pos

def navigate(start, block, nb_lines, nb_cols):
    # initialize the direction
    direction = Direction.UP
    cur_pos = start
    next_pos = move(cur_pos, direction)
    nb_steps = 0
    positions = set()
    positions.add((start, direction))
    while True:
        if (next_pos, direction) in positions:
            return True
        # check if we are out of the grid
        if next_pos[0] < 0 or next_pos[0] >= nb_lines or next_pos[1] < 0 or next_pos[1] >= nb_cols:
            #print(f"Out of the grid at {cur_pos}")
            #print(f"Nb steps : {nb_steps}")
            return False
        # check if we are on a block
        if next_pos in block:
            #print(f"Hit a block at {cur_pos}")
            next_dir = direction.value + 1
            direction = Direction(next_dir % 4)
            next_pos = move(cur_pos, direction)
        else:
            cur_pos = next_pos
            positions.add((cur_pos, direction))
            next_pos = move(next_pos, direction)
            nb_steps += 1
    


def get_out(start, block, nb_lines, nb_cols):
    print(f"Start : {start}")
    print(f"Block : {block}")
    print(f"Nb lines : {nb_lines}")
    print(f"Nb cols : {nb_cols}")
    # initialize the direction
    direction = Direction.UP
    cur_pos = start
    next_pos = move(cur_pos, direction)
    nb_steps = 0
    positions = set()
    positions.add(start)
    while True:
        # check if we are out of the grid
        if next_pos[0] < 0 or next_pos[0] >= nb_lines or next_pos[1] < 0 or next_pos[1] >= nb_cols:
            #print(f"Out of the grid at {cur_pos}")
            #print(f"Nb steps : {nb_steps}")
            print(f"{len(positions)}")
            
            return len(positions)
        # check if we are on a block
        if next_pos in block:
            #print(f"Hit a block at {cur_pos}")
            next_dir = direction.value + 1
            direction = Direction(next_dir % 4)
            next_pos = move(cur_pos, direction)
        else:
            cur_pos = next_pos
            positions.add(cur_pos)
            next_pos = move(next_pos, direction)
            nb_steps += 1
    

def second(filename):
    with open(filename, "r") as f:
        block = []
        data = f.readlines()
        nb_lines = len(data)
        for i,l in enumerate(data):
            nb_cols = len(l)
            l = l.strip()
            for j,elem in enumerate(l):
                if elem == "#":
                    block.append((i,j))
                if elem == "^":
                    start = (i,j)
        nb_block_cycles = 0
        block_set = set(block)
        for i in tqdm(range(nb_lines)):
            for j in range(nb_cols):
                if (i,j) not in block_set and (i,j) != start:
                    if navigate(start, block_set|{(i,j)}, nb_lines, nb_cols):
                        nb_block_cycles += 1
        print(f"Nb block cycles : {nb_block_cycles}")

def first(filename):
    with open(filename, "r") as f:
        block = []
        data = f.readlines()
        nb_lines = len(data)
        for i,l in enumerate(data):
            nb_cols = len(l)
            l = l.strip()
            for j,elem in enumerate(l):
                if elem == "#":
                    block.append((i,j))
                if elem == "^":
                    start = (i,j)

        get_out(start, block,nb_lines,nb_cols)    

if __name__ == "__main__":
    second(sys.argv[1])
