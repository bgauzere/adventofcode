import re
import sys
import numpy as np
import scipy


def parse_data(filename):
    with open(filename, "r") as f:
        content = [[int(coord) for coord in re.findall(
            r'\d+', line.strip())] for line in f.readlines()]
        data = np.array(content)
        limits = [l+1 for l in np.max(data, axis=0)]
        volume = np.zeros(limits)
        print(volume.shape)
        for voxel in content:
            x, y, z = voxel
            volume[x, y, z] = 1
        # print(volume)
    return volume, content


def is_surrunded(x, y, z, volume):

    if np.sum(volume[x+1:, y, z]) == 0 and np.sum(volume[:x, y, z]) == 0:
        return False
    if np.sum(volume[x, y+1:, z]) == 0 and np.sum(volume[x, :y, z]) == 0:
        return False
    if np.sum(volume[x, y, z+1:]) == 0 and np.sum(volume[x, y, :z]) == 0:
        return False
    return True


def get_neighbours(x, y, z, volume):
    neighbours = []
    if (x > 0):
        neighbours.append([x-1, y, z])
    if (x < volume.shape[0]-1):
        neighbours.append([x+1, y, z])
    if (y > 0):
        neighbours.append([x, y-1, z])
    if (y < volume.shape[1]-1):
        neighbours.append([x, y+1, z])
    if (z > 0):
        neighbours.append([x, y, z-1])
    if (z < volume.shape[2]-1):
        neighbours.append([x, y, z+1])
    return neighbours


def nb_neighbours(x, y, z, volume):
    nb = 0
    for neighbour in get_neighbours(x, y, z, volume):
        n_x, n_y, n_z = neighbour
        if volume[n_x, n_y, n_z] == 1:
            nb += 1
    return nb


def fill_gaps_ite(x, y, z, volume):

    to_explore = {(x, y, z)}
    while len(to_explore) > 0:
        x, y, z = to_explore.pop()
        volume[x, y, z] = 2
        for neigh in get_neighbours(x, y, z, volume):
            n_x, n_y, n_z = neigh
            if volume[n_x, n_y, n_z] == 0:
                to_explore.add((n_x, n_y, n_z))


def fill_gaps(volume):
    for dim in [0, 1, 2]:
        for border in range(volume.shape[dim]):
            to_check = [0, 0, 0]
            to_check[dim] = border
            x, y, z = to_check
            #print(x, y, z, volume[x, y, z])
            if volume[x, y, z] == 0:
                fill_gaps_ite(x, y, z, volume)
            # print(x, y, z, volume[x, y, z])
    volume[np.where(volume == 0)] = 1
    volume[np.where(volume == 2)] = 0


if __name__ == '__main__':
    filename = sys.argv[1]
    volume, content = parse_data(filename)
    # print(volume)
    fill_gaps(volume)
    # print(volume)
    total_area = 0
    for voxel in content:
        total_area += 6 - nb_neighbours(*voxel, volume)
    print(total_area)
