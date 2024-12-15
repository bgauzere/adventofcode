import sys 

def read_content(file):
    with open(file, "r") as f:
        content = f.readlines()
        # map
        map = []
        i = 0
        while (content[i].startswith("#")):
            map.append([])
            for j,elem in enumerate(content[i].strip()):
                if elem == "#":
                    map[-1].extend("##")
                if elem == ".":
                    map[-1].extend("..")
                if elem == "O":
                    map[-1].extend("[]")
                if elem == "@":
                    map[-1].extend("..")
                    start = (i, j*2)
            i += 1
        # moves
        i += 1 #empty line
        moves = []
        for i in range(i, len(content)):
            moves += content[i].strip()
        
    return map, moves, start

def next_pos(pos, move):
    i,j = pos
    if move == "^":
        return (i-1, j)
    elif move == "v":
        return (i+1, j)
    elif move == "<":
        return (i, j-1)
    elif move == ">":
        return (i, j+1)

def push_box_h(box_pos, map, toward_left):
    dir = -1 if toward_left else 1
    if map[box_pos[0]][box_pos[1]+dir*2] == "#":
        return False
    elif map[box_pos[0]][box_pos[1]+dir*2] == ".":
        map[box_pos[0]][box_pos[1]+dir*2] = map[box_pos[0]][box_pos[1]+dir]
        map[box_pos[0]][box_pos[1]+dir] = map[box_pos[0]][box_pos[1]]
        map[box_pos[0]][box_pos[1]] = "."
        return True
    else : #we have a box
        n_pos = (box_pos[0], box_pos[1]+dir*2)
        if push_box_h(n_pos, map, toward_left):
            map[box_pos[0]][box_pos[1]+dir*2] = map[box_pos[0]][box_pos[1]+dir]
            map[box_pos[0]][box_pos[1]+dir] = map[box_pos[0]][box_pos[1]]
            map[box_pos[0]][box_pos[1]] = "."
            return True
        return False

def push_box_v(box_pos, map, toward_up):
    dir = -1 if toward_up else 1
    box_pos1 = box_pos
    if map[box_pos[0]][box_pos[1]] == "[":
        box_pos2 = (box_pos[0], box_pos[1]+1)
    else:
        box_pos2 = (box_pos[0], box_pos[1]-1)
    
    # check if we can move the box
    items_to_check =  (map[box_pos1[0]+dir][box_pos1[1]], map[box_pos2[0]+dir][box_pos2[1]])
    if items_to_check[0] == "." and items_to_check[1] == ".": # ok tout est libre
        map[box_pos1[0]+dir][box_pos1[1]] = map[box_pos1[0]][box_pos1[1]]
        map[box_pos2[0]+dir][box_pos2[1]] = map[box_pos2[0]][box_pos2[1]]
        map[box_pos1[0]][box_pos1[1]] = "."
        map[box_pos2[0]][box_pos2[1]] = "."
        return True
    elif items_to_check[0] == "#" or items_to_check[1] == "#": # impossible on a un mur
        return False
    else:
        map_potentiel = [line.copy() for line in map]
        first_ok = False
        if items_to_check[0] == ".":
            first_ok = True
        else:
            first_ok = push_box_v((box_pos1[0]+dir,box_pos1[1]), map_potentiel, toward_up)

        second_check =  map_potentiel[box_pos2[0]+dir][box_pos2[1]] # au cas ou mis à jour par first_ok
        second_ok = False
        if second_check == ".":
            second_ok = True
        else:
            second_ok = push_box_v((box_pos2[0]+dir,box_pos2[1]), map_potentiel, toward_up)
        if first_ok and second_ok:
            map_potentiel[box_pos1[0]+dir][box_pos1[1]] = map_potentiel[box_pos1[0]][box_pos1[1]]
            map_potentiel[box_pos2[0]+dir][box_pos2[1]] = map_potentiel[box_pos2[0]][box_pos2[1]]
            map_potentiel[box_pos1[0]][box_pos1[1]] = "."
            map_potentiel[box_pos2[0]][box_pos2[1]] = "."
            for i, line in enumerate(map_potentiel):
                map[i] = line
            return True
        else:
            return False
 

def push_box(box_pos, map, move):
    if move == ">":
        return push_box_h(box_pos, map, toward_left=False)
    if move == "<":
        return push_box_h(box_pos, map, toward_left=True)
    if move == "^":
        return push_box_v(box_pos, map, toward_up=True)
    if move == "v":
        return push_box_v(box_pos, map, toward_up=False)

def move_robot(robot_pos, move, map):
    n_pos = next_pos(robot_pos, move)
    if map[n_pos[0]][n_pos[1]] == ".":
        robot_pos = n_pos        
    if map[n_pos[0]][n_pos[1]] == "#":
        print("Robot hit a wall, don't move")
    if map[n_pos[0]][n_pos[1]] == "[" or map[n_pos[0]][n_pos[1]] == "]":
        # we have to move something recursively
        if push_box(n_pos, map, move):
            robot_pos = n_pos
    return  robot_pos   

def display_map(map, robot_pos):
    for i,line in enumerate(map):
        if i == robot_pos[0]:
            line_to_print = line.copy()
            line_to_print[robot_pos[1]] = "@"  
            print("".join(line_to_print))
        else:        
            print("".join(line))

def get_gps_coordinates(map):
    result = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "[":
                result += i*100 + j
    return result

if __name__ == "__main__":
    map, moves,start = read_content(sys.argv[1])
    robot_pos = start
    display_map(map, robot_pos)
    for move in moves:
        robot_pos = move_robot(robot_pos, move, map)
        #print(f"Move {move}:")
        #display_map(map, robot_pos)
        #print()
    print(f"GPS coordinates: {get_gps_coordinates(map)}")