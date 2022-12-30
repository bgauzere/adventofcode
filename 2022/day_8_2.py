import sys
import numpy as np


def read_data(content):
    data = []
    for line in content:
        data.append([int(i) for i in line.strip()])
    return np.array(data)


def get_visibility(row, col, data):
    # check north
    current_height = data[row, col]
    height, width = data.shape

    visi_n = 0
    if row > 0:
        visi_n = 1
        while (row-visi_n > 0) and data[row-visi_n, col] < current_height:
            visi_n += 1

    visi_s = 0
    if row < height-1:
        visi_s = 1
        while (row+visi_s < height-1) and data[row+visi_s, col] < current_height:
            visi_s += 1
    visi_w = 0
    if col > 0:
        visi_w = 1
        while (col-visi_w > 0) and data[row, col-visi_w] < current_height:
            visi_w += 1

    visi_e = 0
    if col < width - 1:
        visi_e = 1
        while (col+visi_e < width-1) and data[row, col+visi_e] < current_height:
            visi_e += 1

    visi = visi_n * visi_s * visi_w * visi_e
    print(f"{row},{col} : {visi} ({visi_n,visi_s, visi_w ,visi_e})")
    return visi


if __name__ == '__main__':
    filename = sys.argv[1]
    max_visi = 0
    with open(filename, "r") as f:
        data = read_data(f.readlines())
        h, l = data.shape
        for col in range(l):
            for row in range(h):
                cur_visi = get_visibility(row, col, data)
                #print(cur_visi, row, col)
                if cur_visi > max_visi:
                    max_visi = cur_visi

    print(max_visi)
