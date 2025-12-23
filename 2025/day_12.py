import sys
import logging
from tqdm import tqdm 
#logging.basicConfig(level=logging.DEBUG)

def get_rotation(shape):
    return [list(reversed(col)) for col in zip(*shape)]

def get_all_rotations(shape):
    rotations = []
    current_shape = shape
    for _ in range(4):
        rotations.append(current_shape)
        current_shape = get_rotation(current_shape)
    return rotations

def get_horizontal_flip(shape):
    return [list(reversed(row)) for row in shape]

def get_vertical_flip(shape):
    return list(reversed(shape))

def get_all_transformations(shape):
    transformations = set()
    rotations = get_all_rotations(shape)
    for rot in rotations:
        transformations.add(shape_to_coords(rot))
        transformations.add(shape_to_coords(get_horizontal_flip(rot)))
        transformations.add(shape_to_coords(get_vertical_flip(rot)))
    return transformations

def shape_to_coords(shape):
    coords = []
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val == 1:
                coords.append((i,j))
    return tuple(sorted(coords))

def parse():
    with open(sys.argv[1],"r") as f:
        contents = f.readlines()
        line = 0
        shapes = []
        for _ in range(6):
            line += 1
            # read the next three lines for the shape
            shape = []
            for _ in range(3):
                l = contents[line].strip()
                l= [1 if c == "#" else 0 for c in l]
                shape.append(l)
                line += 1
            logging.debug(f"Adding shape: {shape}")
            shapes.append(shape)
            line += 1  # skip the empty line
        logging.debug(f"shapes: {shapes}")
        
        regions = []
        
        for l in contents[line:]:
            region = {}
            l = l.strip()
            logging.debug(f"region line: {l}")
            size = l.split(" ")[0][:-1]
            region["w"] = int(size.split("x")[0])
            region["l"] = int(size.split("x")[1])
            region["shape_numbers"] = [int(i) for i in l.split(" ")[1:]]
            regions.append(region)
            logging.debug(f"region: {region}")
        logging.debug(f"regions: {regions}")
        
        return shapes, regions
        
def place_shape(free_cells, all_possible_shapes, shape_distrib,areas,empties_left):
    needed = sum(shape_distrib[i] * areas[i] for i in range(6))
    if needed > len(free_cells): return False
    if sum(shape_distrib) == 0:
        return True
    if not free_cells:
        return False 
    free_cell = min(free_cells)
    # plusieurs options : vide ou placer une shape parmi shape_distrib
    for shape_number in range(len(shape_distrib)):
        if shape_distrib[shape_number] == 0:
            continue
        for shape in all_possible_shapes[shape_number]:
            # try to place shape at free_cell
            for anchor in shape:
                shape_coords = [(free_cell[0] + coord[0] - anchor[0],
                 free_cell[1] + coord[1] - anchor[1]) for coord in shape]
                if all(coord in free_cells for coord in shape_coords):
                    # place the shape
                    for coord in shape_coords:
                        free_cells.remove(coord)
                    shape_distrib[shape_number] -= 1
                    if place_shape(free_cells, all_possible_shapes, shape_distrib,areas,empties_left):
                        return True
                    # backtrack
                    for coord in shape_coords:
                        free_cells.add(coord)
                    shape_distrib[shape_number] += 1
    if empties_left > 0:
        free_cells.remove(free_cell)
        empties_left -= 1
        if place_shape(free_cells, all_possible_shapes, shape_distrib,areas,empties_left):
            return True
        empties_left += 1
        free_cells.add(free_cell)
    return False

def first(shapes, regions):
    """trop long sur test, ok sur vrai input"""
    ok_to_fit = 0
    all_possible_shapes = []
    areas = [sum(sum(row) for row in shape) for shape in shapes]
    logging.debug(f"areas: {areas}")
    for shape in shapes:
        transformations = get_all_transformations(shape)
        logging.debug(f"transformations for shape {shape}: {transformations}")
        all_possible_shapes.append(transformations)
    for region in tqdm(regions):
        
        free_cells = set()
        for i in range(region["l"]):
            for j in range(region["w"]):
                free_cells.add((i,j)) 
        logging.debug(f"region {region}")
        
        empties_left = region["l"] * region["w"] - sum(region["shape_numbers"][i] * areas[i] for i in range(6))
        success = place_shape(free_cells, all_possible_shapes, region["shape_numbers"],areas,empties_left)
        logging.debug(f"{success}")
        ok_to_fit += 1 if success else 0
    return ok_to_fit


def firstV2(shapes,regions):
    """!! a marché sur le vrai input !!"""
    areas = [sum(sum(row) for row in shape) for shape in shapes]
    ok_to_fit = 0
    for region in regions:
        presents_areas = sum([region["shape_numbers"][i]*areas[i] for i in range(6)])
        logging.debug(presents_areas)
        if presents_areas < region["w"]*region["l"]:
            ok_to_fit += 1
    return ok_to_fit

if __name__ == "__main__":
    shapes, regions = parse()
    print(first(shapes, regions))