import sys

def read_content(filename):
    with open(filename) as f:
        data = f.readlines()
        patterns = [towel.strip() for towel in data[0].strip().split(",")]
        towels = []
        for towel in data[2:]:
            towels.append(towel.strip())
        return patterns, towels
    
def find_pattern(patterns, towel):
    if len(towel) == 0:
        return True
    for pattern in patterns:
        #print(f"Pattern : --{pattern}--")
        if towel.startswith(pattern):
            #print(f"Pattern found : {pattern}")
            if find_pattern(patterns, towel[len(pattern):]):
                return True
    return False

if __name__ == "__main__":
    patterns, towels = read_content(sys.argv[1])
    #print(f"Towel : --{towels[0]}--")
    #find_pattern(patterns, towels[0])
    nb_possible = 0
    for towel in towels:
        if find_pattern(patterns, towel):
            print(f"{towel} is possible")
            nb_possible += 1
        else:
            print(f"{towel} is impossible")
    print(nb_possible)