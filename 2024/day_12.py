import sys
from collections import defaultdict

def get_map(filename):
    map = []
    regions = set()
    with open(filename) as f:
        lines = f.readlines()
        for l in lines:
            map.append(list(l.strip()))
            regions.update(set(l.strip()))
    return map
def is_inside(pos, map):
    i,j = pos
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[0])

def get_plant(map, pos):
    return map[pos[0]][pos[1]]




def count_sides(perimeter_with_faces, perimeter):
    # for p in perimeter_with_faces:
    #     print(p, perimeter_with_faces[p])
    pixels = list(perimeter_with_faces.keys())
    pixels.sort()
    #print(pixels)
    for i,p1 in enumerate(pixels):
        for p2 in pixels[i+1:]:
            #print(f"{p1} {p2}")
            if p1[0] == p2[0] and abs(p1[1] - p2[1]) == 1:
                if "v" in perimeter_with_faces[p1] and "v" in perimeter_with_faces[p2]:
                    # print(f"{p1} {p2} share v")
                    perimeter -= 1
                if "^" in perimeter_with_faces[p1] and "^" in perimeter_with_faces[p2]:
                    # print(f"{p1} {p2} share ^")
                    perimeter -= 1
            if p1[1] == p2[1] and abs(p1[0] - p2[0]) == 1:
                if ">" in perimeter_with_faces[p1] and ">" in perimeter_with_faces[p2]:
                    # print(f"{p1} {p2} share >")
                    perimeter -= 1
                if "<" in perimeter_with_faces[p1] and "<" in perimeter_with_faces[p2]:
                    # print(f"{p1} {p2} share <")
                    perimeter -= 1
    return perimeter

str_dir = {(0,1): ">", (0,-1): "<", (1,0): "v", (-1,0): "^"}

def expand_sides(map, pos, visited, label, region=None, perimeter=0, fences = None):
    if region is None:
        region = set()
    if fences is None:
        fences = defaultdict(set)
    region.add(pos)
    for dir in [(0,1), (0,-1), (1,0), (-1,0)]:
        neigh = pos[0]+dir[0], pos[1]+dir[1]
        if not is_inside(neigh, map):
            fences[pos].add(str_dir[dir])
            perimeter += 1
            continue
        if get_plant(map,neigh) != label:
            fences[pos].add(str_dir[dir])
            perimeter += 1
            continue
        if neigh in visited:
            continue
        if get_plant(map, neigh) == label:
            if neigh not in visited:
                visited.add(neigh)
                region, visited, perimeter, fences = expand_sides(map, neigh, visited, label, region, perimeter, fences)
    return region, visited, perimeter, fences

def expand(map, pos, visited, region, nb_fences =0, area=0):
    #print(f"{pos=}")
    area += 1
    for dir in [(0,1), (0,-1), (1,0), (-1,0)]:
        neigh = pos[0]+dir[0], pos[1]+dir[1]
        #print("Neigh: ", neigh)
        if not is_inside(neigh, map):
            nb_fences += 1
            #print(f"Fence : {pos=}, {neigh=}")
            continue
        if get_plant(map, neigh) != region:
            nb_fences += 1
            #print(f"Fence : {pos=}, {neigh=}")
        if neigh in visited:
            #print(f"Visited: {pos=}, {neigh=}")
            continue
        if get_plant(map, neigh) == region:
            if neigh not in visited:
                visited.add(neigh)
                nb_fences, area, visited = expand(map, neigh, visited, region, nb_fences, area)
                #print(f"Region: {pos=}, {neigh=}, {get_plant(map, neigh)=}")
    return nb_fences, area, visited

def second(filename):
    map = get_map(filename)
    visited = set()
    result = 0
    
    for i in range(len(map)):
        for j in range(len(map[0])):
            pos = (i,j)
            if pos not in visited:
                visited.add(pos)
                region, visited, perimeter, fences = expand_sides(map, pos, visited, get_plant(map,pos), None)
                #for p in fences:
                #    print(p, fences[p])
                nb_sides = count_sides(fences, perimeter)
                area = len(region)
                result += area * nb_sides
                print(get_plant(map,pos),area, nb_sides)
                #return
    print(result)

def first(filename):
    map = get_map(filename)
    visited = set()
    result = 0
    
    for i in range(len(map)):
        for j in range(len(map[0])):
            pos = (i,j)
            if pos not in visited:
                visited.add(pos)
                nb_fences, area, visited = expand(map, pos, visited, get_plant(map,pos), 0, 0)
                print(f"{get_plant(map,pos)} : {area} * {nb_fences} ")
                result += area * nb_fences
    print(result)

if __name__ == "__main__":
    second(sys.argv[1])
    
