import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = [int(i.strip()) for i in f.readlines()]

        nb_increased = 0
        for i, cur in enumerate(content[1:], start=1):
            if cur > content[i-1]:
                nb_increased += 1
        print(nb_increased)
