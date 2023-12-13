import numpy as np
import sys

def read_content():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        return content


def find_symmetry_colV2(tab):
    n = tab.shape[1]
    for j in range(tab.shape[1]-1):
        # test de j vs j+1
        if np.sum(np.abs(tab[:,j] - tab[:,j+1]))<=1:
            # check if the symmetry is complete up to one thing
            sym_range = min(j+1,n-(j+1))
            debut = j-sym_range+1
            fin = j+1+sym_range
            
            diffs = np.abs(tab[:,debut:j+1] - np.flip(tab[:,j+1:fin],axis=1))
            if np.sum(np.sum(diffs,axis=0)) == 1:
            #if (tab[:,debut:j+1] == np.flip(tab[:,j+1:fin],axis=1)).all():
                # print("symmetry found")
                # print(f"{j=},{sym_range=},{debut =}, {fin =}")
                # print(f"{tab[:,debut:j+1] =}")
                # print(f"{np.flip(tab[:,j+1:fin],axis=1) =}")
                return j
    return None

def find_symmetry_col(tab):
    n = tab.shape[1]
    for j in range(tab.shape[1]-1):
        # test de j vs j+1
        if ((tab[:,j] == tab[:,j+1]).all()):
            # check if the symmetry is complete
            sym_range = min(j+1,n-(j+1))
            debut = j-sym_range+1
            fin = j+1+sym_range
            print(f"{j=},{sym_range=},{debut =}, {fin =}")
            print(f"{tab[:,debut:j+1] =}")
            print(f"{np.flip(tab[:,j+1:fin],axis=1) =}")
            if (tab[:,debut:j+1] == np.flip(tab[:,j+1:fin],axis=1)).all():
                print("symmetry found")
                return j
    return None


# def find_symmetry_line(tab): # ou on pourrait prendre la transposée !
#     n = tab.shape[0]
#     for i in range(tab.shape[0]-1):
#         # test de i vs i+1
#         if ((tab[i,:] == tab[i+1,:]).all()):
#             # check if the symmetry is complete
#             sym_range = min(i,n-i-1)

#             print(f"{j=},{sym_range=}")
#             print(f"{j-sym_range =}, {j+sym_range =}")
#             print(f"{tab[:,j-sym_range+1:j+1] =}")
#             print(f"{np.flip(tab[:,j+1:j+sym_range+1],axis=1) =}")
#             #print(f"{tab[:,j-sym_range:j] =} , {tab[:,j+1:j+sym_range+1] =}")
#             if (tab[:,j-sym_range+1:j+1] == np.flip(tab[:,j+1:j+sym_range+1],axis=1)).all():
#                 print("symmetry found")
#                 return j
#             return i
#     return None


def second():
    # relax match to at most difference of one
    content = read_content()
    notes = []
    cur_note = []
    for l in content:
        if l == "":
            cur_note = (np.array([ l for l in cur_note]) == "#").astype('int') +1
            notes.append(cur_note)
            cur_note = []
        else:
            cur_note.append(list(l))
    cur_note = (np.array([ l for l in cur_note]) == "#").astype('int') +1
    notes.append(cur_note)
            
    total = 0
    for note in notes:
        #print("new note !")
        symmetry_c= find_symmetry_colV2(note)
        if symmetry_c is not None:
            range_c = symmetry_c + 1
            total += range_c
        #print("transpose !!!")
        symmetry_l = find_symmetry_colV2(note.T)
            #print(f"{symmetry_l =}")
            #    if symmetry_l is not None:
        if symmetry_l is not None:
            range_l = symmetry_l + 1
            total += range_l*100

    print(f"{total =}")


def first():
    content = read_content()
    notes = []
    cur_note = []
    for l in content:
        if l == "":
            cur_note = (np.array([ l for l in cur_note]) == "#").astype('int') +1
            notes.append(cur_note)
            cur_note = []
        else:
            cur_note.append(list(l))
    cur_note = (np.array([ l for l in cur_note]) == "#").astype('int') +1
    notes.append(cur_note)
            
    total = 0
    for note in notes:
        symmetry_c= find_symmetry_col(note)
        if symmetry_c is not None:
            range_c = symmetry_c + 1
            total += range_c
        print("transpose !!!")
        symmetry_l = find_symmetry_col(note.T)
            #print(f"{symmetry_l =}")
            #    if symmetry_l is not None:
        if symmetry_l is not None:
            range_l = symmetry_l + 1
            total += range_l*100

    print(f"{total =}")


if __name__ == "__main__":
    second()
    #first()
