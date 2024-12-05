import sys
import numpy as np

def second(filename):
    enabled = True
    with open(filename, "r") as f:
        data = f.readlines()
        result = 0
        for content in data:
            i=0
            while (i < len(content)):
                if content[i:].startswith("do()"):
                    enabled = True
                    i+=len("do()")
                elif content[i:].startswith("don't()"):
                    enabled = False
                    i+=len("don't()")
                elif content[i:].startswith("mul("):
                    i+=len("mul(")
                    idx, operand = get_operand(content[i:])
                    if idx > 0:
                        i += idx
                        if content[i] == ",":
                            i += 1
                            idx, operand2 = get_operand(content[i:])
                            if idx > 0:
                                i += idx
                                if (content[i]== ")"):
                                    i += 1
                                    print(f" detect : {operand, operand2, operand * operand2, result}")
                                    if enabled:
                                        result += operand * operand2
                else:
                    print(content[i:i+4])
                    i+=1
        print(result)


def get_operand(line):
    i=0
    while (line[i].isdigit()):
        i+=1
    if i > 0:
        return i, int(line[:i])
    else:
        return i, None
def first(filename):
    with open(filename, "r") as f:
        data = f.readlines()
        result = 0
        for content in data:
            i=0
            while (i < len(content)):
                if content[i:].startswith("mul("):
                    i+=len("mul(")
                    idx, operand = get_operand(content[i:])
                    if idx > 0:
                        i += idx
                        if content[i] == ",":
                            i += 1
                            idx, operand2 = get_operand(content[i:])
                            if idx > 0:
                                i += idx
                                if (content[i]== ")"):
                                    i += 1
                                    print(f" detect : {operand, operand2, operand * operand2, result}")
                                    result += operand * operand2
                else:
                    print(content[i:i+4])
                    i+=1
        print(result)
if __name__ == "__main__":
    second(sys.argv[1])