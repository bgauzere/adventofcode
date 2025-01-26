from enum import Enum
import sys
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import copy
from itertools import combinations, chain

class BinaryAdder:
    def __init__(self, gates):
        self.gates = gates # ! attention, dans Gate, on se fait reference à Gate.gates tout ele
        self.outputs = [g for g in gates.keys() if g.startswith("z")]
        self.outputs.sort()
        self.x_inputs = [g for g in gates.keys() if g.startswith("x")]
        self.x_inputs.sort()
        self.y_inputs = [g for g in gates.keys() if g.startswith("y")]
        self.y_inputs.sort()
        self.dimension = len(self.outputs)

    def set_x(self,x):
        for val, g in zip(x,self.x_inputs) :
            self.gates[g].value = val

    def set_y(self,y):
        for val, g in zip(y,self.y_inputs) :
            self.gates[g].value = val

            
    def get_binx(self):
        x = []
        for g in self.x_inputs:
            x.append(str(int(self.gates[g].value)))
        x = "".join(x[::-1])
        return x

    def get_x(self):
        return int(self.get_binx(), 2)

    def get_biny(self):
        y = []
        for g in self.y_inputs:
            y.append(str(int(self.gates[g].value)))
        y = "".join(y[::-1])
        return y

    def get_y(self):
        return int(self.get_biny(), 2)

    def get_output(self):
        bit_string = "".join(
            [str(int(self.gates[g_z].value)) for g_z in self.outputs]
        )
        return bit_string

    def solve(self):
        for g in self.outputs:
            self.gates[g].solve()
        return "".join([str(int(self.gates[g].value)) for g in self.outputs])

    def is_valid(self):
        level = self.min_level_failure(x,y)
        return True if level == -1 else False

    def min_level_failure(self, x=None, y=None):
        self.solve()
        bin_z = bin(self.get_x() + self.get_y())[2:]
        bin_z = bin_z[::-1]
        bit_string = self.get_output()
        print(f"z = {bin_z} {len(bin_z)}")
        print(f"r = {bit_string}, {len(bit_string)}")
        for i, (c_z, c_r) in enumerate(zip(bin_z, bit_string)):
            if c_z != c_r:
                return i
        return -1


    def reset(self):
        for g in self.gates.keys():
            if g not in self.x_inputs and g not in self.y_inputs:
                self.gates[g].reset()

class Gate:
    gates = {}

    def __init__(self, name, value=None, ope1=None, ope2=None, operand=None):
        self.value = value
        self.name = name
        self.gates[name] = self
        self.ope1 = ope1
        self.ope2 = ope2
        self.operand = operand

    def solve(self):
        if self.value is not None:
            return int(self.value)
        else:
            return int(self.calculate())

    def calculate(self):
        if self.operand == "AND":
            self.value = (
                self.gates[self.ope1].solve() & self.gates[self.ope2].solve()
            )
        elif self.operand == "OR":
            self.value = (
                self.gates[self.ope1].solve() | self.gates[self.ope2].solve()
            )
        elif self.operand == "XOR":
            self.value = (
                self.gates[self.ope1].solve() != self.gates[self.ope2].solve()
            )
        return int(self.value)

    def predecessors(self):
        pred = set()
        pred.add(self.ope1)
        pred.add(self.ope2)
        
        if not self.ope1.startswith("x") and not self.ope1.startswith("y"):
            pred = pred | self.gates[self.ope1].predecessors()
        if not self.ope2.startswith("x") and not self.ope2.startswith("y"):
            pred = pred | self.gates[self.ope2].predecessors()
        return pred

    def reset(self):
        self.value = None

    def __str__(self):
        return f"{self.name} : {self.ope1}  {self.operand} {self.ope2}"


def parse_input(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        i = 0
        while len(data[i].strip()) > 0:
            name = data[i][:3]
            value = int(data[i][5])
            Gate(name, value)
            i += 1
        i += 1
        while i < len(data):
            elements = data[i].strip().split(" ")
            ope1 = elements[0]
            ope2 = elements[2]
            operand = elements[1]
            name = elements[-1]
            Gate(name, None, ope1, ope2, operand)
            i += 1

    return None


def part1():
    parse_input(sys.argv[1])
    output_gates = []
    for g in Gate.gates:
        if g.startswith("z"):
            Gate.gates[g].solve()
            output_gates.append(g)
    output_gates.sort(reverse=True)
    print("".join([str(int(Gate.gates[g].value)) for g in output_gates]))
    bit_string = "".join([str(int(Gate.gates[g].value)) for g in output_gates])
    decimal_number = int(bit_string, 2)
    print(decimal_number)

def find_swaps(current_gates, to_swap, level):
    # get all pairs of gates to swap
    results = []
    for i in range(len(to_swap)):
        for j in range(i + 1, len(to_swap)):
            # swap the gates
            print(f"Testing {to_swap[i]} <-> {to_swap[j]} ...")
            gates_copy = copy.deepcopy(current_gates)
            g1 = gates_copy[to_swap[i]]
            g2 = gates_copy[to_swap[j]]

            g1.name, g2.name = g2.name, g1.name
            gates_copy[to_swap[i]] = g2
            gates_copy[to_swap[j]] = g1

            adder = BinaryAdder(gates_copy)

            [
                g.reset()
                for g in gates_copy.values()
                if not g not in adder.x_inputs and g not in adder.y_inputs
            ]
            new_level = adder.min_level_failure()
            if new_level > level:
                print(f"Found a pair that works!")
                print(f"   {g1.name} <-> {g2.name}")
                results.append((g1.name, g2.name, new_level))

    return results

def repair_gates(current_gates, gates_levels, swaps=None):

    """
    Function de réparation des gates
    Faire un swap pour améliorer le min level de  failure, max 4 swaps
    """
    print(f"current swaps : {swaps}")
    if swaps is None:
        swaps = []

    adder = BinaryAdder(current_gates)
    if len(swaps) == 4:
        if adder.is_valid():
            return swaps
        else:
            return False

    # trouver les prochains swaps et tous les tester
    level = adder.min_level_failure()
    print(level)
    to_swap = [
        g
        for g in gates
        if gates_levels[g] == level or gates_levels[g] == level + 1
    ]
    local_swaps = find_swaps(current_gates, to_swap, level)
    local_swaps.sort(key=lambda x: x[2])
    print(f"nb swap to test : {len(local_swaps)}")
    for swap in local_swaps:
        swap_gates = copy.deepcopy(current_gates)
        [
                g.reset()
                for g in swap_gates.values()
                if not g not in adder.x_inputs and g not in adder.y_inputs
        ]
            
        g1, g2, _ = swap
        swap_gates[g1], swap_gates[g2] = swap_gates[g2], swap_gates[g1]
        swap_gates[g1].name = g2
        swap_gates[g2].name = g1
        results = repair_gates(swap_gates, gates_levels, swaps + [swap])
        if results:
            return results
    return False


def find_incorrect_pair(adder, swaps, level, gates_levels,x,y):
    imp_keys = set(adder.x_inputs)|set(adder.y_inputs)|set(adder.outputs)|set(swaps) 
    possible_keys = [g for g in adder.gates.keys() if g not in imp_keys and (gates_levels[g]== level or gates_levels[g]==level+1)]
    #possible_keys.sort()
    print(f"{len(possible_keys)=}")
    print(f"{possible_keys}")
    print(f"{adder.gates['nnr'].value = }, {adder.gates['rqf'].value = }")
    print(f"{adder.gates['x21'].value = }, {adder.gates['y21'].value = }")
    
    
    for swap1,swap2 in combinations(possible_keys, 2):
        print(f"Swap {swap1} <-> {swap2}")
        save_gates = copy.deepcopy(Gate.gates) # i lfaut tout faire sur Gate !! que c'est moche !

        if swap1 in [Gate.gates[swap2].ope1,Gate.gates[swap2].ope2]:
            continue
        if swap2 in [Gate.gates[swap1].ope1,Gate.gates[swap1].ope2]:
            continue
        
        print(Gate.gates[swap1], Gate.gates[swap2])
        Gate.gates[swap1], Gate.gates[swap2] = Gate.gates[swap2], Gate.gates[swap1]
        Gate.gates[swap1].name = swap1
        Gate.gates[swap2].name = swap2
        print(Gate.gates[swap1], Gate.gates[swap2])
        cur_adder = BinaryAdder(Gate.gates)
        
        print(cur_adder.gates[swap1], cur_adder.gates[swap2])
        cur_adder.set_x(x)
        cur_adder.set_y(y)
        cur_adder.reset()
        level = cur_adder.min_level_failure()
        if level == -1:
            print("Found ! ")
            return swap1, swap2
        Gate.gates = save_gates
        
if __name__ == "__main__":

    
    print("Part 1")
    part1()
    print("Part 2")
    # les portes sont hierarchiques
    # calcul des prédécesseurs
    parse_input(sys.argv[1])
    gates_levels = {}
    for i in range(46):
        g = f"z{i:02}"
        gates_levels[g] = i
        pred = Gate.gates[g].predecessors()
        for g in pred:
            if g not in gates_levels:
                gates_levels[g] = i
    gates = list(gates_levels.keys())
    gates.sort()
    adder = BinaryAdder(Gate.gates)

    # Un z(i) a 6 portes de + que z(i+1)
    # Identifier les portes qui posent problème
    # trouver dans le meme level un remplaçant. 
    # Pour chaque problème, trouver le remplacacant, effectuer le swap
    # Voir si le problème est résolu et continuer
    swaps = []
    for i in range(2, 45):
        cur_gate = f"z{i:02}"
        nb_theo = i*6
        nb_real = len(Gate.gates[cur_gate].predecessors())
        print(f"{Gate.gates[cur_gate]}")
        print(f"{i} : {nb_theo = } {nb_real = }")
        to_swap = None
        if nb_theo != nb_real or Gate.gates[cur_gate].operand != "XOR" :
            print(f"Bad gate: {cur_gate}")
            for g in Gate.gates:
                if g not in adder.x_inputs and g not in adder.y_inputs:
                    if gates_levels[g] == i or gates_levels[g] == i+1:
                        if Gate.gates[g].operand == "XOR":
                            if len(Gate.gates[g].predecessors()) == nb_theo:
                                print(f"Swap with {g} : {Gate.gates[g]}")
                                to_swap = g
            # swap gates g and cur_gate
            print(f"swap {cur_gate} with {to_swap}")
            Gate.gates[to_swap], Gate.gates[cur_gate] = Gate.gates[cur_gate], Gate.gates[to_swap]
            Gate.gates[to_swap].name = to_swap
            Gate.gates[cur_gate].name = cur_gate
            swaps.append((cur_gate, to_swap))
    print(swaps)
    
    # plus qu'un a trouver.
    # tester différentes combinaisons de x,y jusqu'à 1 qui ne marche pas. Trouver le swap qui fait marcher et retester

    adder = BinaryAdder(Gate.gates)
    print(adder.min_level_failure())

    while len(swaps) < 4:
        print("test !")
        # test un nouveau x et y
        # si pas bon, tester tous les swaps possibles hormis les swaped, les z, et les x/y
        new_x =  [random.choice([0,1]) for _ in range(45)]
        new_y = [random.choice([0,1]) for _ in range(45)]
        adder.set_x(new_x)
        adder.set_y(new_y)
        adder.reset()
        level = adder.min_level_failure()
        if level != -1:
            print(level)
            last_swap = find_incorrect_pair(adder,
                                            list(chain.from_iterable(swaps)),
                                            level,
                                            gates_levels, new_x,new_y)
            swaps.append(last_swap)
            break
        
    print(",".join(sorted(list(chain.from_iterable(swaps)))))
   # ! marche pas tout le temps, marche avec nnr et rqf
