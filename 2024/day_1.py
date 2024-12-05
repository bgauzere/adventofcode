import sys
from collections import Counter

def second(filename):
    with open(filename, "r") as f:
        content = f.readlines()
        l1,l2 = [], []
        for i,l in enumerate(content):
            l = l.split()
            l1.append(int(l[0]))
            l2.append(int(l[1]))
    counter = Counter(l2)
    #print(counter)
    result = 0
    for i in l1:
        result += counter[i]*i
    print(result)


def first(filename):
    with open(filename, "r") as f:
        content = f.readlines()
        l1,l2 = [], []
        for i,l in enumerate(content):
            l = l.split()
            l1.append(int(l[0]))
            l2.append(int(l[1]))
        l1.sort()
        l2.sort()
        dist = 0
        for i,j in zip(l1,l2):
            dist += abs(i-j)
        print(dist)

if __name__ == "__main__":
    second(sys.argv[1])