from utils import read_content
import re
from dataclasses import dataclass

def xmas_hash(sequence):
    total = 0
    for c in sequence:
        total += ord(c)
        total *= 17
        total = total%256

    return total


def second():
    content = read_content()[0]
    print(content)
    content= content.strip()
    res = 0
    pattern_label = r'^([a-z]+)'
    boxes = [[] for i in range(256)]
    for sequence in content.split(","):
        label = re.match(pattern_label,sequence).group(1)
        hash_label = xmas_hash(label)
        print(f"{label =} : { hash_label=}")
        if "-" in sequence:
            if Lens(label,0) in boxes[hash_label]:
                boxes[hash_label].remove(Lens(label))
        if "=" in sequence:
            focal = int(sequence[-1])
            new_lens = Lens(label, focal)
            if Lens(label) in boxes[hash_label]:
                idx = boxes[hash_label].index(new_lens)
                boxes[hash_label][idx] = new_lens
            else:
                boxes[hash_label].append(new_lens)
    focusing_power = 0
    for i,box in enumerate(boxes):
        if box :
            focus_power_lens = sum([lens.focal*(i+1)*(j+1) for j,lens in enumerate(box)])
            print(f"{i} : {box} /{focus_power_lens}")
            focusing_power += focus_power_lens
    return focusing_power
        

            
            
            
@dataclass
class Lens:
    label : str
    focal:  int =0
    def __eq__(self,other):
        return self.label == other.label

    def __str__(self):
        return f"[{self.label} {self.focal}]"

    
def first():
    #print(xmas_hash("HASH"))
    content = read_content()[0]
    print(content)
    content= content.strip()
    res = 0
    for sequence in content.split(","):
        cur_hash = xmas_hash(sequence)
        print(f"{sequence =} : {cur_hash=}")
        res += cur_hash
    return res
if __name__ == '__main__':
    print(first())
    print(second())
