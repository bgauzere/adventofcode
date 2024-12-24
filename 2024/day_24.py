from enum import Enum
import sys

class Gate():
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
            return  int(self.calculate())
    
    def calculate(self):
        if self.operand == "AND":
            self.value = self.gates[self.ope1].solve() & self.gates[self.ope2].solve()
        elif self.operand == "OR":
            self.value = self.gates[self.ope1].solve() | self.gates[self.ope2].solve()
        elif self.operand == "XOR":
            self.value = self.gates[self.ope1].solve() != self.gates[self.ope2].solve()
        return int(self.value)
    
def parse_input(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        i = 0
        while len(data[i].strip())>0:
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
        



if __name__ == "__main__":
    parse_input(sys.argv[1])
    output_gates = []
    for g in Gate.gates:
        if g.startswith("z"):
            Gate.gates[g].solve()
            output_gates.append(g)
    output_gates.sort(reverse=True)
    print("".join([str(int(Gate.gates[g].value)    ) for g in output_gates]))
    bit_string = "".join([str(int(Gate.gates[g].value)) for g in output_gates])
    decimal_number = int(bit_string, 2)
    print(decimal_number)