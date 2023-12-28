from utils import read_content
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import nnls



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

                
def second(content):
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
    pos_z = np.array([a[2] for a in positions])
    dir_x = np.array([a[0] for a in directions])
    dir_y = np.array([a[1] for a in directions])
    dir_z = np.array([a[2] for a in directions])
    
    # plot     
    t = np.arange(0, 20)
    for i in range(len(pos_x)):
        plt.plot(pos_x[i] + t*dir_x[i], pos_y[i] + t*dir_y[i],'o')
    # rock 
    rock = (24, 13, 10, -3, 1, 2)
    plt.plot(24 + t*-3, 13 + t*1,"--")
    plt.show()
    # real_t = [5,3,4,6,1]
        
    rock = np.random.randint(10, size=(6,)) # 24, 13, 10, -3, 1, 2)
    
    for i in range(1000):
        print(i)
        # optimization
        # t unknown
        A = np.zeros((3*n,n))
        b = np.zeros((3*n,))

        for i in range(len(pos_x)):
            A[3*i, i] = rock[3] - dir_x[i]
            A[3*i+1, i] = rock[4] - dir_y[i]
            A[3*i+2, i] = rock[5] - dir_z[i]
            b[3*i] = - (rock[0] - pos_x[i])
            b[3*i+1] = - (rock[1] -pos_y[i])
            b[3*i+2] = - ( rock[2] -pos_z[i])
            
        t = nnls(A,b)[0]
        # print(A@real_t)
        # print(b)
        # print(t)

        # rocks params unknown
        A = np.zeros((3*n,6))
        b = np.zeros((3*n,))
        for i in range(len(pos_x)):
            A[3*i, 0] = 1
            A[3*i,3] = t[i]
            A[3*i+1,1] = 1
            A[3*i+1,4] = t[i]
            A[3*i+2,2] = 1
            A[3*i+2,5] = t[i]
            b[3*i] = pos_x[i] + t[i]*dir_x[i]
            b[3*i+1] = pos_y[i] + t[i]*dir_y[i]
            b[3*i+2] = pos_z[i] + t[i]*dir_z[i]
        
        params = np.linalg.lstsq(A,b,rcond=None)
        #print(params[0])
        rock = list(params[0])
    print(f"{rock =}")
    print(f"{t = }")
    #print(f"position of rock at t = 5 = {,,,})
    # 
if __name__ == "__main__":
    content = read_content()
    print(content)
    #print(first(content))
    print(second(content))
