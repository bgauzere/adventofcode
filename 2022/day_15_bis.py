import re
import sys
from dataclasses import dataclass
from tqdm import tqdm


@dataclass(frozen=True)
class Beacon():
    x: int
    y: int

    def coords(self):
        return [self.x, self.y]


@dataclass(frozen=True)
class Sensor():
    x: int
    y: int
    closest_beacon: Beacon

    def coords(self):
        return [self.x, self.y]

    def range(self):
        return manhattan_2D(self.coords(), self.closest_beacon.coords())

    def __str__(self):
        return f"({self.x},{self.y})"


def find_x_y(data):
    return [int(coord) for coord in re.findall(r'[-+]?\d+', data)]


def parse_beacon(line):
    beacon_part = line.split(":")[1]
    x, y = find_x_y(beacon_part)
    return Beacon(x, y)


def parse_sensor(line, beacon):
    sensor_part = line.split(":")[0]
    x, y = find_x_y(sensor_part)
    return Sensor(x, y, beacon)


def get_beacon(beacon, beacons):
    for b in beacons:
        if b == beacon:
            return b


def parse_data(content):
    beacons = set()
    sensors = []
    for line in content:
        beacon = parse_beacon(line)
        beacons.add(beacon)
        sensor = parse_sensor(line, get_beacon(beacon, beacons))
        sensors.append(sensor)
    return beacons, sensors


def manhattan_2D(x, y):
    return sum([abs(i-j) for i, j in zip(x, y)])


def can_be_a_beacon(point_to_test, beacons_and_sensor_pos,
                    sensors):
    if point_to_test in beacons_and_sensors_pos:
        return True
    for sensor in sensors:
        if manhattan_2D(point_to_test, sensor.coords()) <= sensor.range():
            return False
    return True


def merge(limits):
    merged_limits = [limits[0]]
    for limit in limits[1:]:
        # 4 cas : inclut -> rien à faire, dépasse à gauche, dépasse à droite, disjoint
        for existing_limit in merged_limits:
            if limit[0] >= existing_limit[0] and limit[1] <= existing_limit[1]:
                pass
            elif limit[0] >= existing_limit[0] and limit[1] > existing_limit[1]:
                existing_limit[1] = limit[1]  # on étend à droite
            elif limit[0] < existing_limit[0] and limit[1] >= existing_limit[1]:
                existing_limit[0] = limit[0]  # on étend à gauche
            else:  # disjoint
                merged_limits.append(limit)
    return merged_limits


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = [line.strip() for line in f.readlines()]
        beacons, sensors = parse_data(content)
    beacons_and_sensors_pos = [truc.coords() for truc in list(beacons)+sensors]
    print(beacons)
    print(sensors)
    x_min = 0
    x_max = 4000000
    y_min = 0
    y_max = 4000000
    for cur_y in tqdm(range(y_min, y_max)):
        covered_x = []
        for sensor in sensors:
            x, y = sensor.coords()
            diff_y = abs(cur_y - y)
            range_x = [sensor.x-(sensor.range()-diff_y),
                       sensor.x+(sensor.range()-diff_y)]
            if range_x[0] < range_x[1]:
                covered_x.append(range_x)
        ranges = merge(sorted(covered_x, key=lambda i: i[0]))
        # rint(ranges)
