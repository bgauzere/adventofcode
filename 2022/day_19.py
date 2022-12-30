import copy
from dataclasses import dataclass
import sys
import re
from tqdm import tqdm


@dataclass
class BluePrint():
    cost_ore: [int, int, int]
    cost_clay: [int, int, int]
    cost_obsidian: [int, int, int]
    cost_geode: [int, int, int]

    def max_ore(self):
        return max(self.cost_ore[0],
                   self.cost_clay[0],
                   self.cost_obsidian[0],
                   self.cost_geode[0])

    def max_clay(self):
        return max(self.cost_ore[1],
                   self.cost_clay[1],
                   self.cost_obsidian[1],
                   self.cost_geode[1])

    def max_obsidian(self):
        return max(self.cost_ore[2],
                   self.cost_clay[2],
                   self.cost_obsidian[2],
                   self.cost_geode[2])

    def max_geode(self):
        return max(self.cost_ore[3],
                   self.cost_clay[3],
                   self.cost_obsidian[3],
                   self.cost_geode[3])


def parse_data(content):
    blueprints = []
    for line in content:
        costs = [int(i) for i in re.findall(r'\d+', line)]
        print(costs)
        cost_ore = [costs[1], 0, 0]
        cost_clay = [costs[2], 0, 0]
        cost_obsidian = [costs[3], costs[4], 0]
        cost_geode = [costs[5], 0, costs[6]]
        cur_bp = BluePrint(cost_ore, cost_clay, cost_obsidian, cost_geode)
        blueprints.append(cur_bp)
    return blueprints


class RobotFactory():
    def __init__(self, bp):
        self.robots = [1, 0, 0, 0]
        self.blueprint = bp
        self.building = [0, 0, 0, 0]
        self.money = [0, 0, 0]
        self.nb_geode_opens = 0

    def copy(self):
        rf = RobotFactory(self.blueprint)
        rf.robots = self.robots.copy()
        rf.building = self.building.copy()
        rf.money = self.money.copy()
        rf.nb_geode_opens = self.nb_geode_opens
        return rf

    def __str__(self):
        return f"rf({self.robots}) : m{self.money,self.nb_geode_opens}"

    def produce(self):
        self.money[0] += self.robots[0]
        self.money[1] += self.robots[1]
        self.money[2] += self.robots[2]
        self.nb_geode_opens += self.robots[3]

    def enough_money(self, cost):
        return all([m >= c for m, c in zip(self.money, cost)])

    def spent(self, cost):
        for i, c in enumerate(cost):
            self.money[i] -= c

    def check_if_possible(self, cost):
        for i, c in enumerate(cost):
            if c > 0 and self.robots[i] == 0:
                return False
        return True

    def build(self, minute, cost, index_robot):
        needs = cost
        if not self.check_if_possible(cost):
            return 0
        required = [h-n for n, h in zip(needs, self.money)]
        #minute += 1
        while any(r < 0 for r in required):  # and minute < 24:
            self.produce()
            required = [h-n for n, h in zip(needs, self.money)]
            minute += 1
        self.spent(cost)
        self.building[index_robot] = 1
        return minute

    def build_ore(self, minute):
        return self.build(minute, self.blueprint.cost_ore, 0)

    def build_clay(self, minute):
        return self.build(minute, self.blueprint.cost_clay, 1)

    def build_obsidian(self, minute):
        return self.build(minute, self.blueprint.cost_obsidian, 2)

    def build_geode(self, minute):
        return self.build(minute, self.blueprint.cost_geode, 3)

    def operate(self):
        for i, r in enumerate(self.building):
            self.robots[i] += r
        self.building = [0, 0, 0, 0]


def find_best_strategy(rf, minute):
    rf.produce()
    rf.operate()
    minute += 1
    #print(f"{minute} : {rf}")
    if minute == 24:
        return rf.nb_geode_opens
    elif minute > 24:
        print(f"problemos : {minute} : {rf}")
        assert(False)
    # new state
    # do nothing
    strategies = []
    # build ore robot
    if rf.robots[0] <= rf.blueprint.max_ore():
        cur_rf = rf.copy()
        minutes_elapsed = cur_rf.build_ore(minute)
        if minutes_elapsed > 0 and minutes_elapsed < 24:
            nb_geode = find_best_strategy(cur_rf, minutes_elapsed)
            strategies.append(nb_geode)
        elif minutes_elapsed >= 24:
            strategies.append(rf.nb_geode_opens + (24-minute-1)*rf.robots[3])

    # build clay robot
    if rf.robots[1] <= rf.blueprint.max_clay():
        cur_rf = rf.copy()
        minutes_elapsed = cur_rf.build_clay(minute)
        if minutes_elapsed > 0 and minutes_elapsed < 24:
            nb_geode = find_best_strategy(cur_rf, minutes_elapsed)
            strategies.append(nb_geode)
        elif minutes_elapsed >= 24:
            strategies.append(rf.nb_geode_opens + (24-minute-1)*rf.robots[3])

    # build obsidian robot
    if rf.robots[2] <= rf.blueprint.max_obsidian():
        cur_rf = rf.copy()
        minutes_elapsed = cur_rf.build_obsidian(minute)
        if minutes_elapsed > 0 and minutes_elapsed < 24:
            nb_geode = find_best_strategy(cur_rf, minutes_elapsed)
            strategies.append(nb_geode)
        elif minutes_elapsed >= 24:
            strategies.append(rf.nb_geode_opens + (24-minute-1)*rf.robots[3])

    # build geode robot
    cur_rf = rf.copy()
    minutes_elapsed = cur_rf.build_geode(minute)
    if minutes_elapsed > 0 and minutes_elapsed < 24:
        nb_geode = find_best_strategy(cur_rf, minutes_elapsed)
        strategies.append(nb_geode)
    elif minutes_elapsed >= 24:
        strategies.append(rf.nb_geode_opens + (24-minute-1)*rf.robots[3])

    return max(strategies)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = [line.strip() for line in f.readlines()]
        blueprints = parse_data(content)
        print(blueprints)
        qualities = []
        for bp in tqdm(blueprints):
            rf = RobotFactory(bp)
            quality = find_best_strategy(rf, 0)
            qualities.append(quality)
            print(quality)
        output = 0
        for i, q in enumerate(qualities):
            output += q*(i+1)
        print(output)
