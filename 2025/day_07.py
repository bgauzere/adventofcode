import sys
import logging
from tqdm import tqdm
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)


def second():
    with open(sys.argv[1], "r") as f:
        contents = [l.strip() for l in f.readlines()]
        beams = {}
        start = contents[0].find("S")
        logging.debug(f"{start}")
        beams[start] = 1
        logging.debug(beams)
                
        nb_tachyon_beams = 1
        for l in tqdm(contents[1:]):
            nb_separations = 0
            separators = [i for i in range(len(l)) if l[i] == "^"]
            if separators:
                new_beams = defaultdict(int)
                for beam in beams.keys():
                    if beam in separators:
                        new_beams[beam-1] += beams[beam]  
                        new_beams[beam + 1] += beams[beam]
                    else:
                        new_beams[beam] += beams[beam]
                beams = new_beams  
            logging.debug(beams)
            nb_tachyon_beams = sum(beams.values())  
            logging.debug(nb_tachyon_beams)
        return nb_tachyon_beams

def first():
    with open(sys.argv[1], "r") as f:
        contents = [l.strip() for l in f.readlines()]
        beams = set()
        start = contents[0].find("S")
        logging.debug(f"{start}")
        beams.add(start)
        nb_separations = 0
        for l in contents[1:]:
            separators = [i for i in range(len(l)) if l[i] == "^"]
            if separators:
                new_beams = set()
                for beam in beams:
                    if beam in separators:
                        new_beams.add(beam -1)
                        new_beams.add(beam + 1)
                        nb_separations += 1
                    else:
                        new_beams.add(beam)
                beams = new_beams
        return nb_separations
                    
if __name__ =="__main__":
    print(first())
    print(second())