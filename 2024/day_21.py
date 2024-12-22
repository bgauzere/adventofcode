import sys
import networkx as nx
import matplotlib.pyplot as plt
import string

def get_codes(filename):
    with open(filename, 'r') as f:
        return [l.strip() for l in f.readlines()]


def get_numkeypad():
    num_keypad = nx.DiGraph()
    for i in range(10):
        num_keypad.add_node(str(i))
    num_keypad.add_node("A")
    num_keypad.add_node(" ")
    

    edges = [("0","A", {"dir": ">", "weight": 1}),
             ("0","2", {"dir": "^", "weight": 1}),
            ("A","0", {"dir": "<", "weight": 1}),
            ("A","3", {"dir": "^", "weight": 1}),
            ("1","4", {"dir": "^", "weight": 1}),
            ("1","2", {"dir": ">", "weight": 1}),
            ("2","1", {"dir": "<", "weight": 1}),
            ("2","5", {"dir": "^", "weight": 1}),
            ("2","3", {"dir": ">", "weight": 1}),
            ("2","0", {"dir": "v", "weight": 1}),
            ("3","2", {"dir": "<", "weight": 1}),
            ("3","6", {"dir": "^", "weight": 1}),
            ("3","A", {"dir": "v", "weight": 1}),
            ("4","7", {"dir": "^", "weight": 1}),
            ("4","5", {"dir": ">", "weight": 1}),
            ("4","1", {"dir": "v", "weight": 1}),
            ("5","2", {"dir": "v", "weight": 1}),
            ("5","8", {"dir": "^", "weight": 1}),
            ("5","4", {"dir": "<", "weight": 1}),
            ("5","6", {"dir": ">", "weight": 1}),
            ("6","9", {"dir": "^", "weight": 1}),
            ("6","3", {"dir": "v", "weight": 1}),
            ("6","5", {"dir": "<", "weight": 1}),
            ("7","4", {"dir": "v", "weight": 1}),
            ("7","8", {"dir": ">", "weight": 1}),
            ("8","5", {"dir": "v", "weight": 1}),
            ("8","9", {"dir": ">", "weight": 1}),
            ("8","7", {"dir": "<", "weight": 1}),
            ("9","6", {"dir": "v", "weight": 1}),
            ("9","8", {"dir": "<", "weight": 1}),
            # ("0", "1", {"dir": ">^", "weight": 2}),
            # ("1", "0", {"dir": "v>", "weight": 2})
            ]
    num_keypad.add_edges_from(edges)
    # nx.draw(num_keypad, with_labels=True)
    # plt.show()
    return num_keypad


def get_dirkeypad():
    dir_keypad = nx.DiGraph()
    dir_keypad.add_node("A")
    dir_keypad.add_node(">")
    dir_keypad.add_node("<")
    dir_keypad.add_node("^")
    dir_keypad.add_node("v")
    dir_keypad.add_node(" ")
    

    edges = [("A",">", {"dir": "v"}),
            ("A","^", {"dir": "<", "weight": 1}),
            ("^","A", {"dir": ">", "weight": 1}),
            ("^","v", {"dir": "v", "weight": 1}),
            ("v","^", {"dir": "^", "weight": 1}),
            ("v",">", {"dir": ">", "weight": 1}),
            ("v","<", {"dir": "<", "weight": 1}),
            (">","v", {"dir": "<", "weight": 1}),
            (">","A", {"dir": "^", "weight": 1}),
            ("<","v", {"dir": ">", "weight": 1}),
            # ("<","^", {"dir": "^>", "weight": 2}),
            # ("^","<", {"dir": "<v", "weight": 2})
            ]
    dir_keypad.add_edges_from(edges,)
    # nx.draw(dir_keypad, with_labels=True)
    # plt.show()
    return dir_keypad

def num_key(x):
    # prio au ^< au lieu de <^     
    # et >v au lieu de v>
    if x == "^":
        return 0
    elif x == ">":
        return 1
    elif x == "v":
        return 2
    else:
        return 3
     
def dir_key(x):
    # prio au >^au lieu de ^>  et v< au lieu de <v
    if x == ">":
        return 0
    elif x == "v":
        return 1
    elif x == "<":
        return 2
    else:
        return 3
def alt_key(x):
     # < sur ^ sur v sur >
    if x == "<":
        return 0
    elif x == "^":
        return 1
    elif x == "v":
        return 2
    else:  
        return 3


def solve_first_keyboard(code):
    num_keypad = get_numkeypad()
    #print(code)
    code = "A" + code
    all_paths = []
    for i in range(1, len(code)):
        paths = []
        for cur_path in nx.all_shortest_paths(num_keypad, code[i-1], code[i]):
            #cur_path = nx.shortest_path(num_keypad, code[i-1], code[i])
            #print(cur_path)
            dir_path = []
            for i in range(1,len(cur_path)):
                e = (cur_path[i-1], cur_path[i])
                dir = num_keypad[e[0]][e[1]]["dir"]
                dir_path.append(dir)
            #dir_path.sort(key=alt_key)
            dir_path.append('A')
            paths.append(dir_path)
        all_paths.append(paths)
    sequences = [""]
    for i in range(len(all_paths)):
        sequences_new = []
        for s in sequences:
            for p in all_paths[i]:
                sequences_new.append(s + "".join(p))
        sequences = sequences_new
    return sequences 

def solve_second_keyboard(code):
    dir_keypad = get_dirkeypad()
    code = "A" + code
    all_paths = []
    for i in range(1, len(code)):
        paths = []
        for cur_path in nx.all_shortest_paths(dir_keypad, code[i-1], code[i]):
            dir_path = []
            for i in range(1,len(cur_path)):
                e = (cur_path[i-1], cur_path[i])
                dir = dir_keypad[e[0]][e[1]]["dir"]
                dir_path.append(dir)
            dir_path.append('A')
            paths.append(dir_path)
        all_paths.append(paths)
    sequences = [""]
    for i in range(len(all_paths)):
        sequences_new = []
        for s in sequences:
            for p in all_paths[i]:
                sequences_new.append(s + "".join(p))
        sequences = sequences_new
    return sequences 



if __name__ == "__main__":
    codes = get_codes(sys.argv[1])
    result = 0

    for code in codes:
        solutions = []
        for sol_1 in solve_first_keyboard(code):
            for sol_2 in solve_second_keyboard(sol_1):
                for sol_3 in solve_second_keyboard(sol_2):
                    solutions.append(sol_3)
        path = min(solutions, key=len)      #print(solutions)
        print(path)
        l = len(path)
        int_code = int("".join([i for i in code if i.isdigit()]))
        print(f"{code} : {l},{int_code}, {l*int_code}")
        result += l*int_code
    print(result)


    """ presque bon : il suffit d'optimiser les directions similaires cote à cote (d ou le sort), avec l'assurance que les directions triées correspondent à un chemin faisable (pas vrai à cause des bords)"""