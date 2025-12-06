import sys
import logging
import math

logging.basicConfig(level=logging.DEBUG)

def first():
    with open(sys.argv[1], "r") as f:
        contents = [l.strip() for l in f.readlines()]
        nb_equations = len([int(i) for i in contents[0].split(" ") if i != ""])
        list_equations = [list() for _ in range(nb_equations)]
        for l in contents[:-1]:
            numbers = [int(i) for i in l.split(" ") if i != ""]
            for j in range(nb_equations):
                list_equations[j].append(numbers[j])
        logging.debug(list_equations)
        grand_total = 0
        operations = [c for c in contents[-1].split(" ") if c != ""]
        logging.debug(operations)
        for op,numbers in zip(operations, list_equations):
            logging.debug(f"{op},{numbers}")
            if op == "*":
                grand_total += math.prod(numbers)
            if op == "+":
                grand_total += sum(numbers)
            
                            
    return grand_total, list_equations, operations

def count_equation(terms,cur_op):
    sub_total = 0
    if len(terms) > 0:
        if cur_op == "*":
            sub_total = math.prod(terms)
        if cur_op == "+":
            sub_total = sum(terms)
        logging.debug(f"{cur_op=}, {sub_total=}")
    return sub_total
    
def second():
    grand_total = 0
    with open(sys.argv[1], "r") as f:
        contents = [l[:-1] for l in f.readlines()]
        nb_numbers = len(contents)-1
        terms = []
        cur_op = contents[-1][0]
        for i, op in enumerate(contents[-1]):
            if op != " ":
                # nouvelle equation quand contents[-1][j] != *
                # on reinitialise tout et on repart 
                grand_total += count_equation(terms,cur_op)
                terms = []
                cur_op=op
            #terme colonne i
            str_term = "".join([contents[j][i] for j in range(nb_numbers) if contents[j][i] != " "])
            logging.debug(f"{str_term=}")
            if str_term:
                term = int(str_term)
                logging.debug(f"{term = }")
                terms.append(term)
        grand_total += count_equation(terms,cur_op)
                
    return grand_total

if __name__ == "__main__":
    # grand_total, list_equations, operations = first()
    # print(grand_total)
    print(second())