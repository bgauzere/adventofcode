from sympy import symbols, Eq, solve
import re
import sys


class Monkey():
    def __init__(self, name, value=None, monkey1=None, monkey2=None, operator=None):
        self.name = name
        self.init_value = value
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.operator = operator

    @property
    def value(self):
        if self.name != "humn":
            return self.init_value
        else:
            return 301

    def expr(self, x):
        if self.name == "humn":
            return x
        if self.init_value is not None:
            return self.init_value

        return self.operation(self.monkey1.expr(x), self.monkey2.expr(x))
    # return f"({self.monkey1.get_literal_expr()} {self.operator} {self.monkey2.get_literal_expr()})"

    def contains_humm(self):
        if self.name == "humn":
            return True
        elif self.monkey1 is not None and self.monkey2 is not None:
            return self.monkey1.contains_humm() or self.monkey2.contains_humm()
        return False

    def solve(self):
        if self.init_value is not None:
            return self.value
        else:
            v1 = self.monkey1.solve()
            v2 = self.monkey2.solve()
            self.init_value = self.operation(v1, v2)
            return self.value

    def operation(self, v1, v2):
        match(self.operator):
            case "+":
                return v1 + v2
            case "*":
                return v1 * v2
            case "/":
                return v1/v2
            case "-":
                return v1-v2

    @property
    def is_value(self):
        return self.init_value is not None


def parse_data(filename):
    monkeys = {}
    with open(filename, 'r') as f:
        content = [line.strip() for line in f.readlines()]
        for line in content:
            name = line[:4]
            value = re.findall(r'\d+', line)
            m1 = None
            m2 = None
            operation = None
            if len(value) == 1:
                value = int(value[0])
            else:
                value = None
                m1 = line[6:10]
                operation = line[11]
                m2 = line[13:17]
            # print(name, value, m1, m2, operation)
            monkey = Monkey(name, value, m1, m2, operation)
            # print(name, value, m1, m2, operation,
            #      monkey.is_value, monkey.value)
            monkeys[name] = monkey
    return monkeys


def day_21(filename):
    monkeys = parse_data(filename)
    for monkey in monkeys.values():
        if not monkey.is_value:
            monkey.monkey1 = monkeys[monkey.monkey1]
            monkey.monkey2 = monkeys[monkey.monkey2]
    value = monkeys["root"].solve()
    print(value)


def day_21_bis(filename):
    monkeys = parse_data(filename)
    for monkey in monkeys.values():
        if not monkey.is_value:
            monkey.monkey1 = monkeys[monkey.monkey1]
            monkey.monkey2 = monkeys[monkey.monkey2]

    if monkeys["root"].monkey1.contains_humm():
        unk = monkeys["root"].monkey1
        operand = monkeys["root"].monkey2
    else:
        unk = monkeys["root"].monkey1
        operand = monkeys["root"].monkey2

    value = operand.solve()
    x = symbols('x')
    eq = Eq(unk.expr(x), value)
    sol = solve((eq), (x))
    print(sol)
    # v2 = monkeys["root"].monkey2.contains_humm()

    # print(v1, v2)
    # print(
    #     f"{monkeys['root'].monkey1.get_literal_expr()}={monkeys['root'].monkey2.solve()}")


if __name__ == '__main__':
    filename = sys.argv[1]
    day_21_bis(filename)
