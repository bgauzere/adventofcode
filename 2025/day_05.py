import sys
import logging

logging.basicConfig(level=logging.DEBUG)

class Tree:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.left = None
        self.right = None
        
    def __str__(self, indent=0):
        s = ""
        prefix = "  " * indent
        s = f"{prefix}{self.min, self.max}\n"
        if self.left is not None:
            s += f"{prefix}Gauche:\n{self.left.__str__(indent + 1)}"
        if self.right is not None:
            s += f"{prefix}Droite:\n{self.right.__str__(indent + 1)}"
        return s
        
    def count(self):
        count = 0
        if self.left is not None:
            count += self.left.count()
            self.min = max(self.min, self.left.max+1)
            
        if self.right is not None:
            count += self.right.count()
            self.max = min(self.max, self.right.min-1)
        if self.min > self.max:
            logging.critical("Invalid range: min is greater than or equal to max")
        count += self.max - self.min + 1
        return count

def first():
    with open(sys.argv[1],"r") as f:
        contents = [l.strip() for l in f.readlines()]
        ranges = []
        n = 0
        while contents[n] != "":
            ranges.append([int(c) for c in contents[n].split("-")])
            n += 1
        ingredients = []
        for l in contents[n+1:]:
            ingredients.append(int(l))
        logging.debug(f"{len(ranges)} ranges et {len(ingredients)} ingredients")
        logging.debug(ranges[0])
        nb_fresh =0
        for i in ingredients:
            for r in ranges:
                if i >= r[0] and i<=r[1]:
                    nb_fresh += 1
                    break
        return nb_fresh, ranges


def secondbis(ranges):
    ranges.sort(key = lambda x:x[0])
    return second(ranges)

def second(ranges):
    t = Tree(ranges[0][0], ranges[0][1])
    for r in ranges[1:]:
        current = t
        inserted = False
        while not inserted:
            if r[1] < current.min:
                if current.left is None:
                    current.left = Tree(r[0], r[1])
                    inserted = True
                else:
                    current = current.left
            elif r[0] > current.max:
                if current.right is None:
                    current.right = Tree(r[0], r[1])
                    inserted = True
                else:
                    current = current.right
            else:
                # merge
                current.min = min(current.min, r[0])
                current.max = max(current.max, r[1])
                inserted = True
    logging.debug(t)
    nb = t.count()
    logging.debug(t)
    return nb
   
    
    
if __name__=="__main__":
    nb_fresh, ranges = first()
    print(nb_fresh)
    print(secondbis(ranges))