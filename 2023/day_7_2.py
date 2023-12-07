import sys
from collections import Counter
import string 
# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

# Every hand is exactly one type. From strongest to weakest, they are:
#     Five of a kind, where all five cards have the same label: AAAAA
#     Four of a kind, where four cards have the same label and one card has a different label: AA8AA
#     Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
#     Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
#     Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
#     One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
#     High card, where all cards' labels are distinct: 23456

card_order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3','2', 'J']

# tester les configs avec un len(set(hand))

def sort_hand(hand):
    """convertit hand en une chaine de caractere indiquant en un le type de main,  et deux l'ordre des cartes"""
    output = ""
    hand_set = Counter(hand)
    print(hand_set)
    if 'J' in hand_set.keys():
        if len(hand_set)> 1:
            nb_J = hand_set['J']
            del hand_set['J']
            max_key = max(hand_set,key=lambda x:hand_set[x])
            hand_set[max_key] += nb_J
            
    print(hand_set)
    #print(hand_set)
    #print(max(hand_set.values()))
    if len(hand_set) == 1:
        output += '1'
    elif len(hand_set) == 2:
        # carré ou full
        if max(hand_set.values()) == 4:
            output += '2'
        else:
            output += '3'
        
    elif len(hand_set) == 3:
        # double pair ou three of a kind
        if max(hand_set.values()) == 3:
            output += '4'
        else:
            output += '5'
    elif len(hand_set)==4:
        output += '6'
    else :
        output += '7'
    return output + "".join([string.ascii_lowercase[card_order.index(card)] for card in hand])
        
def first(content):
    hands = []
    for l in content:
        hand, bid = l.split()
        hand = list(hand)
        bid = int(bid)
        hands.append([hand, bid])
        hands.sort(key=lambda x : sort_hand(x[0]))
    print(f"{hands=}")
    print(f"{[sort_hand(hand[0]) for hand in hands] = }")
    sum_bids = 0
    for i, [hand,bid] in enumerate(hands[::-1],1):
        sum_bids += i*bid
    return sum_bids


        

if __name__ == '__main__':
    file = sys.argv[1]
    with open(file,'r') as f:
        content = f.readlines()
        content = [l.strip() for l in content]
    res = first(content)
    print(res)
