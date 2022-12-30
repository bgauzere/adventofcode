def exo1():
    maximum_cal = 0
    current_cal = 0
    with open("input_day1.txt", "r") as f:
        for i, line in enumerate(f):
            stripped_line = line.strip()
            if stripped_line.isdigit():
                current_cal = current_cal + int(stripped_line)
            else:
                if current_cal > maximum_cal:
                    maximum_cal = current_cal
                current_cal = 0

    print(maximum_cal)


def exo2():
    calories = []
    current_cal = 0
    with open("input_day1.txt", "r") as f:
        for i, line in enumerate(f):
            stripped_line = line.strip()
            if stripped_line.isdigit():
                current_cal = current_cal + int(stripped_line)
            else:
                calories.append(current_cal)
                current_cal = 0
    calories.sort()
    print(sum(calories[-3:]))


if __name__ == '__main__':
    exo1()
    exo2()
