from utils import read_content
from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

@dataclass(frozen=True)
class Point():
    line:int
    col:int

    def __str__(self):
        return f"({self.line}, {self.col})"
    
    def neighbours(self, map):
        neighbours = []
        if self.line > 0:
            neighbours.append(Point(self.line-1, self.col))
        if self.line < len(map)-1:
            neighbours.append(Point(self.line+1, self.col))
        if self.col > 0:
            neighbours.append(Point(self.line, self.col-1))
        if self.col < len(map[0])-1:
            neighbours.append(Point(self.line, self.col+1))
        return neighbours



def first(content):
    points = []
    for line, _ in enumerate(content):
        for col, point in enumerate(_):
            if point in [".",">","<","^","v"]:
                points.append(Point(line, col))
    start_point = Point(0,content[0].index("."))
    end_point = Point( len(content)-1, content[-1].index("."))

    edges = []
    for p in points:
        neighbours = p.neighbours(content)
        # if content[p.line][p.col] == ">":
        #     edges.append((p, Point(p.line, p.col+1)))
        #     continue
        # if content[p.line][p.col] == "<":
        #     edges.append((p, Point(p.line, p.col-1)))
        #     continue
        # if content[p.line][p.col] == "^":
        #     edges.append((p, Point(p.line-1, p.col)))
        #     continue
        # if content[p.line][p.col] == "v":
        #     edges.append((p, Point(p.line+1, p.col)))
        #     continue
        # # current p is a "."
        for n in neighbours:
            c_neigh = content[n.line][n.col]
            if c_neigh in [".",">","<","^","v"]:
                edges.append((p, n))
            # if c_neigh == ">" and n.col > p.col:
            #     edges.append((p, n))
            # if c_neigh == "<" and n.col < p.col:
            #     edges.append((p, n))
            # if c_neigh == "^" and n.line < p.line:
            #     edges.append((p, n))
            # if c_neigh == "v" and n.line > p.line:
            #     edges.append((p, n))
        

    
    G = nx.Graph()
    #print(points)
    G.add_nodes_from(points)
    G.add_edges_from(edges)
    intersections = [p for p in points if G.degree(p) > 2]
    G_intersections = nx.DiGraph()
    G_intersections.add_nodes_from(intersections)
    G_intersections.add_node(start_point)
    G_intersections.add_node(end_point)
    queue = deque()
    queue.append((start_point,start_point,0))
    visited = set()
    while len(queue) > 0:
        p,prec,dist = queue.popleft()
        visited.add((p,prec))
        dist += 1
        if p in G_intersections.nodes and p != start_point and p != prec: # intersection 
            if p in G_intersections.neighbors(start_point):
                print(f"edge {prec} -> {p} is not valid")
                continue
            
            else:
                G_intersections.add_edge(prec,p, attr={"dist" : dist})
                dist = 0
                prec = p

        if p != end_point:
            for n in G.neighbors(p):
                if (n,prec) not in visited:
                    queue.append((n,prec,dist))
    # post processing
    prec_end = next(G_intersections.predecessors(end_point))
    neighbours = list(G_intersections.neighbors(prec_end))
    for p in neighbours:
       if p != end_point:
           G_intersections.remove_edge(prec_end,p)
            
    node_pos = {p:(p.col,-p.line) for p in G_intersections.nodes()}

    nx.draw_networkx(G_intersections, with_labels=True, pos=node_pos)
    nx.draw_networkx_edge_labels(G_intersections, pos=node_pos, 
                                 edge_labels={(e[0],e[1]):e[2]['attr']['dist'] for e in G_intersections.edges(data=True)})
    plt.show()

    # nodes_path  = nx.bellman_ford_path(G_intersections, start_point, end_point,weight="dist")
    # length = 0
    # for i in range(len(nodes_path)-1):
    #     length += 1/G_intersections[nodes_path[i]][nodes_path[i+1]]['attr']['dist']
        
    # print(length)

    #print(f"{len(intersections)} intersections")
    color = [p in intersections for p in G.nodes()]


    #print(color)

    # nx.draw_networkx(G, with_labels=True, node_color =color, pos={p:(p.col,-p.line) for p in points})
    # plt.show()

    #cycles = nx.cycle_basis(G,root = start_point)
    #print(cycles)
    paths = nx.all_simple_paths(G_intersections, start_point, end_point)
    print("tadam")
    #print(len(paths))
    max = 0
    for p in paths:
        lenght = sum([G_intersections[p[i]][p[i+1]]['attr']['dist'] for i in range(len(p)-1)])
        if lenght > max:
            max = lenght
            print(max-1)
        
    # breakpoint()
    #return max([len(p) for p in paths]) -1

if __name__ == "__main__":
    content = read_content()
    print(content)
    print(first(content))


