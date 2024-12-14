import sys 
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def get_robots(filename):
    positions = []
    velocities = []
    with open(filename, "r") as file:
        data = [line.strip() for line in file.readlines()]
        for line in data:
            line = line.split(" ")
            positions.append([int(x.strip()) for x in line[0][2:].split(",")])
            velocities.append([int(x.strip()) for x in line[1][2:].split(",")])
            #print(positions[-1], velocities[-1])
    return positions, velocities

def move(pos, vel, height=7, width=11):
    pos[0] = (pos[0] + vel[0]) % width
    pos[1] = (pos[1] + vel[1]) % height
    return pos

def counts(pos, height=7, width=11):
    mid_h = height//2
    mid_w = width//2
    #print(mid_h, mid_w)
    quadrants = [0,0,0,0] # top-left, top-right, bottom-left, bottom-right
    for p in pos:
        if p[1] < mid_h and p[0] < mid_w: # top-left
            quadrants[0] += 1
        if p[1] < mid_h and p[0] >= width-mid_w:
            quadrants[1] += 1
        if p[1] >= height-mid_h and p[0] < mid_w: # bottom-left
            quadrants[2] += 1
        if p[1] >= height-mid_h and p[0] >= width-mid_w:
            quadrants[3] += 1
    return quadrants


def save_fig(positions, filename, height=7, width=11):
    # counts occurences in positions
    map = np.zeros((height,width))
    
    for pos in positions:
        map[pos[1], pos[0]] = 1
    fig, ax = plt.subplots()
    ax.matshow(map)
    fig.savefig(filename) 
    plt.close()

def display(positions, height=7, width=11):
    # counts occurences in positions
    counts = Counter([tuple(pos) for pos in positions])
    #print(f"counts : {counts}")
    for j in range(height):
        for i in range(width):
            if (i,j) in counts:
                print(f"{counts[(i,j)]}", end="")
            else:
                print(".", end="")
        print()

if __name__ == "__main__":
    positions, velocities = get_robots(sys.argv[1])
    height, width = int(sys.argv[2]), int(sys.argv[3])
    #display(positions, height, width)
    for i in tqdm(range(10000)):
        for pos,vel in zip(positions,velocities):
            move(pos, vel, height, width)
        #print(f"==={i}===")
        save_fig(positions,f"map_{i}.svg", height, width)

        
    # count by quadrants 
    c_quadrants = counts(positions, height, width)
    # prod of c_quadrants
    print(np.prod(c_quadrants))
