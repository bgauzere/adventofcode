import re
import sys


class Monkey():
    def __init__(self, name, value=None, monkey1=None, monkey2=None, operator=None):
        self.name = name
        self.value = value
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.operator = operator

    def solve(self):
        if self.value is not None:
            return self.value
        else:
            v1 = self.monkey1.solve()
            v2 = self.monkey2.solve()
            self.value = self.operation(v1, v2)
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
        return self.value is not None


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
            #print(name, value, m1, m2, operation)
            monkey = Monkey(name, value, m1, m2, operation)
            # print(name, value, m1, m2, operation,
            #      monkey.is_value, monkey.value)
            monkeys[name] = monkey
    return monkeys


if __name__ == '__main__':
    filename = sys.argv[1]
    monkeys = parse_data(filename)
    for monkey in monkeys.values():
        if not monkey.is_value:
            monkey.monkey1 = monkeys[monkey.monkey1]
            monkey.monkey2 = monkeys[monkey.monkey2]
    value = monkeys["root"].solve()
    print(value)
