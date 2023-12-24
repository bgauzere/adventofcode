from utils import read_content
from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt

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
        

    
    G = nx.DiGraph()
    print(points)
    G.add_nodes_from(points)
    G.add_edges_from(edges)
    #nx.draw(G, with_labels=True)
    #plt.show()
    paths = nx.all_simple_paths(G, start_point, end_point)
    # for p in paths:
    #     print(len(p))
    # breakpoint()
    return max([len(p) for p in paths]) -1

if __name__ == "__main__":
    content = read_content()
    print(content)
    print(first(content))


