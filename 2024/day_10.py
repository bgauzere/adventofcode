import sys

from collections import defaultdict

def get_map(filename):
    with open(filename, 'r') as file:
        data = [[int(a) for a in line.strip()] for line in file]
        nb_rows = len(data)
        nb_cols = len(data[0])
        starts = []
        for i in range(nb_rows):
            for j in range(nb_cols):
                if data[i][j] == 0:
                    starts.append((i,j))
    return data, starts, nb_rows, nb_cols

def is_inside(position, nb_rows, nb_cols):
    return position[0] >= 0 and position[0] < nb_rows and position[1] >= 0 and position[1] < nb_cols



def get_ratings(data, position, nb_rows, nb_cols, height=0):
    if  height == 9:
        return 1
    # J'explore mes 4 voisins
    # Pour chaque voisin dont la hauteur est height + 1, je continue l'exploration
    # Je somme le nombre de chemins possibles à partir de chaque voisin
    # Je retourne la somme
    
    nb_paths = 0

    for neighbours in [(-1,0), (1,0), (0,-1), (0,1)]:
        new_position = (position[0] + neighbours[0], position[1] + neighbours[1])
        if is_inside(new_position, nb_rows, nb_cols):
            if data[new_position[0]][new_position[1]] == height + 1:
                nb_cur_paths = get_ratings(data, new_position, nb_rows, nb_cols, height + 1)
                nb_paths += nb_cur_paths
    return nb_paths

def get_hiketrails(data, position, nb_rows, nb_cols, visited, height=0):
    visited.add(position)
    if  height == 9:
        return 1
    # J'explore mes 4 voisins
    # Pour chaque voisin dont la hauteur est height + 1, je continue l'exploration
    # Je somme le nombre de chemins possibles à partir de chaque voisin
    # Je retourne la somme
    
    nb_paths = 0

    for neighbours in [(-1,0), (1,0), (0,-1), (0,1)]:
        new_position = (position[0] + neighbours[0], position[1] + neighbours[1])
        if is_inside(new_position, nb_rows, nb_cols) and new_position not in visited:
            if data[new_position[0]][new_position[1]] == height + 1:
                nb_cur_paths = get_hiketrails(data, new_position, nb_rows, nb_cols, visited, height + 1)
                nb_paths += nb_cur_paths
    return nb_paths


def second(filename):
    data, starts, nb_rows, nb_cols = get_map(filename)
    total_paths = 0
    for start in starts:
        nb_path = get_ratings(data, start, nb_rows, nb_cols)
        print(f"{start} : {nb_path}")
        total_paths += nb_path
    print(total_paths)


def first(filename):
    data, starts, nb_rows, nb_cols = get_map(filename)
    total_paths = 0
    for start in starts:
        visited = set()
        nb_path = get_hiketrails(data, start, nb_rows, nb_cols, visited)
        print(f"{start} : {nb_path}")
        total_paths += nb_path
    print(total_paths)

    
if __name__ == "__main__":
    second(sys.argv[1])