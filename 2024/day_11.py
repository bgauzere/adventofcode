import sys
from tqdm import tqdm
import functools


@functools.cache
def expand(n, nb_blinks):
    if nb_blinks == 0:
        return 1
    if n == 0:
        return expand(1, nb_blinks-1)
    
    if len(str(n)) % 2 == 0:
        str_n = str(n)
        n_1 = int(str_n[:len(str_n)//2])
        n_2 = int(str_n[len(str_n)//2:])
        return expand(n_1, nb_blinks-1) + expand(n_2, nb_blinks - 1)
    
    return expand(n*2024, nb_blinks-1)

def first(filename, nb_blinks=25):
    with open(filename) as f:
        content = f.readlines()[0].strip()
        numbers = [int(x) for x in content.split(" ")]
        result = 0
        for n in numbers:
            result += expand(n, nb_blinks)
        print(result)



if __name__ == "__main__":
    first(sys.argv[1], 75)