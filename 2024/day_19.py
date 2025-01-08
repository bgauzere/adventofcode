import sys
from tqdm import tqdm

from functools import lru_cache


def read_content(filename):
    with open(filename) as f:
        data = f.readlines()
        patterns = [towel.strip() for towel in data[0].strip().split(",")]
        towels = []
        for towel in data[2:]:
            towels.append(towel.strip())
        return tuple(patterns), tuple(towels)


@lru_cache(maxsize=None)
def find_all_patterns(patterns, towel, nb_patterns=0):
    if len(towel) == 0:
        # print("Towel is empty")
        return 1
    cur_nb = 0
    for pattern in patterns:
        # print(f"Pattern : --{pattern}--")
        if towel.startswith(pattern):
            # print(towel, pattern)
            # print(f"Pattern found : {pattern}")
            cur_nb += find_all_patterns(
                patterns, towel[len(pattern) :], nb_patterns
            )

    return nb_patterns + cur_nb


def find_pattern(patterns, towel):
    if len(towel) == 0:
        return True
    for pattern in patterns:
        # print(f"Pattern : --{pattern}--")
        if towel.startswith(pattern):
            # print(f"Pattern found : {pattern}")
            if find_pattern(patterns, towel[len(pattern) :]):
                return True
    return False


if __name__ == "__main__":
    patterns, towels = read_content(sys.argv[1])
    # print(f"Towel : --{towels[0]}--")
    # find_pattern(patterns, towels[0])
    nb_possible = 0
    for towel in towels:
        if find_pattern(patterns, towel):
            # print(f"{towel} is possible")
            nb_possible += 1
        else:
            pass
            # print(f"{towel} is impossible")
    print(nb_possible)

    ### Part 2
    sum_up = 0
    for towel in tqdm(towels):
        nb_patterns = find_all_patterns(patterns, towel)
        sum_up += nb_patterns
    print(sum_up)
