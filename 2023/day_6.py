import sys
import re
from math import prod

def race(time_press, time_total):
    """ retourne la distance parcouru"""
    speed = time_press
    return (time_total - time_press) * speed


def second():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        print(content)
        # first line in Time
        # second line is distance
        times  = [int(content[0].split(":")[1].replace(" ","").strip())] 
        records = [int(content[1].split(":")[1].replace(" ","").strip())]
        print(f"{times=}, {records=}")

        
        nb_races = len(times)
        nb_records_races = []
        for time,record in zip(times, records):
            # test des statégies de pousser pendant k seconds, accelerer à k mm/s, et relacher pour time -k seconds pour avancer
            # Je pense qu' on pourra accélérer tout ca. La fonction est croissante puis décroissante. Il faudrait expliciter la fonction et calculer sa dérivée pour trouver l'optimum. La fonction est concave
            # distance(t) = (t_total - t_press)*t_press
            #                         = t_total * t_press - t_press**2
            #                        \delta =  = t_total - 2 t_press
             #                        \delta = 0 <=> t_press = 1/2 t_total
            # a partir de ça il faudrait déterminer par dichotomie des deux cotés du max quand est ce que l'on descend en dessous du record !
            record_breaks = 0
            for time_press in range(time):
                distance = race(time_press,time)
                if distance > record:
                    record_breaks += 1
            nb_records_races.append(record_breaks)
        return prod(nb_records_races)


def first():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        print(content)
        # first line in Time
        # second line is distance
        times  = [int(c) for c in re.findall(r'\d+', content[0])]
        records = [int(c) for c in re.findall(r'\d+', content[1])]

        nb_races = len(times)
        nb_records_races = []
        for time,record in zip(times, records):
            # test des statégies de pousser pendant k seconds, accelerer à k mm/s, et relacher pour time -k seconds pour avancer
            record_breaks = 0
            for time_press in range(time):
                distance = race(time_press,time)
                if distance > record:
                    record_breaks += 1
            nb_records_races.append(record_breaks)
        return prod(nb_records_races)
if __name__ == '__main__':
    #res = first()
    res = second()
    print(res)
