"""Stratégie pour la part 1 : dijkstra sur l'abre des états des lumieres. Chaque arête est un bouton pressé. 
Chaque état est le nombre de fois où un bouton a été préssé
Terminaison : on a atteint l'état demandé"""

import sys
import logging
import heapq
from tqdm import tqdm

#logging.basicConfig(level=logging.DEBUG)

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
            joltages.append(joltage)
        return lights,buttons, joltages
    
    
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
        res += switch_on_lights(l,b)
        logging.debug(f"{res=}")
    return res 
    
if __name__ == "__main__":
    lights,buttons, joltages = parse()
    logging.debug(lights[0])
    logging.debug(buttons[0])
    logging.debug(joltages[0])
    res = first( lights,buttons)
    print(res)