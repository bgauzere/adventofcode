import sys
from itertools import cycle
import re
import math

def second():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        directions = list(content[0])

        # read nodes
        nodes = {}
        start_nodes = []
        pattern = r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)"
        for  l in content[2:]:
            match = re.search(pattern, l)
            node = match.group(1)
            left = match.group(2)
            right = match.group(3)
            nodes[node] = (left,right)
            if node.endswith('A'):
                start_nodes.append(node)
                
        # parcours
        
        iter_found = []
        for current in start_nodes:
            pool = cycle(directions)
            i= 0
            while (not current.endswith('Z')):
                cur_dir = next(pool)
                #print(current)
                current = nodes[current][0] if cur_dir == 'L' else nodes[current][1]
                i += 1
            iter_found.append(i)
        return math.lcm(*iter_found)
    
def first():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        directions = list(content[0])

        # read nodes
        nodes = {}
        pattern = r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)"
        for  l in content[2:]:
            match = re.search(pattern, l)
            node = match.group(1)
            left = match.group(2)
            right = match.group(3)
            nodes[node] = (left,right)

        # parcours
        current = 'AAA'
        pool = cycle(directions)
        i= 0
        while (current != 'ZZZ'):
            cur_dir = next(pool)
            current = nodes[current][0] if cur_dir == 'L' else nodes[current][1]
            i += 1
        return i
    
if __name__ == '__main__':
    res = second()
    print(res)
