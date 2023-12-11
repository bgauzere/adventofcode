import numpy as np
import sys
from scipy.spatial.distance import cdist


def read_content():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        return content


def first():
    content = read_content()
    empty_lines= []
    galaxies = []
    n,p = len(content),len(content[0])
    map_galaxy = np.array([list(l) for l in content])
    print(map_galaxy)
    galaxies = np.where(map_galaxy=="#")
    galaxies = np.vstack(galaxies).T
    map_galaxy = (map_galaxy == "#").astype('int')
 
    empty_lines = np.sum(map_galaxy,axis=1) == 0
    empty_cols = np.sum(map_galaxy,axis=0) == 0

    expansion_factor = 1000000 # 1 for first part
    decalage_lines = np.cumsum(empty_lines)*(expansion_factor -1)
    decalage_cols = np.cumsum(empty_cols)*(expansion_factor -1)
    
    print(f"{decalage_cols =}")
    print(f"{decalage_lines =}")
    # convert galaxys:
    for galaxy in galaxies:
        print(galaxy)
        galaxy[0] += decalage_lines[galaxy[0]]
        galaxy[1] += decalage_cols[galaxy[1]]
        print(galaxy)
    # for i,line in enumerate(content):
    #     galaxy_in_row = False
    #     for j, point in enumerate(line):
    #         if point == "#":
    #             galaxies.append((i, j))
    #             galaxy_in_row = True
    #     if not galaxy_in_row:
    #         empty_lines.append(i)

    dists = cdist(galaxies, galaxies, metric='cityblock')
    print(np.sum(np.triu(dists,1)))
    
    # for i,g1 in enumerate(galaxies):
    #     print(f"{g1}")
    #     for g2 in galaxies[i+1:]:
    #         print(np.abs(g1[0] - g2[0]) + np.abs(g1[1] - g2[1]) )
        
if __name__ == '__main__':
    res = first()
    print(res)
