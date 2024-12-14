import sys 

def get_robots(filename):
    positions = []
    velocities = []
    with open(filename, "r") as file:
        data = [line.strip() for line in file.readlines()]
        for line in data:
            line = line.split(" ")
            positions.append([int(x) for x in line[0][3:-1].split(",")])
            velocities.append([int(x) for x in line[1][3:-1].split(",")])
            print(positions[-1], velocities[-1])
        


if __name__ == "__main__":
    pos, vel = get_robots(sys.argv[1])