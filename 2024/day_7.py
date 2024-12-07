import sys
import numpy as np
import itertools
from tqdm import tqdm


def test_sequence(numbers, permutation, result):
    cur = numbers[0]
    for n in numbers[1:]:
        op = permutation.pop()
        if op == 0:
            cur += n
        else:
            cur *= n
        if cur > result:
            return False
    return cur == result

def test_sequenceV2(numbers, permutation, result):
    cur = numbers[0]
    for n,op in zip(numbers[1:],permutation):
        if op == 0:
            cur += n
        elif op == 1:
            cur *= n
        else:
            cur = cur * (10 ** len(str(n))) + n
        if cur > result:
            return False
    return cur == result


def second(filename):
    with open(filename, "r") as f:
        content = f.readlines()
        result_sum = 0
        for l in tqdm(content):
            l.strip()
            result, numbers = l.split(":")
            result = int(result)
            numbers = [int(n) for n in numbers.strip().split(" ")]
            
            #print(f"init : {result, numbers}")
            
            nb_operations = len(numbers)-1
            
            for p in itertools.product([0,1,2], repeat=nb_operations):
                if test_sequenceV2(numbers, p, result):
                    #print(f"{result} possible")
                    result_sum += result
                    break
            
        print(f"Result sum : {result_sum}")

def first(filename):
    with open(filename, "r") as f:
        content = f.readlines()
        result_sum = 0
        for l in content:
            l.strip()
            result, numbers = l.split(":")
            result = int(result)
            numbers = [int(n) for n in numbers.strip().split(" ")]
            
            nb_operations = len(numbers)-1
            perms = np.array(list(itertools.product([0,1], repeat=nb_operations)))
            for p in perms:
                if test_sequence(numbers, list(p), result):
                    #print(f"{result} possible")
                    result_sum += result
                    break
            
        print(f"Result sum : {result_sum}")
if __name__ == "__main__":
    second(sys.argv[1])
