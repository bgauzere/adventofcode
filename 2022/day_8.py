import sys
import numpy as np


def read_data(content):
    data = []
    for line in content:
        data.append([int(i) for i in line.strip()])
    return np.array(data)


def is_visible(row, col, data):
    current_height = data[row, col]
    visible_w = np.all(data[row, :col] < current_height)
    visible_e = np.all(data[row, col+1:] < current_height)
    visible_n = np.all(data[:row, col] < current_height)
    visible_s = np.all(data[row+1:, col] < current_height)
    return visible_w or visible_e or visible_n or visible_s


def perimeter(data):
    h, l = data.shape
    return 2*(h+l) - 4


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        data = read_data(f.readlines())
        h, l = data.shape
        nb_visible = 0
        for col in range(1, l-1):
            for row in range(1, h-1):
                if is_visible(row, col, data):
                    print(f"{row},{col} is visible")
                    nb_visible += 1
        print(nb_visible+perimeter(data))
