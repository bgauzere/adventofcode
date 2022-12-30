import string


def car_to_priority(car):
    return string.ascii_letters.index(car)+1


def compute_priorities():
    priorities = []
    with open("input_day3.txt", "r") as f:
        for line in f:
            line = line.strip()
            length_compartment = len(line)//2
            # print(length_compartment)
            set_pack1 = set(line[:length_compartment])
            set_pack2 = set(line[length_compartment:])
            letter_common = [l for l in (set_pack1 & set_pack2)]
            priorities.append(car_to_priority(letter_common[0]))
    return sum(priorities)


if __name__ == '__main__':
    priorities = []
    with open("input_day3.txt", "r") as f:
        data = f.readlines()
        for k in range(0, len(data), 3):
            group = data[k:k+3]
            badge = [l for l in (
                set(group[0].strip()) &
                set(group[1].strip()) &
                set(group[2].strip()))]
            priorities.append(car_to_priority(badge[0]))
    print(sum(priorities))
