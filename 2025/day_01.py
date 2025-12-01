"""
A rotation starts with an L or R which indicates whether the rotation should be to the left (toward lower numbers) or to the right (toward higher numbers). Then, the rotation has a distance value which indicates how many clicks the dial should be rotated in that direction.
Because the dial is a circle, turning the dial left from 0 one click makes it point at 99. Similarly, turning the dial right from 99 one click makes it point at 0.
The actual password is the number of times the dial is left pointing at 0 after any rotation in the sequence.
"""
import sys

def second():
    dial = 50
    password = 0
    with open(sys.argv[1], "r") as f:
        content = f.readlines()
        for l in content:
            l=l.strip()
            dir = l[0]
            if dial == 0 and dir == "L":
                password -=1
            steps = int(l[1:])
            #print(f"{dir=}, {steps=}")
            password += steps // 100
            #breakpoint()
            if dir == "L":
                dial = dial - steps%100
            else:
                dial = dial + steps%100
            if dial >= 100:
                password +=1
            if dial <= 0 :
                password +=1
            dial = dial % 100
            #print(f"{password=}, {dial=}")
    return password  

def first():
    dial = 50
    password = 0
    with open(sys.argv[1], "r") as f:
        content = f.readlines()
        for l in content:
            l=l.strip()
            dir = l[0]
            steps = int(l[1:])
            #print(dial, dir, steps)
            if dir == "L":
                dial = dial - steps%100
            else:
                dial = dial + steps%100
            if dial >= 100:
                dial -= 100
            if dial < 0 :
                dial = 100-abs(dial)
            #print(dial)
            if dial == 0:
                password += 1
    return password

if __name__ == "__main__":
    print(first())
    print(second())
