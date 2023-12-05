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
        self.ranges.append([start, length, destination])


    def map_me(self,input_id):
        for start, length, dest in self.ranges:
            if input_id >= start  and input_id < start+length:
                return dest + input_id - start 
        return input_id


def second():
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        
        seed_ranges = [int(c) for c in content[0].split(": ")[1].split(" ")]
        seeds = []
        # trop long !!
        # faire une réduction de mapping pour avoir la correspondance seed -> soil
        for i in range(0,len(seed_ranges),2):
            print(seed_ranges[i], seed_ranges[i+1])
            seeds.extend([int(c) for c in range(seed_ranges[i], seed_ranges[i]+seed_ranges[i+1],1)])
        print(seeds)
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
        print(min)



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
