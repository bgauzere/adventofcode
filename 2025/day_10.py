"""Stratégie pour la part 1 : dijkstra sur l'abre des états des lumieres. Chaque arête est un bouton pressé. 
Chaque état est le nombre de fois où un bouton a été préssé
Terminaison : on a atteint l'état demandé"""

import sys
import logging
import heapq
import scipy
from tqdm import tqdm
from collections import deque

import numpy as np

logging.basicConfig(level=logging.DEBUG)

def parse():
    with open(sys.argv[1],"r") as f:
        #[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        content = f.readlines()
        lights =[] 
        buttons = []
        joltages = []
        for l in content:
            l = l.strip()
            parts = l.split(" ")
            light = parts[0][1:-1]
            
            lights.append(light)
            cur_buttons = []    
            for button in parts[1:-1]:
                cur_buttons.append(tuple([int(i) for i in button[1:-1].split(",")]))
            buttons.append(cur_buttons)
            joltage = parts[-1]
            joltages.append([int(i) for i in joltage[1:-1].split(",")])
        return lights,buttons, joltages
    

def switch_on_lights_v2(light, buttons):
    
    light = sum([2**i if light[i]=="#" else 0 for i in range(len(light))])
    
    # conversion des boutons en bitmask
    b_mask = []
    for b in buttons:
        mask = 0
        for switch in b:
            mask += 2**switch
        b_mask.append(mask)
    
    init_lights = 0
    visited = set()
    queue = deque([(0,init_lights)])

    while queue:
        nb_presses, cur_light = queue.popleft()
        visited.add(cur_light)
        if cur_light == light:
            return nb_presses
        for switch in b_mask:
            new_light = cur_light^switch
            if new_light not in visited:
                queue.append((nb_presses+1,new_light))
    return False

def switch_on_lights(light, buttons):
    light = [1 if light[i]=="#" else 0 for i in range(len(light))]
    init_lights = [0]*len(light)
    priority_queue = [(1, b,init_lights) for b in buttons]

    while priority_queue:
        current_distance, current_button, current_light = heapq.heappop(priority_queue)
        new_light = current_light.copy()
        for switch in current_button:
            logging.debug(f"{switch=}")
            new_light[switch] = (new_light[switch]+1) % 2
        if new_light == light:
            return current_distance
        for button in buttons:
            distance = current_distance + 1
            heapq.heappush(priority_queue, (distance, button, new_light))

def first(lights,all_buttons):
    res = 0
    for l,b in tqdm(zip(lights,all_buttons)):
        res += switch_on_lights_v2(l,b)
        logging.debug(f"{res=}")
    return res 

from scipy.optimize import milp, LinearConstraint, Bounds

def find_joltages(all_buttons, joltages):
    b = np.array(joltages, dtype=int)
    n = len(b)
    m = len(all_buttons)

    # Construire A (n x m) en 0/1
    A = np.zeros((n, m), dtype=int)
    for j, btn in enumerate(all_buttons):
        for i in btn:
            A[i, j] = 1

    # Objectif min sum x_j
    c = np.ones(m, dtype=float)

    # Ax = b (égalité) -> LinearConstraint avec lb=ub=b
    constraints = LinearConstraint(A, lb=b, ub=b)

    # x_j >= 0
    bounds = Bounds(lb=np.zeros(m), ub=np.full(m, np.inf))

    # Variables entières
    integrality = np.ones(m, dtype=int)  # 1 = integer

    res = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)
    logging.debug(f"{res.x=}")
    return res.x.sum()

def second(all_buttons, joltages):
    res = 0
    for b,j in tqdm(zip(all_buttons, joltages)):
        res += find_joltages(b,j)
    return res
    
if __name__ == "__main__":
    lights,buttons, joltages = parse()
    logging.debug(lights[0])
    logging.debug(buttons[0])
    logging.debug(joltages[0])
    res = first( lights,buttons)
    print(res)
    res = second(buttons, joltages)
    print(res)