import sys
from tqdm import tqdm
from itertools import pairwise
from collections import defaultdict


def next_secret(number):
    secret = number * 64
    secret = mix(secret, number)
    secret = prune(secret)
    result = int(secret / 32)
    secret = mix(secret, result)
    secret = prune(secret)
    result = secret * 2048
    secret = mix(secret, result)
    secret = prune(secret)
    return secret


def prune(number):
    return number % 16777216


def mix(number, other_number):
    return number ^ other_number


def generate(number):
    for _ in range(2000):
        number = next_secret(number)
    return number


def read_numbers(filename):
    with open(filename) as f:
        data = f.readlines()
        return [int(number.strip()) for number in data]


def part2(numbers):
    # get all sequences
    generated_numbers = []
    for number in tqdm(numbers):
        cur_gen = [number]
        for _ in range(2000):
            number = next_secret(number)
            cur_gen.append(number)
        generated_numbers.append(cur_gen)

    sequences = defaultdict(int)
    for number, generated_number in tqdm(zip(numbers, generated_numbers)):
        sequences_found = set()
        # init sequence
        cur_seq = [
            generated_number[1] - generated_number[0],
            generated_number[2] - generated_number[1],
            generated_number[3] - generated_number[2],
        ]
        for i, (a, b) in enumerate(pairwise(generated_number[3:])):
            before = a % 10
            after = b % 10
            cur_seq.append(after - before)
            if tuple(cur_seq) not in sequences_found:
                sequences_found.add(tuple(cur_seq))
                sequences[tuple(cur_seq)] += after

            cur_seq.pop(0)
    # print(sequences[(-2, 1, -1, 3)])
    print(max(sequences.values()))


if __name__ == "__main__":
    numbers = read_numbers(sys.argv[1])
    # part 1
    # generated_numbers = [generate(number) for number in tqdm(numbers)]
    # print(sum(generated_numbers))
    # # part 2
    part2(numbers)
