import sys
import numpy as np

def read_equations(filename):
    with open(filename, "r") as file:
        data = [line.strip() for line in file.readlines()]
        equations = []
        equation = {"mat": [], "prize" : []}
        for line in data:
            if len(line) == 0:
                equations.append(equation)
                equation = {"mat": [], "prize" : []}
            elif line.startswith("Button A"):
                line = line.split("+")
                equation["mat"].append((int(line[1].split(",")[0]), int(line[2].strip())))
            elif line.startswith("Button B"):
                line = line.split("+")
                equation["mat"].append((int(line[1].split(",")[0]), int(line[2].strip())))
            elif line.startswith("Prize"):
                line = line.split("=")
                equation["prize"] = ((int(line[1].split(",")[0]), int(line[2].strip())))
        equations.append(equation)
    return equations

def first(filename, second=False):
    equations = read_equations(filename)
    result = 0
    eps = 1e-8
    for eq in equations:
        A = np.array(eq["mat"]).T
        if (np.linalg.matrix_rank(A)< 2):
            print(A)
        b = np.array(eq["prize"])
        if second:
            b = b + 10000000000000
        x = np.linalg.solve(A,b)
        i_x = np.round(x)
        if np.isclose(A@i_x, b, atol=1e-2, rtol=0).all():
            result += i_x[0]*3 + i_x[1]
        else:
            print(f"No solution {np.linalg.norm(A@i_x - b)}")
    print(result)

if __name__ == "__main__":
    first(sys.argv[1], True)