import sys


def create_grid(n=20):
    grid = [["." for _ in range(n)] for _ in range(n)]
    return grid


def display_path(positions):
    grid = create_grid()
    for pos in positions:
        grid[pos[0]][pos[1]] = "#"
    display_grid(grid)


def display_grid(grid):
    for line in grid:
        print("".join(line))


def display(positions, labels):
    grid = create_grid()
    for knot, pos in positions.items():
        print(knot, pos)
        grid[pos[0]][pos[1]] = labels[knot]
    display_grid(grid)


def read(command):
    direction = command[0]
    numbers = int(command[2:])
    return [direction]*numbers


def apply_direction_to_head(head, move):
    match move:
        case 'R':
            head[1] += 1
        case 'L':
            head[1] -= 1
        case 'U':
            head[0] += 1
        case 'D':
            head[0] -= 1
    return head


def are_touching(tail, head):
    return abs(tail[0]-head[0]) <= 1 and abs(tail[1]-head[1]) <= 1


def move_tail_close_to_head(tail, head):
    if are_touching(tail, head):  # touching, do nothing
        return tail

    diff_vector = [head[0] - tail[0], head[1]-tail[1]]

    if diff_vector[0] == 0:  # same row
        if diff_vector[1] > 0:  # head is right tail, move right
            tail[1] += 1
        else:
            tail[1] -= 1
    elif diff_vector[1] == 0:  # same col
        if diff_vector[0] > 0:  # head is above tail, move up
            tail[0] += 1
        else:
            tail[0] -= 1
    else:  # diagonal, non touching, so the move is diagonal
        # 4 diagonal
        if diff_vector[0] > 0:  # head is above tail, move up
            tail[0] += 1
        else:
            tail[0] -= 1
        if diff_vector[1] > 0:  # head is right tail, move right
            tail[1] += 1
        else:
            tail[1] -= 1
    return tail


if __name__ == '__main__':
    filename = sys.argv[1]
    labels = ["H", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    knots = {knot: [0, 0]
             for knot in range(10)}  # ["H", "1", "2", "3", "4", "5", "6", "7", "8", "9"]}
    positions = set()
    with open(filename, "r") as f:
        commands = [line.strip() for line in f.readlines()]
        for command in commands:
            # print(command)
            moves = read(command)
            for move in moves:
                head = apply_direction_to_head(knots[0], move)
                knots[0] = head
                for knot in range(1, 10):
                    knots[knot] = move_tail_close_to_head(
                        knots[knot], knots[knot-1])
                positions.add(tuple(knots[9]))
            #display(knots, labels)

    print(len(positions))
    # display_path(positions)
