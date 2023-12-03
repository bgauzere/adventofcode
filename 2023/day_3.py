import numpy as np
import sys
import string
from math import prod

def ind_ok(i,j,n,p):
    return i >= 0 and j>=0 and i < n and j<p

def get_neighbours_indices(i,j,mat):
    indices = []
    n,p = mat.shape
    for ind_l in [i-1,i,i+1]:
        for ind_c in [j-1,j,j+1]:
            if (not (ind_l == i and j == ind_c)) and ind_ok(ind_l,ind_c,n,p):
                    indices.append([ind_l,ind_c])
    return indices

def get_neighbours_values(i,j,length,mat):
    values = []
    n,p = mat.shape
    for ind_l in [i-1,i,i+1]:
        for ind_c in range(j-1,j+length+1):
            if not (ind_l == i) or not (j<=ind_c<j+length):
                if ind_ok(ind_l,ind_c,n,p):
                    values.append(mat[ind_l,ind_c])
    return values

def second():
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        mat = []
        #Creation matrice
        for l in content:
            mat.append(list(l.strip()))
        
        mat_np = np.array(mat)

        numbers = []
        gears = []
        n,p = mat_np.shape
        for i in range(n):
            j=0
            current_number = ""
            while(j<p):
                # gear
                if mat_np[i,j] == "*":
                    gears.append([i,j])
                #part
                if mat_np[i,j] in string.digits:
                    current_number += mat_np[i,j] 
                else:
                    if not current_number == "":
                        numbers.append([i,j-len(current_number),len(current_number),int(current_number)])
                        current_number = ""
                j += 1
            if not current_number == "":
                        numbers.append([i,j-len(current_number),len(current_number),int(current_number)])
                        current_number = ""
        # organisation des parts
        numbers_hash = np.ones((n,p)) #{i:{} for i in range(n)}
        for number in numbers:
            # on span la part sur l'ensemble des ces positions
            for j in range(number[1], number[1]+number[2]):
                numbers_hash[number[0]][j] = number[3]
        ratios = []
        for gear in gears:
            n_ind = get_neighbours_indices(gear[0],gear[1],mat_np)
            parts = []
            for ind in n_ind:
                part = numbers_hash[ind[0],ind[1]]
                if part != 1 : parts.append(part)
            print(f"{gear=} : {parts=}, {n_ind=}")
            parts= list(set(parts))
            if len(parts) ==2:
                ratio = parts[0] * parts[1]
                print(ratio)
                ratios.append(ratio)
        return sum(ratios)
            
    
    
def first():
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        mat = []
        for l in content:
            mat.append(list(l.strip()))
        
        mat_np = np.array(mat)

        # detect nupmber (j'ai pris le probleme a l'envers, on aurait pu d'abord detecter les symboles
        numbers = []
        n,p = mat_np.shape
        for i in range(n):
            j=0
            current_number = ""
            while(j<p):
                if mat_np[i,j] in string.digits:
                    current_number += mat_np[i,j] 
                else:
                    if not current_number == "":
                        numbers.append([i,j-len(current_number),len(current_number),int(current_number)])
                        current_number = ""
                j += 1
            if not current_number == "":
                        numbers.append([i,j-len(current_number),len(current_number),int(current_number)])
                        current_number = ""
                
        print(numbers)
        # get neighbours of numbers
        sum_parts = 0
        for number in numbers:
            neighbours = get_neighbours_values(number[0],number[1],number[2],mat_np)
            print(f"{number =} : {neighbours = }")
            neighbours = [n for n in neighbours if not n in string.digits]
            if set(neighbours) != set(['.']):
                print(set(neighbours))
                sum_parts += number[3]
                
        print(sum_parts)
        


if __name__ == '__main__':
    result = second()
    print(result)
