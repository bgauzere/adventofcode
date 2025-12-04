""" Within each bank, you need to turn on exactly two batteries;
the joltage that the bank produces is equal to the number formed by the digits
on the batteries you've turned on.
"""
import numpy as np
import sys
import logging

#logging.basicConfig(level=logging.DEBUG)

def first():
    sum_banks=0
    with open(sys.argv[1],"r") as f:
        content = f.readlines()
        for bank in content:
            bank=bank.strip()
            # pas ouf les 4 pacrours de listes...
            # je pourrais les regrouper en remettant en cause l'hypothèse à chaque fois
            list_digits = [int(i) for i in bank]
            k = np.argmax(list_digits[:-1])
            max_voltage_1 = list_digits[k]
            max_voltage_2 = np.max(list_digits[k+1:])
            max_bank = max_voltage_1*10+max_voltage_2
            sum_banks += max_bank
    return sum_banks

def find_next_best(list_digits, k):
    return np.argmax(list_digits[:-(12-k)])
        
    

def second():
    sum_banks = 0
    with open(sys.argv[1],"r") as f:
        content = f.readlines()
        for bank in content:
            bank=bank.strip()
            joltage_digits = np.empty((12))
            list_digits = np.array([int(i) for i in bank])
            for i in range(12):
                logging.debug(f"{list_digits} - {(11-i)} - {list_digits[:-(11-i)]}")
                remaining_need = (11-i)
                if remaining_need>0:
                    k = np.argmax(list_digits[:-remaining_need])
                else:
                    k = np.argmax(list_digits)
                logging.debug(f"k={k}")
                joltage_digits[i] = list_digits[k]
                list_digits=list_digits[k+1:]
                logging.debug(f"joltage_digits[{i}]={joltage_digits[i]}")
            logging.debug(f"joltage_digits={joltage_digits}")
            joltage_bank = sum([x*10**(11-i) for i,x in enumerate(joltage_digits)])
            
            sum_banks += joltage_bank
    return int(sum_banks)

if __name__ == "__main__":
    print(first())
    print(second())