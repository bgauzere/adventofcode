from tqdm import tqdm
from utils import read_content
import numpy as np


def print_map(rocks_map):
    for l in rocks_map:
        print("".join(l))
    return None

def find_northest_free_place(i,j,rocks_map):
    if i == 0:
        return i,j
    new_i = i
    while (rocks_map[new_i-1][j] == '.' ):
        new_i -= 1
        if new_i == 0:
            break
    #new_i  = max(0,new_i)            
    return new_i,j

def rotate(rocks_map,direction):
    if direction == "S":
        return rocks_map[::-1]
    if direction == "W":
        return np.array(rocks_map).T.tolist()
    if direction == "E":
        return np.flip(np.array(rocks_map).T,axis=0).tolist()
    return rocks_map
#def inverse_rotate(rocks_map,direction):
    
def update_map(rocks_map, direction):
    # rotate
    rocks_map = rotate(rocks_map,direction)
    # if direction == 'S':
    #     rocks_map = rocks_map[::-1]
    #     print_map(rocks_map)
    for i,line in enumerate(rocks_map):
        for j, point in enumerate(line):
            
            if point == "O":
                # roll it according to direction
                new_i,new_j = find_northest_free_place(i,j,rocks_map)
                if (new_i != i) or (new_j != j):
                    rocks_map[new_i][new_j] = 'O'
                    rocks_map[i][j] = '.'
                print(f"({i},{j})  -> ({new_i},{new_j})")
                #print_map(rocks_map)
    return rotate(rocks_map,direction)

def second():
    content = read_content()
    rocks_map = [list(l) for l in content]
    print_map(rocks_map)

    #    while (1):
    # move in one direction N,S,W,E
    nb_cycles = 3
    for cycle in nb_cycles:
        for direction in ['N', 'W', 'S','E']:
            print(f"{direction = }")
            # update map
            rocks_map = update_map(rocks_map,direction)

    # check
    print_map(rocks_map)
    n = len(content)
    total = 0
    for index,l in enumerate(rocks_map):
        total += sum([c == "O" for c in l]) * (n-index)

    print(total)


def first():
    content = read_content()
    rocks_map = [list(l) for l in content]
    print_map(rocks_map)

#    while (1):
        # move in one direction N,S,W,E
    direction = 'N'
    print(f"{direction = }")
    # update map
    rocks_map = update_map(rocks_map,direction)

    # check
    print_map(rocks_map)
    n = len(content)
    total = 0
    for index,l in enumerate(rocks_map):
        total += sum([c == "O" for c in l]) * (n-index)

    print(total)

if __name__ == '__main__':
    first()
    second()
