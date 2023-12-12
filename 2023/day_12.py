import numpy as np
import sys
from scipy.spatial.distance import cdist
from itertools import combinations
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

if __name__ == "__main__":
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