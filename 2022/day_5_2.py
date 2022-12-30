def valid_stack_line(line):
    return "[" in line


def read_initial_stacks(input_data_filename):
    stacks = []
    with open(input_data_filename, "r") as f:
        for line in f:
            #line = line.strip()
            line = line[:-1]  # remove \n
            if not valid_stack_line(line):
                return stacks
            positions = list(range(1, len(line), 4))
            if len(stacks) == 0:
                stacks = [[] for _ in positions]  # creation des stacks
            for k, position in enumerate(positions):
                if line[position] != ' ':
                    # on insere en tete pour mettre en bas de la pile étant donné qu'on la parcourt de haut en bas
                    stacks[k].insert(0, line[position])
    return stacks


def valid_movement_line(line):
    return line.startswith("move")


def get_info(line):
    words = line.split(" ")
    quantity = int(words[1])
    from_stack = int(words[3]) - 1
    to_stack = int(words[5]) - 1
    return quantity, from_stack, to_stack


def apply_movement(stacks, input_data_filename):
    positions = {"quantity": 5, "from": 12, "to": 17}
    with open(input_data_filename, "r") as f:
        for line in f:
            if valid_movement_line(line):

                quantity, from_stack, to_stack = get_info(line)
                crates = stacks[from_stack][-quantity:]
                stacks[to_stack].extend(crates)
                stacks[from_stack][-quantity:] = []

    return stacks


if __name__ == '__main__':
    filename = "input_day5.txt"
    stacks = read_initial_stacks(filename)
    apply_movement(stacks, filename)

    print("".join([stack.pop() for stack in stacks]))
