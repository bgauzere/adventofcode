import numpy as np
import sys
import string
import re

def second():
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        mat = []
        result = 0
        nb_games = len(content)
        nb_cards = [1 for _ in range(nb_games)]
        for i,l in enumerate(content):
            l=l.strip()
            l_first,_,l_second  = l.partition("|")
            _,_,l_first = l_first.partition(":")
            
            winning = [int(c) for c in re.findall(r'\d+', l_first)]
            my_numbers = [int(c) for c in re.findall(r'\d+', l_second)]
            nb_common = len(list(set(winning) & set(my_numbers)))
            for j in range(i+1,i+nb_common+1):
                nb_cards[j] += 1*nb_cards[i]
            if nb_common > 0:
                result += 2**(nb_common-1)
            print(f"{winning=}, {my_numbers = }, {nb_common=}")
        return sum(nb_cards)
    
def first():
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        mat = []
        result = 0
        for l in content:
            l=l.strip()
            l_first,_,l_second  = l.partition("|")
            _,_,l_first = l_first.partition(":")
            
            winning = [int(c) for c in re.findall(r'\d+', l_first)]
            my_numbers = [int(c) for c in re.findall(r'\d+', l_second)]
            nb_common = len(list(set(winning) & set(my_numbers)))
            if nb_common > 0:
                result += 2**(nb_common-1)
            print(f"{winning=}, {my_numbers = }, {nb_common=}")
        return result
    

if __name__ == '__main__':
    result = second()
    print(result)
