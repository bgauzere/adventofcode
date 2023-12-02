import re
import sys
from math import prod

colors = ['blue','green','red']
maxes_hypotheses = { 'blue':14,'green':13,'red':12}
    

def parse_line(line):
    # Utilisation d'une expression régulière pour trouver les paires de chiffres et de couleurs
    matches = re.findall(r'(\d+) (\w+)', line)
    
    # Conversion de chaque paire en tuple (nombre, couleur)
    pairs = [(int(number), color) for number, color in matches]
    
    return pairs

def get_max_colors(pairs):
    maxes = { c : 0 for c in colors}
    for pair in pairs:
        color = pair[1]
        if pair[0] > maxes[color]:
            maxes[color] = pair[0]
    return maxes



def second():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.readlines()
        powers = []
        for l in content:
            l =l.strip()
            match = re.search(r'Game (\d+)', l)
            id_game =  int(match.group(1))
            
            pairs = parse_line(l)
            print(pairs)
            max_colors = get_max_colors(pairs)
            power =prod(max_colors.values())
            powers.append(power)
    return sum(powers)
    

def first():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.readlines()
        games_ok = []
        for l in content:
            l =l.strip()
            match = re.search(r'Game (\d+)', l)
            id_game =  int(match.group(1))
            
            pairs = parse_line(l)
            print(pairs)
            max_colors = get_max_colors(pairs)
            if all([max_colors[c] <= maxes_hypotheses[c] for c in colors]):
                games_ok.append(id_game)
        print(games_ok)
    return sum(games_ok)
            

if __name__ == '__main__':
    #result = first()
    result = second()
    print(result)
