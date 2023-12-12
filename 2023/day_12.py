import numpy as np
import sys
from scipy.spatial.distance import cdist
from itertools import combinations

from functools import cache
import re
def read_content():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        return content

def check_sequences_ok(springs, sequences):
    pattern = r"#+"  # Matches one or more consecutive "#"
    matches = re.findall(pattern, springs)
    ok = all([len(m) == sequence for m,sequence in zip(matches,sequences)])
    return ok

def first(): #brute force
    content = read_content()
    total_ok = 0
    for l in content:
        data_spring, sequences = l.split()
        print(data_spring)
        
        sequences = [int(s) for s in sequences.split(",")]
        print(sequences)
        # check all possible replacements. If ok, add to the count
        total_number_of_springs = sum(sequences)
        number_of_current_springs = sum([x=="#" for x in data_spring])
        mark_indexes = [i for i, x in enumerate(data_spring) if x == "?"]
        number_of_unknown = len(mark_indexes)
        number_of_springs_to_place = total_number_of_springs - number_of_current_springs
        print(f"{number_of_unknown = }, {number_of_springs_to_place = }")
        # compute how many ways to fill number_of_springs_to_place in mark_indexes
        possibilities = list(combinations(mark_indexes, number_of_springs_to_place))
        number_ok = 0
        for p in possibilities:
            #print(p)
            new_sequence = list(data_spring)
            for i in p:
                new_sequence[i] = "#"
            new_sequence = "".join(new_sequence)
            new_sequence.replace("?", ".")
            if check_sequences_ok(new_sequence, sequences):
                number_ok += 1
        print(f"{number_ok = }")
        total_ok += number_ok
    print(f"{total_ok = }")

def second():
    content = read_content()
    total_ok = 0
    for l in content:
        data_spring, sequences = l.split()
        data_spring = (data_spring+"?")*5
        data_spring = data_spring[:-1]
        print(data_spring)
        sequences = tuple([int(s) for s in sequences.split(",")])
        sequences = sequences*5
        print(sequences)
        cur_ok = nb_ok(data_spring+".", sequences)
        print(f"{cur_ok = }")
        total_ok += cur_ok
    print(f"{total_ok = }")

@cache
def nb_ok(springs, sequences,serie_en_cours=False):
    #print(f"{springs = }, {sequences = }, {sequence = }")
    #print(f"not(springs) = {not(springs)}")
    nb_springs = sum([x=="#" for x in springs])
    nb_marks = sum([x=="?" for x in springs])
    if not(springs):
        if sum(sequences) ==0:
            print(f"Found a solution (1) : {springs = }, {sequences = }")
        return sum(sequences) == 0 #nb_springs == 0
    if not(sequences):
        if set(springs) == set("."):
            print(f"Found a solution (2): {springs = }, {sequences = }")
        return not "#" in springs
    
    if not "#" in springs:#  and sum(sequences) == 0: #nb_springs == 0
        #print(f"Found a solution: {springs = }, {sequences = }")
        if sum(sequences) == 0:
            #print(f"Found a solution (3): {springs = }, {sequences = }, {sequence = }")
            return 1
    if sum(sequences) == 0 and "#" in springs:
        return 0
    
    cur_nb_solutions = 0
    next = springs[0]
    
    if next == "?":
        possibilities = ["#", "."]
    else:
        possibilities = [next]

    for next in possibilities:
        #print(f"{next = }")
        #cur_sequence = sequence + next
        if next == "#":
            if sequences[0] == 0:
                pass #return 0
            else:
                cur_sequences = tuple([sequences[0]-1 , *sequences[1:]])#.copy()
                #cur_sequences[0] -= 1
                #print(f"{next=}")
                cur_nb_solutions += nb_ok(springs[1:], cur_sequences,
                                          serie_en_cours=True)
        else: # next == "."
            if serie_en_cours and sequences[0] == 0: # on l'a terminé, on passe à la suivante
                if len(sequences)>1:
                    #print(f"{next =}")
                    cur_nb_solutions += nb_ok(springs[1:], sequences[1:],
                                              serie_en_cours=False) 
            elif serie_en_cours and sequences[0] > 0:
                pass # on stop, on a cassé la liste
            else:
                #print(f"{next}")
                cur_nb_solutions += nb_ok(springs[1:], sequences,
                                          serie_en_cours=False) 
    return cur_nb_solutions
if __name__ == "__main__":
    second()