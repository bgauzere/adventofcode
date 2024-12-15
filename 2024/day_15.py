import sys 

def read_content(file):
    with open(file, "r") as f:
        content = f.readlines()
        # map
        map = []
        i = 0
        while (content[i].startswith("#")):
            map.append(list(content[i].strip()))
            if "@" in content[i]:
                start = (i, content[i].index("@"))
                map[start[0]][start[1]] = "."
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

def push_box(box_pos, map, move):
    n_pos = next_pos(box_pos, move)
    if map[n_pos[0]][n_pos[1]] == ".": 
        # empty space, we can move the box
        map[box_pos[0]][box_pos[1]] = "."
        map[n_pos[0]][n_pos[1]] = "O"
        return True
    if map[n_pos[0]][n_pos[1]] == "#":
        print("Box hit a wall, don't move")
        return False
    if map[n_pos[0]][n_pos[1]] == "O":
        # we have to move something recursively
        if push_box(n_pos, map, move):
            map[box_pos[0]][box_pos[1]] = "."
            map[n_pos[0]][n_pos[1]] = "O"
            return True


def move_robot(robot_pos, move, map):
    n_pos = next_pos(robot_pos, move)
    if map[n_pos[0]][n_pos[1]] == ".":
        robot_pos = n_pos
        
    if map[n_pos[0]][n_pos[1]] == "#":
        print("Robot hit a wall, don't move")
    if map[n_pos[0]][n_pos[1]] == "O":
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
            if map[i][j] == "O":
                result += i*100 + j
    return result

if __name__ == "__main__":
    map, moves,start = read_content(sys.argv[1])
    robot_pos = start
    display_map(map, robot_pos)
    for move in moves:
        robot_pos = move_robot(robot_pos, move, map)
        # print(f"Move {move}:")
        # display_map(map, robot_pos)
        # print()
    print(f"GPS coordinates: {get_gps_coordinates(map)}")