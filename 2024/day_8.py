import sys
from collections import defaultdict

def get_antennas(filename):
    with open(filename) as f:
        antennas = defaultdict(list)
        content = f.readlines()
        nb_rows = len(content)
        for i,l in enumerate(content):
            l = l.strip()
            nb_cols = len(l)
            for j,c in enumerate(l):
                if c != "." and c != "#":
                    antennas[c].append((i,j))
    return antennas, nb_rows, nb_cols

def antinodesv2(antenna_1, antenna_2, nb_rows, nb_cols):
    dx,dy = antenna_2[0] - antenna_1[0], antenna_2[1] - antenna_1[1]
    #print(f"dx : {dx}, dy : {dy}")
    found_antinodes = set()
    cur_x, cur_y = antenna_1
    while (is_inside((cur_x, cur_y), nb_rows, nb_cols)):
        found_antinodes.add((cur_x, cur_y))
        cur_x += dx
        cur_y += dy
    
    cur_x, cur_y = antenna_2
    while (is_inside((cur_x, cur_y), nb_rows, nb_cols)):
        found_antinodes.add((cur_x, cur_y))
        cur_x -= dx
        cur_y -= dy
    return found_antinodes

def is_inside(a, nb_rows, nb_cols):
    return a[0] >= 0 and a[0] < nb_rows and a[1] >= 0 and a[1] < nb_cols
def second(filename):
    antennas, nb_rows, nb_cols = get_antennas(filename)
    found_antinodes = set()
    for antenna in antennas:
        # get each pair in antennas[antenna]
            for i in range(len(antennas[antenna])):
                for j in range(i+1, len(antennas[antenna])):
                    found_antinodes.update(antinodesv2(antennas[antenna][i], 
                                                       antennas[antenna][j],
                                                       nb_rows, nb_cols))
    print(f"Nb antinodes : {len(found_antinodes)}")

def antinodes(antenna_1, antenna_2):
    dx,dy = antenna_2[0] - antenna_1[0], antenna_2[1] - antenna_1[1]
    #print(f"dx : {dx}, dy : {dy}")
    a1 = antenna_1[0] - dx, antenna_1[1] - dy
    a2 = antenna_2[0] + dx, antenna_2[1] + dy
    return a1, a2

def first(filename):
    antennas, nb_rows, nb_cols = get_antennas(filename)
    nb_antinodes = 0
    found_antinodes = set()
    for antenna in antennas:
        # get each pair in antennas[antenna]
        for i in range(len(antennas[antenna])):
            for j in range(i+1, len(antennas[antenna])):
                a1, a2 = antinodes(antennas[antenna][i], antennas[antenna][j])
                if is_inside(a1, nb_rows, nb_cols):
                    found_antinodes.add(a1)
                if is_inside(a2, nb_rows, nb_cols):
                    found_antinodes.add(a2)
                    #print(f"Antinodes for {antenna} : {a1}, {a2}")
    print(f"Nb antinodes : {len(found_antinodes)}")

def display(filename, found_antinodes):
    with open(filename) as f:
        content = f.readlines()
        content = [list(l.strip()) for l in content]
        for a in found_antinodes:
            content[a[0]][a[1]] = "#"
        for l in content:
            print("".join(l))

if __name__ == "__main__":
    second(sys.argv[1])