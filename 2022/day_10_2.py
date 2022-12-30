import sys


def read_instruction(command):
    """
    returns nb of cycles and value added
    """
    if command == "noop":
        return 1, 0
    else:
        return 2, int(command[5:])


def print_cycles(cycles):
    for i in range(20, 221, 40):
        print(f"{i} : {cycles[i-1]}")


def get_signal_strength(cycles):
    signal_strengths = []
    for i in range(20, 221, 40):
        signal_strengths.append(signal_strength(i, cycles))
    return signal_strengths


def signal_strength(i, cycles):
    return cycles[i-1] * i


def draw_row(cycles):
    row = []
    for i in range(40):
        if abs(i-cycles[i]) <= 1:
            row.append("#")
        else:
            row.append(".")
    return row


def draw(cycles):
    i = 0
    screen = []
    while(i+40 <= len(cycles)):
        screen.append(draw_row(cycles[i:i+40]))
        i = i + 40
    for line in screen:
        print("".join(line))


if __name__ == '__main__':
    filename = sys.argv[1]
    cycles = [1]

    with open(filename, "r") as f:
        contents = [line.strip() for line in f.readlines()]
        for instruction in contents:
            nb_of_cycles, to_add = read_instruction(instruction)
            if nb_of_cycles == 1:
                cycles.append(cycles[-1] + to_add)
            else:
                cycles.extend([cycles[-1] for _ in range(nb_of_cycles)])
                cycles[-1] = cycles[-2] + to_add
        draw(cycles)
