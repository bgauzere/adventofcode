import re
import sys
import numpy as np


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
        print(volume)
    return volume, content


def nb_neighbours(x, y, z, volume):
    nb = 0
    if (x > 0) and volume[x-1, y, z] == 1:
        nb += 1
    if (x < volume.shape[0]-1) and volume[x+1, y, z] == 1:
        nb += 1
    if (y > 0) and volume[x, y-1, z] == 1:
        nb += 1
    if (y < volume.shape[1]-1) and volume[x, y+1, z] == 1:
        nb += 1
    if (z > 0) and volume[x, y, z-1] == 1:
        nb += 1
    if (z < volume.shape[2]-1) and volume[x, y, z+1] == 1:
        nb += 1
    return nb


if __name__ == '__main__':
    filename = sys.argv[1]
    volume, content = parse_data(filename)
    total_area = 0
    for voxel in content:
        total_area += 6 - nb_neighbours(*voxel, volume)
    print(total_area)
