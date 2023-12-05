import numpy as np
import sys
import string
import re

class Mapping():
    def __init__(self, id):
        """
        ranges : [start, length, destination_start]
        """
        self.id = id
        self.ranges = []
        
    def add_range(self, start, length, destination):
        range_map = {"from":[start, start+length], "offset" : destination - start, "to":[destination, destination+length]}
        self.ranges.append(range_map)


    def map_me(self, ranges_to_map):
        """
        ranges to map : [[start, end], [start, end]]
        """
        final_ranges = []
        stack = ranges_to_map
        #still_to_do = True
        remaining_parts = []
            
        while  stack:
            print(stack)
            start, end = stack.pop()
            for range_map in self.ranges:
                
                if start > range_map["from"][1] or end < range_map["from"][0]:
                    # pas de mapping, le range n'est pas concerné
                    continue
                if start >= range_map["from"][0] or end < range_map["from"][1]:
                    # une partie du range est concernée
                    eff_range_start = max(start, range_map["from"][0])
                    eff_range_end = min(end, range_map["from"][1])
                    final_ranges.append([eff_range_start + range_map["offset"], eff_range_end + range_map["offset"]])
                    # la partie entre start et  eff_range_start reste à faire
                    if start < eff_range_start:
                        remaining_parts.append([start, eff_range_start])
                    # la partie entre end et range_map["from"][1] reste à faire
                    if end > eff_range_end:
                        remaining_parts.append([eff_range_end, end])
        for part in remaining_parts:
            if not self.processed(part):        
                final_ranges.append(part)
        
        if len(final_ranges) == 0:
            return [[start, end]]
        return final_ranges
    
    
    def processed(self, range):
        for r in self.ranges:
            if range[0] >= r["from"][0] and range[1] <= r["from"][1]:
                return True
        return False

    def __str__(self):
        s = f"{self.id} : \n"
        for r in self.ranges:
            s += f"    {r}\n"
        return s
        

def second():
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        
        seed_ranges = [int(c) for c in content[0].split(": ")[1].split(" ")]
        seed_ranges = [[seed_ranges[i], seed_ranges[i]+seed_ranges[i+1]] for i in range(0,len(seed_ranges),2)]
        mappings = []
        current_map = None
        for l in content[1:]:
            if l == "":
                continue
            if l[0] in string.digits:
                # c'est un range
                print(f"range : {l=}")
                destination, start, length = l.split(" ") 
                print(start, destination, length)
                current_map.add_range(int(start), int(length), int(destination))
            elif l[0] in string.ascii_lowercase:
                if current_map is not None:
                    mappings.append(current_map)
                current_id = l.split(" ")[0]
                current_map = Mapping(current_id)
        mappings.append(current_map)

        final_ranges = []

        for seed_range in seed_ranges:
            current_ranges = [seed_range]
            for m in mappings:
                print(f"{current_ranges = }")
                print(f"{str(m)}")
                
                next_ranges = m.map_me(current_ranges)
                current_ranges = next_ranges
            final_ranges.extend(current_ranges)
        print(current_ranges)
        res = min([min(range) for range in final_ranges])
        return res





def first():
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        
        seeds = content[0].split(": ")[1]
        print(seeds)
        seeds = [int(c) for c in seeds.split(" ")]
        mappings = []
        current_map = None
        for l in content[1:]:
            if l == "":
                continue
            if l[0] in string.digits:
                # c'est un range
                print(f"range : {l=}")
                destination, start, length = l.split(" ") 
                print(start, destination, length)
                current_map.add_range(int(start), int(length), int(destination))
            elif l[0] in string.ascii_lowercase:
                if current_map is not None:
                    mappings.append(current_map)
                current_id = l.split(" ")[0]
                current_map = Mapping(current_id)
        mappings.append(current_map)
        min = 10000000000000000000                      
        for seed in seeds:
            print(f"seed : {seed=}")
            for m in mappings:
                seed = m.map_me(seed)
                print(f"{m.id =}, {seed=}")
            if seed < min:
                min = seed
        return min

if __name__ == '__main__':
    result = second()
    print(result)
