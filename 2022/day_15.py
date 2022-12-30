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


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = [line.strip() for line in f.readlines()]
        beacons, sensors = parse_data(content)
    beacons_and_sensors_pos = [truc.coords() for truc in list(beacons)+sensors]
    print(beacons_and_sensors_pos)
    print([2, 10] in beacons_and_sensors_pos)
    print(beacons)
    print(sensors)
    x_min = 10000000
    x_max = 0
    for sensor in sensors:
        if x_min > sensor.x - sensor.range():
            x_min = sensor.x - sensor.range()
        if x_max < sensor.x + sensor.range():
            x_max = sensor.x + sensor.range()
    covered_x = []
    y_test = 2000000
    print(x_min, x_max)
    for x in tqdm(range(x_min, x_max)):
        point_to_test = [x, y_test]
        if not can_be_a_beacon(point_to_test, beacons_and_sensors_pos, sensors):
            covered_x.append(point_to_test)
    # for point in covered_x:
    #     print(point)
    print(f"{len(covered_x)}")
