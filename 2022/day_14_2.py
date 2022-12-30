import sys


def parse_structures(content):
    list_structures = []
    for line in content:
        current_structure = []
        for structure in line.split("->"):
            current_structure.append([int(data.strip())
                                     for data in structure.split(",")])
        list_structures.append(current_structure)
    return list_structures


def get_limits(structures):
    x_min, x_max = 500, 500
    y_min = 0
    y_max = 0
    for structure in structures:
        for path in structure:
            if path[0] > x_max:
                x_max = path[0]
            if path[0] < x_min:
                x_min = path[0]
            if path[1] > y_max:
                y_max = path[1]
    return x_min, x_max, y_min, y_max


def build_structure(landscape, structure, x_min, x_max, y_min, y_max):
    for i in range(len(structure)-1):
        #print(f"{i}: {structure[i], structure[i+1]}")
        x_start = min(structure[i][0], structure[i+1][0])
        x_end = max(structure[i][0], structure[i+1][0])
        y_start = min(structure[i][1], structure[i+1][1])
        y_end = max(structure[i][1], structure[i+1][1])

        for x in range(x_start, x_end+1):
            for y in range(y_start, y_end+1):
                #print(x-x_min, y-y_min)
                landscape[y-y_min][x-x_min] = ROCK
    return landscape


def parse_landscape(content):
    padding = 499
    structures = parse_structures(content)
    x_min, x_max, y_min, y_max = get_limits(structures)
    x_min = x_min-padding
    x_max = x_max+padding
    y_max = y_max+2
    #print(x_min, x_max, y_min, y_max)

    landscape = []
    for i in range(y_min, y_max+1):
        landscape.append([AIR].copy() * (x_max-x_min + 1))
    for structure in structures:
        landscape = build_structure(
            landscape, structure, x_min, x_max, y_min, y_max)

    floor = [[x_min, y_max], [x_max, y_max]]
    landscape = build_structure(
        landscape, floor, x_min, x_max, y_min, y_max)

    return landscape, [x_min, x_max, y_min, y_max]


def print_landscape(landscape):
    for line in landscape:
        print("".join(line))


def go_down(sand_unit, landscape, limits):
    x_sand, y_sand = sand_unit
    x_min, x_max, y_min, y_max = limits
    if (y_sand == limits[-1]):
        return None, False

    if landscape[y_sand+1-y_min][x_sand-x_min] == AIR:
        return [x_sand, y_sand+1], False
    elif landscape[y_sand+1-y_min][x_sand-1-x_min] == AIR:
        if (x_sand-1 >= x_min):
            return [x_sand-1, y_sand+1], False
        else:
            return None, False
    elif landscape[y_sand+1-y_min][x_sand+1-x_min] == AIR:
        if (x_sand + 1 < x_max):
            return [x_sand+1, y_sand+1], False
        else:
            return None, False
    else:
        return [x_sand, y_sand], True


def drop_sand(landscape, source, limits):
    sand_unit = source
    rest = False
    while sand_unit is not None and not rest:
        sand_unit, rest = go_down(sand_unit, landscape, limits)
        #print(sand_unit, rest)
    return sand_unit, rest


AIR = '.'
SAND = 'o'
ROCK = '#'
SOURCE = "+"

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        sand_source = [500, 0]
        content = f.readlines()
        content = [line.strip() for line in content]
        landscape, limits = parse_landscape(content)
        landscape[0][500-limits[0]] = SOURCE
        no_more_flow = False
        nb_rest = 0
        while not no_more_flow:
            sand_unit, rest = drop_sand(landscape, sand_source, limits)
            landscape[sand_unit[1]-limits[2]][sand_unit[0]-limits[0]] = SAND
            nb_rest += 1
            if sand_unit == sand_source:
                no_more_flow = True

        print_landscape(landscape)
        print(nb_rest)
