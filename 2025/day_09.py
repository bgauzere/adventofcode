import sys
import numpy as np
import logging
import matplotlib.pyplot as plt
from tqdm import tqdm 
from collections import deque


 #logging.basicConfig(level=logging.DEBUG)

def display_grid(points, frontiers):
     # Find bounds
    min_x = min(p[0] for p in points)-1
    max_x = max(p[0] for p in points)+1
    min_y = min(p[1] for p in points)-1
    max_y = max(p[1] for p in points)+1

    # Convert points to set of tuples for lookup
    points_set = set(tuple(p) for p in points)

    # Display grid
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in points_set:
                row += "X"
            elif (x, y) in frontiers:
                row += "#"
            elif is_inside_optimized((x,y), points):
                row += "o"
            else:
                row += "."
        print(row)
    
def flood(frontiers):
    """scale pas"""
    # Find bounds
    min_x = min(p[0] for p in frontiers)-1
    max_x = max(p[0] for p in frontiers)+1
    min_y = min(p[1] for p in frontiers)-1
    max_y = max(p[1] for p in frontiers)+1
    start = (min_x, min_y)
    to_visit = deque([start])
    outside = set()
    while to_visit:
        cur = to_visit.popleft()
        outside.add(cur)
        x,y = cur
        if x-1 >= min_x and (x-1,y) not in frontiers and (x-1,y) not in outside:
            to_visit.append((x-1,y))
        if y-1 >= min_y and (x,y-1) not in frontiers and (x,y-1) not in outside:
            to_visit.append((x,y-1))
        if x+1 <= max_x and (x+1,y) not in frontiers and (x+1,y) not in outside:
            to_visit.append((x+1,y))
        if y+1 <= max_y and (x,y+1) not in frontiers and (x,y+1) not in outside:
            to_visit.append((x,y+1))
    return outside

def is_inside(point, frontiers, points):
    max_x = max(p[0] for p in points)+1
    if point in frontiers:
        return True
    # ray tracing
    nb_frontiers_points = sum([1 for i in range(point[0],max_x) if (i,point[1]) in points])
    if (nb_frontiers_points % 2) == 0 and nb_frontiers_points > 0:
        return False
    nb_frontiers_crossed = sum([1 for i in range(point[0],max_x) if (i,point[1]) in frontiers])
    return (nb_frontiers_crossed % 2) == 1



def is_inside_optimizedv2(point, vertices):
    px, py = point
    n = len(vertices)
    
    inside = False

    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        
        # 1. GESTION FRONTIERE (BORD)
        # ---------------------------
        # Si segment horizontal
        if p1[1] == p2[1] == py:
            if min(p1[0], p2[0]) <= px <= max(p1[0], p2[0]):
                return True # Sur le bord
        
        # Si segment vertical
        if p1[0] == p2[0] == px:
            if min(p1[1], p2[1]) <= py <= max(p1[1], p2[1]):
                return True # Sur le bord

        # 2. RAY CASTING (INTERIEUR)
        # --------------------------
        # On ne s'intéresse qu'aux murs VERTICAUX qui sont STRICTEMENT à notre droite.
        # Pourquoi ? Car on lance un rayon vers la droite.
        
        # Est-ce un mur vertical ?
        if p1[0] == p2[0]:
            # Est-il à droite du point ?
            if p1[0] > px:
                # Est-ce que notre Y passe à travers la hauteur de ce mur ?
                # Règle importante : on inclut le bas, on exclut le haut (ou l'inverse)
                # pour éviter de compter 2 fois les coins.
                # Ici : y_min <= y < y_max
                y_min = min(p1[1], p2[1])
                y_max = max(p1[1], p2[1])
                
                if y_min <= py < y_max:
                    inside = not inside

    return inside

def is_inside_optimized(point, vertices):
    x, y = point
    n = len(vertices)
    if point in vertices:
        return True
    intersections = 0 
    for i in range(n):
        xi, yi = vertices[i]
        j=(i+1)%n
        xj, yj = vertices[j]
        if yj == y and yi==y:
            intersect_x = (x == max(xj,xi)) or (x == min(xj,xi))
            if intersect_x : 
                return True 
        if xj==x and xi == x:
            intersect_y = (y == max(yj,yi)) or (y == min(yj,yi))
            if intersect_y : 
                return True 
        # je ne suis plus sur un segment
        # on ne regardent que les segments verticaux
        if xj == xi:
            intersect_y = y > min(yi,yj) and y<max(yi,yj)            
            if intersect_y:
                intersect_x =  x<max(xi,xj)
                if intersect_x:
                    intersections +=1
        
    return (intersections % 2) == 1 

def second(points):
    # on calcule les frontieres
    frontiers = set()
    nb_points = len(points)
    same_dim = 0
    for i,cur_p in tqdm(enumerate(points)):
        next_point = points[(i+1)%nb_points]
        logging.debug(f"{cur_p},{next_point}")
        start = min(cur_p[not(same_dim)],next_point[not(same_dim)])
        end = max(cur_p[not(same_dim)],next_point[not(same_dim)])

        for p in range(start,end+1):
            if same_dim == 0:
                frontier = (cur_p[0],p)
            else:
                frontier = (p,cur_p[1])
            frontiers.add(frontier)
            logging.debug(frontier)
        
        same_dim = not(same_dim)
    logging.debug(len(frontiers))
    logging.debug(frontiers)
    #outside = flood(frontiers)
    #display_grid(points, frontiers)
    #logging.debug(is_inside((1,1), frontiers, points))
    largest_area = 0
    for i,p in tqdm(enumerate(points)):
        for p2 in points:
                # calcul de l'aire
                
                #if aire < 4581864452 and aire > largest_area and aire > 10000:
                # on teste tous les points ! 
                # en haut a gauche
                upper_left = (min(p[0],p2[0]), min(p[1],p2[1]))
                # en bas a droite
                bottom_right = (max(p[0],p2[0]), max(p[1],p2[1]))
                # en haut a droite
                upper_right = (max(p[0],p2[0]), min(p[1],p2[1]))
                # en bas a gauche
                bottom_left = (min(p[0],p2[0]), max(p[1],p2[1]))
                aire = bottom_right[0]-upper_left[0]+1
                aire *= bottom_right[1]-upper_left[1]+1
                if aire > largest_area:
                    # on test les 4 bords du rectangle
                    if is_inside_optimized(upper_left, points) and is_inside_optimized(bottom_right, points) and is_inside_optimized(upper_right, points) and is_inside_optimized(bottom_left, points):
                        center = ((p[0]+p2[0])//2, (p[1]+p2[1])//2)
                        if is_inside_optimized(center, points):                        
                            # test 100 random points sampled in the rectangle
                            sample_ok = True
                            for _ in range(1000):
                                sample_point = (np.random.randint(upper_left[0], bottom_right[0]+1), np.random.randint(upper_left[1], bottom_right[1]+1))
                                if not is_inside_optimized(sample_point, points):
                                    sample_ok = False
                                    break
                            if sample_ok:
                                largest_area = aire
                                border_ok = True
                                for x in range(upper_left[0], bottom_right[0]+1):
                                    # test edge haut
                                    if not is_inside_optimizedv2((x, upper_left[1]), points):
                                        border_ok = False
                                        break
                                    if not is_inside_optimizedv2((x, bottom_left[1]), points):
                                        border_ok = False
                                        break
                                if border_ok:
                                    for y in range(upper_left[1], bottom_right[1]+1):
                                        if not is_inside_optimizedv2((upper_left[0], y), points):
                                            border_ok = False
                                            break
                                        if not is_inside_optimizedv2((upper_right[0], y), points):
                                            border_ok = False
                                        break
                                    if border_ok:
                                        largest_area = aire
                # alternative plus rapide mais pas forcement fiable
                # if is_inside_optimized(upper_left, points) and is_inside_optimized(bottom_right, points) and is_inside_optimized(upper_right, points) and is_inside_optimized(bottom_left, points):
                #     center = ((p[0]+p2[0])//2, (p[1]+p2[1])//2)
                #     if is_inside_optimized(center, points):                        
                #         # test 100 random points sampled in the rectangle
                #         sample_ok = True
                #         for _ in range(1000):
                #             sample_point = (np.random.randint(upper_left[0], bottom_right[0]+1), np.random.randint(upper_left[1], bottom_right[1]+1))
                #             if not is_inside_optimized(sample_point, points):
                #                 sample_ok = False
                #                 break
                #         if sample_ok:
                #             largest_area = aire
    return largest_area

def first():
    with open(sys.argv[1], "r") as f:
        contents = [l.strip() for l in f.readlines()]
        points = []
        for l in contents:
            points.append(tuple([int(i) for i in l.split(",")]))
        logging.debug(len(points))
        largest_area = 0
        for i,p in enumerate(points):
            for p2 in points[i+1:]:
                # calcul de l'aire
                aire = np.abs(p[0]-p2[0]+1)*np.abs(p[1]-p2[1]+1) 
                if aire > largest_area:
                    largest_area = aire
        return largest_area,points
    
    
if __name__ == "__main__":
    largest_area, points  = first()
    print(largest_area)
    print(second(points))