from tqdm import tqdm
import sys
from dataclasses import dataclass
from collections.abc import Callable
from sympy.ntheory import primefactors, factorint


@dataclass
class Item():
    worry_level: int

    def increase_worry_level(self, operation, operand):
        self.worry_level = operation(self.worry_level, operand)

    def __str__(self):
        return str(self.worry_level)

    def is_divisible_by(self, divisor, common_divisor):
        self.worry_level = self.worry_level % common_divisor
        return self.worry_level % divisor == 0


def multiply(old: int, operand: int):
    return old*operand


def add(old: int, operand: int):
    return old + operand


def power(old: int, _: int):
    return old ** 2


@dataclass
class Monkey():
    items: list[Item]
    operation: Callable[[int, int], int]
    operand: int
    divisor: int
    monkey_if_false: int
    monkey_if_true: int
    nb_inspected = 0

    def no_more_items(self):
        return len(self.items) == 0

    def process_item(self, common_divisor) -> [int, Item]:
        self.nb_inspected += 1
        item = self.items.pop()
        item.increase_worry_level(self.operation, self.operand)
        # item.decrease_worry_level()
        if item.is_divisible_by(self.divisor, common_divisor):
            return self.monkey_if_true, item
        else:
            return self.monkey_if_false, item

    def receive_item(self, item: Item):
        self.items.insert(0, item)

    def __str__(self):
        return "".join([f"{item}," for item in self.items[::-1]])


def parse_ope(line):
    match line[21]:
        case "+":
            operation = add
            operand = int(line[23:])
        case "*":
            if line[23:26] == "old":
                operation = power
                operand = None
            else:
                operation = multiply
                operand = int(line[23:])
    return operation, operand


def parse_monkey(content):
    items = [Item(int(item))
             for item in content[1][15:].split(",") if len(item) > 0]
    items = items[::-1]
    operation, operand = parse_ope(content[2])
    divisor = int(content[3][18:])
    monkey_1 = int(content[4][24:])
    monkey_2 = int(content[5][25:])
    monkey = Monkey(items, operation, operand, divisor, monkey_2, monkey_1)
    return monkey


def parse_monkeys(f):
    monkeys = []
    content = f.readlines()
    content = [line.strip() for line in content]
    for index in range(0, len(content), 7):
        monkey = parse_monkey(content[index:index+8])
        monkeys.append(monkey)
    return monkeys


def print_monkeys(monkeys):
    for i, monkey in enumerate(monkeys):
        print(f"Monkey {i} :  {monkey}")


def get_monkey_business(monkeys):
    business = [monkey.nb_inspected for monkey in monkeys]
    print(business)
    business.sort()
    return business[-1]*business[-2]


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, "r") as f:
        monkeys = parse_monkeys(f)
        divisor = 1
        for monkey in monkeys:
            divisor *= monkey.divisor
        print(divisor)
        # print_monkeys(monkeys)
        for _ in tqdm(range(10000)):
            for monkey in monkeys:
                while(not monkey.no_more_items()):
                    next_monkey_id, item = monkey.process_item(divisor)
                    monkeys[next_monkey_id].receive_item(item)
#            print_monkeys(monkeys)
    print_monkeys(monkeys)
    print(get_monkey_business(monkeys))
