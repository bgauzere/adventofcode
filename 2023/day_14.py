from functools import cache
from tqdm import tqdm
from utils import read_content
import numpy as np

def find_cycle(lst): # adaptéde wikipedia
    """Floyd's cycle detection algorithm."""
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    # The hare moves twice as quickly as the tortoise and
    # the distance between them increases by 1 at each step.
    # Eventually they will both be inside the cycle and then,
    # at some point, the distance between them will be
    # divisible by the period λ.
    tortoise = 0
    hare = 1
    while lst[tortoise] != lst[hare]:
        tortoise += 1
        hare += 2
  
    # At this point the tortoise position, ν, which is also equal
    # to the distance between hare and tortoise, is divisible by
    # the period λ. So hare moving in cycle one step at a time, 
    # and tortoise (reset to x0) moving towards the cycle, will 
    # intersect at the beginning of the cycle. Because the 
    # distance between them is constant at 2ν, a multiple of λ,
    # they will agree as soon as the tortoise reaches index μ.

    # Find the position μ of first repetition.    
    mu = 0
    tortoise = 0
    while lst[tortoise] != lst[hare]:
        tortoise += 1
        hare += 1   # Hare and tortoise move at same speed
        mu += 1
 
    # Find the length of the shortest cycle starting from x_μ
    # The hare moves one step at a time while tortoise is still.
    # lam is incremented until λ is found.
    lam = 1
    hare = tortoise
    while lst[tortoise] != lst[hare]:
        hare += 1
        lam += 1
 
    return lam, mu

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
        return np.flip(np.array(rocks_map)).T.tolist()
    return rocks_map
#def inverse_rotate(rocks_map,direction):

@cache
def update_map(rocks_map, direction):
    # rotate
    rocks_map = [list(l) for l in rocks_map]
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
                #print(f"({i},{j})  -> ({new_i},{new_j})")
                #print_map(rocks_map)
    rocks_map = rotate(rocks_map,direction)
    
    return tuple([tuple(l) for l in rocks_map])

def second():
    content = read_content()
    rocks_map = tuple([tuple(l) for l in content])
    print_map(rocks_map)

    #    while (1):
    # move in one direction N,S,W,E
    nb_cycles = 1000000000
    eval_cycles = 1000
    totals = []
    for cycle in tqdm(range(eval_cycles)):
        for direction in ['N', 'W', 'S','E']:
            #print(f"{direction = }")
            # update map
            rocks_map = update_map(rocks_map,direction)
        #print(f"{cycle+1 =}")
        n = len(content)
        total = 0
        for index,l in enumerate(rocks_map):
            total += sum([c == "O" for c in l]) * (n-index)
        print(total)
        totals.append(total)
        #print_map(rocks_map)
    # test all sliding windows between n and m
    n,m=10,50 # estimée avec un plot sale des 1000 premieers valeurs 
    for w_size in range(n,m):
        for i in range(0,len(totals),w_size):
            if totals[i:i+w_size+1] == totals[i+w_size:i+2*w_size+1]:
                lam, mu = i,w_size
                print(lam,mu)
                offset = i
                print(totals[offset + (nb_cycles%w_size)-1])
                #print(totals[
                return
    #lam,mu = find_cycle(totals[100:])
    
    

def first():
    content = read_content()
    rocks_map = [list(l) for l in content]
    print_map(rocks_map)

#    while (1):
        # move in one direction N,S,W,E
    direction = 'E'
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
    #first()
    second()
