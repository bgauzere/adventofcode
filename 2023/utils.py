import numpy as np
import sys

def read_content():
    file = sys.argv[1]
    with open(file,"r") as f:
        content = f.readlines()
        content = [l.strip() for l in content]
        return content


