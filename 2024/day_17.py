import sys


class Prog:
    def __init__(self, A, B, C, code):
        self.A = A
        self.B = B
        self.C = C

        self.opcode = []
        self.operands = []

        data = [int(opcode) for opcode in code.split(",")]
        self.code = data
        # for i in range(0,len(data),2):
        #     self.opcode.append(data[i])
        #     self.operands.append(data[i+1])

        self.i = 0

        self.output = []

    def get_operand(self, operand):  #
        if operand <= 3:
            return operand
        if operand == 4:
            return self.A
        if operand == 5:
            return self.B
        if operand == 6:
            return self.C
        return None

    def exec(self):
        if self.i >= len(self.code):
            return False
        opcode = self.code[self.i]
        operand = self.code[self.i + 1]
        combo_operand = self.get_operand(operand)

        if opcode == 0:

            # the adv instruction (opcode 0) performs division.
            #  The numerator is the value in the A register.
            #  The denominator is found by raising 2 to the power of the instruction's combo operand.
            #  (So, an operand of 2 would divide A by 4 (2^2);
            #  an operand of 5 would divide A by 2^B.)
            # The result of the division operation is truncated to an integer
            #  and then written to the A register.
            self.A = self.A // (2**combo_operand)
        if opcode == 1:
            # The bxl instruction (opcode 1) calculates the bitwise XOR of
            # register B and the instruction's literal operand,
            # then stores the result in register B.
            self.B = self.B ^ operand
        if opcode == 2:
            # The bst instruction (opcode 2) calculates the value of its combo
            #  operand modulo 8 (thereby keeping only its lowest 3 bits),
            # then writes that value to the B register.
            self.B = combo_operand % 8
        if opcode == 3:
            # The jnz instruction (opcode 3) does nothing if the A register is 0.
            #  However, if the A register is not zero, it jumps by setting the
            # instruction pointer to the value of its literal operand;
            # if this instruction jumps, the instruction pointer is not increased
            # by 2 after this instruction.
            if self.A != 0:
                self.i = operand - 2
        if opcode == 4:
            # The bxc instruction (opcode 4) calculates the bitwise XOR
            #  of register B and register C, then stores the result in register B.
            #  (For legacy reasons, this instruction reads an operand but ignores it.)
            self.B = self.B ^ self.C
        if opcode == 5:
            # The out instruction (opcode 5) calculates the value of its combo
            # operand modulo 8, then outputs that value.
            # (If a program outputs multiple values, they are separated by commas.)
            self.output.append(combo_operand % 8)
        if opcode == 6:
            # The bdv instruction (opcode 6) works exactly like the adv instruction
            #  except that the result is stored in the B register.
            #  (The numerator is still read from the A register.)
            self.B = self.A // (2**combo_operand)
        if opcode == 7:
            # The cdv instruction (opcode 7) works exactly like the adv instruction
            #  except that the result is stored in the C register.
            # (The numerator is still read from the A register.)
            self.C = self.A // (2**combo_operand)
        self.i += 2
        return True

    def __str__(self):
        return ",".join([str(n) for n in self.output])


def test():
    # If register C contains 9, the program 2,6 would set register B to 1.
    t1 = Prog(0, 0, 9, "2,6")
    t1.exec()
    assert t1.B == 1
    print("Test 1 OK")

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    t2 = Prog(10, 0, 0, "5,0,5,1,5,4")
    while t2.exec():
        pass
    assert str(t2) == "0,1,2"
    print("Test 2 OK")
    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    t3 = Prog(2024, 0, 0, "0,1,5,4,3,0")
    while t3.exec():
        pass
    assert str(t3) == "4,2,5,6,7,7,7,7,3,1,0"
    assert t3.A == 0
    print("Test 3 OK")
    # If register B contains 29, the program 1,7 would set register B to 26.
    t4 = Prog(0, 29, 0, "1,7")
    t4.exec()
    assert t4.B == 26
    print("Test 4 OK")
    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    t5 = Prog(0, 2024, 43690, "4,0")
    t5.exec()
    assert t5.B == 44354
    print("Test 5 OK")


def get_prog(filename):
    with open(filename) as f:
        data = f.readlines()
        A = int(data[0].split(" ")[2])
        B = int(data[1].split(" ")[2])
        C = int(data[2].split(" ")[2])
        code = data[4].split(" ")[1]
        return Prog(A, B, C, code)


def backtrack(base_8_value, target, i=0):
    # Condition de base : si on a rempli tous les chiffres
    if i == len(base_8_value):
        return True

    # Essayer toutes les valeurs possibles pour le chiffre actuel
    for digit in range(8):
        if digit == 0 and i == 0:
            continue
        base_8_value[i] = digit
        print(f"{base_8_value=}")
        # Convertir le nombre en base 10 pour le tester
        value = int("".join(map(str, base_8_value)), 8)
        prog = Prog(value, 0, 0, target)

        # Exécuter le programme pour vérifier la condition
        while prog.exec():
            pass

        # Vérifier si le préfixe du résultat correspond à celui de la cible
        result = str(prog)
        print(f"{result=}")
        j = (i * 2) + 1
        if result[-j:] == target[-j:]:
            # Si valide, continuer avec l'étape suivante
            print(f"{base_8_value=}, {target=}, {result=}")
            if backtrack(base_8_value, target, i + 1):
                return True

    # Si aucune valeur ne fonctionne, revenir en arrière
    base_8_value[i] = 0
    return False


def part1():
    print("Part 1")
    prog = get_prog(sys.argv[1])
    while prog.exec():
        pass
    print(str(prog))


def part2():
    print("Part 2")
    prog = get_prog(sys.argv[1])

    target = ",".join([str(n) for n in prog.code])
    print(f"{target = }")

    value = 117440
    prog = Prog(value, 0, 0, target)
    # Exécuter le programme pour vérifier la condition
    while prog.exec():
        pass

    # Vérifier si le préfixe du résultat correspond à celui de la cible
    result = str(prog)
    print(f"{result=}")
    print(f"{oct(value)=}")

    # la valeur a trouvé à autant de nombres en representation octale que la
    # longueur du programme
    # backtrack sur les nombres octaux
    base_8_value = [0] * ((len(target) // 2) + 1)
    if backtrack(base_8_value, target):
        print(
            "Solution trouvée :",
            base_8_value,
            int("".join(map(str, base_8_value)), 8),
        )
    else:
        print("Aucune solution trouvée.")


def test():
    prog = get_prog(sys.argv[1])

    target = ",".join([str(n) for n in prog.code])
    print(f"{target = }")
    value = 117440
    prog = Prog(value, 0, 0, target)
    # Exécuter le programme pour vérifier la condition
    while prog.exec():
        pass

    # Vérifier si le préfixe du résultat correspond à celui de la cible
    result = str(prog)
    print(f"{result=}")
    print(f"{oct(value)=}")

    while True:
        value = int("".join(map(str, input())), 8)
        print(f"{oct(value)=}")
        print(f"{value=}")

        prog = Prog(value, 0, 0, target)
        # Exécuter le programme pour vérifier la condition
        while prog.exec():
            pass

        # Vérifier selfi le préfixe du résultat correspond à celui de la cible
        result = str(prog)
        print(f"{result=}")


if __name__ == "__main__":
    part2()
    # test()
