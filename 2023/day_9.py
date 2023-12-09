import sys
import np

def second():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        # lecture des sequenes
        sequences = []
        for l in content:
            sequences.append([int(c) for c in l.split()])
        print(f"{sequences=}")
        #pour chaque sequence
        values_to_add = []
        for sequence in sequences:
            #-> reduction
            print(f"{sequence = }")
            diffs = [sequence]
            while (not all([d == 0 for d in diffs[-1]])):
                diff = list(np.diff(diffs[-1]))
                print(f"{diff = }")
                diffs.append(diff)
            print(f"{diffs = }")

            # -> extension
            diffs = diffs[::-1]
            # on prend à l'envers pour gerer la fin comme le début
            diffs = [diff[::-1] for diff in diffs]
            for i,layer in enumerate(diffs):
                
                if i > 0:
                    #print(f"{layer[-1] = }, {diffs[i-1][-1] = }")
                    layer.append(layer[-1] - diffs[i-1][-1])
                else:
                    layer.append(0)
                #print(i,layer)
                
            values_to_add.append(diffs[-1][-1])
            print(f"{values_to_add[-1] = }")
    return sum(values_to_add)

def first():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        # lecture des sequenes
        sequences = []
        for l in content:
            sequences.append([int(c) for c in l.split()])
        print(f"{sequences=}")
        #pour chaque sequence
        values_to_add = []
        for sequence in sequences:
            #-> reduction
            print(f"{sequence = }")
            diffs = [sequence]
            while (not all([d == 0 for d in diffs[-1]])):
                diff = list(np.diff(diffs[-1]))
                print(f"{diff = }")
                diffs.append(diff)
            print(f"{diffs = }")

            # -> extension
            diffs = diffs[::-1]
            for i,layer in enumerate(diffs):
                print(i)
                if i > 0:
                    layer.append(layer[-1] + diffs[i-1][-1])
                else:
                    layer.append(0)
                print(i,layer)
                
            values_to_add.append(diffs[-1][-1])

    return sum(values_to_add)
if __name__ == '__main__':
    res = second()
    print(res)
    
