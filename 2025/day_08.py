## C'est un pb de CHA avec single linkage, euclidean distance
## On pourrait le faire avec sklearn

import sys
import logging
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm 

from collections import defaultdict

#logging.basicConfig(level=logging.DEBUG)

def euclidean(x,y):
    return np.sqrt(np.sum((x-y)**2))

class Cluster:
    def __init__(self, point):
        self.points = set([point])
        
    def dist(self, other_cluster):
        logging.debug(f"{self}, {other_cluster}")
        d = np.inf
        for p in self.points:
            for o in other_cluster.points:
                cur_d = euclidean(p,o)
                if cur_d < d:
                    d = cur_d
        if d<.1:
            breakpoint()
        return d
    
    def merge(self,other_cluster):
        self.points.add([p for p in other_cluster.points])
        
    def __str__(self):
        return f"{[p for p in self.points]}"
    def __len__(self):
        return len(self.points)
    
def firstv0():
    # je me suis planté, il peut arriver que des connexions se fassent inter clusters ! 
    with open(sys.argv[1],"r") as f:
        content = f.readlines()
        clusters = []
        nb_points = len(content)
        for l in tqdm(content): 
            cluster = Cluster(np.array(([int(i) for i in l.strip().split(",")])))
            clusters.append(cluster)
            
        for c in clusters:
            logging.debug(c)
            
        m_dist = np.ones((nb_points,nb_points))*np.inf
        for i in tqdm(range(nb_points)):
            for j in range(i+1,nb_points):
                m_dist[i,j] = clusters[i].dist(clusters[j])
        
        for _ in  tqdm(range(int(sys.argv[2]))):
            # on trouve la plus petite paire
            ind = np.unravel_index(np.argmin(m_dist, axis=None), m_dist.shape)
            logging.debug(ind)
            # on les merge dans ind[0]
            
            logging.debug(f"Merge de {clusters[ind[1]]} dans {clusters[ind[0]]}")
            clusters[ind[0]].merge(clusters[ind[1]])
            clusters.pop(ind[1])
            
            for j in range(len(m_dist)):
                if j < ind[0]:
                    m_dist[j, ind[0]] = min(m_dist[j, ind[0]], m_dist[j, ind[1]])
                elif j > ind[0]:
                    m_dist[ind[0], j] = min(m_dist[ind[0], j], m_dist[ind[1], j])
            
            # suppression de la colonne ind[1] dans m_dist
            m_dist = np.delete(m_dist, ind[1], axis=0)
            m_dist = np.delete(m_dist, ind[1], axis=1)
            
        logging.debug(clusters)
        logging.debug(len(clusters))
        lengths = [len(c) for c in clusters]
        logging.debug(lengths)
        lengths.sort()
        print(len(lengths))
        breakpoint()
        return lengths[-1]*lengths[-2]*lengths[-3]
                        
def first():
    n=int(sys.argv[2])
    with open(sys.argv[1],"r") as f:
        content = f.readlines()
        points = []
        nb_points = len(content)
        clusters = [i for i in range(nb_points)]
        for l in tqdm(content): 
            data = np.array(([int(i) for i in l.strip().split(",")]))
            points.append(data)
            
        m_dist = np.ones((nb_points,nb_points))*np.inf
        for i in tqdm(range(nb_points)):
            for j in range(i+1,nb_points):
                m_dist[i,j] = np.sum((points[i] - points[j])**2)
        
        # on récupère les 1000 plus petites distances pour initialiser les merges
        distances = m_dist.flatten()
        indices_sorted = distances.argsort()
        top_indices = indices_sorted[:n]
        # on fait les merges
        for ind in top_indices:
            ind = np.unravel_index(ind, m_dist.shape)
            logging.debug(f"{ind} : {points[ind[0]],points[ind[1]] }")
            cluster_to_merge = clusters[ind[1]]
            for i in range(len(clusters)):
                if clusters[i] == cluster_to_merge:
                    clusters[i] = clusters[ind[0]]
        
        sizes = defaultdict(int)    
        for c in clusters:
            sizes[c] += 1
        logging.debug(sizes)
        sizes = list(sizes.values())
        sizes.sort()
        logging.debug(f"{sizes}, {len(sizes)}")
        
        return sizes[-1]*sizes[-2]*sizes[-3], m_dist, points
        
def second(m_dist,points):
    nb_points = len(points)
    #clusters_set = [set(i) for i in range(nb_points)]
    clusters = [i for i in range(nb_points)]
    distances = m_dist.flatten()
    indices_sorted = distances.argsort()
    for ind in indices_sorted:
        ind = np.unravel_index(ind, m_dist.shape)
        logging.debug(f"{ind} : {points[ind[0]],points[ind[1]] }")
        cluster_to_merge = clusters[ind[1]]
        for i in range(len(clusters)):
            if clusters[i] == cluster_to_merge:
                clusters[i] = clusters[ind[0]]
        
        if len(set(clusters)) == 1:
            return points[ind[0]][0] * points[ind[1]][0]
           
if __name__ == "__main__":
    result, m_dist, points = first()
    print(result)
    print(second(m_dist,points))