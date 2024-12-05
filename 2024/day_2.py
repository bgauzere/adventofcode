import sys
import numpy as np


def second(filename):
    with open(filename, "r") as f:
        content = f.readlines()
        content = [[int(a) for a in x.split(" ")] for x in content]
        nb_safe = 0
        for i,l in enumerate(content):
            if check_valid(l):
                nb_safe += 1
            else:
                for j in range(len(l)):
                    if check_valid(l[:j] + l[j+1:]):
                        nb_safe += 1
                        break
        print(nb_safe)

def check_valid(l):
        diffs = np.diff(l)
        # check is all the same sign
        if np.all(np.sign(diffs) == np.sign(diffs[0])):
            if np.max(np.abs(diffs)) < 4:
                return True
        return False


def first(filename):
    with open(filename, "r") as f:
        content = f.readlines()
        content = [[int(a) for a in x.split(" ")] for x in content]
        nb_safe = 0
        for l in content:
            nb_safe += check_valid(l)
        print(nb_safe)

if __name__ == "__main__":
    second(sys.argv[1])