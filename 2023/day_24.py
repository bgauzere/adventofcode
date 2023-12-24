from utils import read_content
import numpy as np
import matplotlib.pyplot as plt



def solve_equation(a1, b1, a2, b2):
    # solve a1t + b1 = a2t + b2 where t is unknown
    t = (b2 - b1) / (a1 - a2)
    return t


def first(content):
    n=len(content)
    directions = []
    positions = []
    for line in content:
        print(line)
        position_str, direction_str = line.split("@")
        position = [int(pos) for pos in position_str.split(",")]
        positions.append(position)
        direction = [int(pos) for pos in direction_str.split(",")]
        directions.append(direction)
    
    pos_x = np.array([a[0] for a in positions])
    pos_y = np.array([a[1] for a in positions])
    dir_x = np.array([a[0] for a in directions])
    dir_y = np.array([a[1] for a in directions])

    # t = np.arange(0, 20)
    # plt.plot(pos_x[0] + t*dir_x[0], pos_y[0] + t*dir_y[0])
    # plt.plot(pos_x[2] + t*dir_x[2], pos_y[2] + t*dir_y[2])
    # plt.show()


    # solve (posx1 +x vecx1 - posx2 -tvecx2 == 0 and posy1 + y vecy1 - posy2 - y vecy2 == 0) 
    #  <=> x (vecx1 - vecx2) = posx2 - posx1 
    #      y (vecy1 - vecy2) = posy2 - posy1

    limits = (200000000000000,400000000000000)
    count_intersections = 0
    for i in range(n):
        for j in range(i+1, n):
            A = np.array([[dir_x[i], -dir_x[j]], [dir_y[i], -dir_y[j]]])
            b = np.array([pos_x[j] - pos_x[i], pos_y[j] - pos_y[i]])
            try:
                x,y = np.linalg.solve(A,b)
            except:
                continue
            if x < 0 or y < 0:
                continue # intersection in the past
            if dir_x[i] == dir_x[j] and dir_y[i] == dir_y[j]:
                continue # parallel
            x,y = pos_x[i] + x*dir_x[i], pos_y[i] + x*dir_y[i]
            if limits[0] <= x <= limits[1] and limits[0] <= y <= limits[1]:
                count_intersections += 1
            print(f"{i}, {j} intersects at {x:.4f},{y:.4f}")
    return count_intersections

                


if __name__ == "__main__":
    content = read_content()
    print(content)
    print(first(content))
