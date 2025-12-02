import sys 
from tqdm import tqdm

def identify_valid_id(start, end):
    # tester que les nombres qui ont un nombre de digits pairs
    # 10, 1000
    nb_ok = 0
    sum_ok = 0
    tested = start
    while tested <= end:
        s_tested = str(tested)
        length = len(str(tested))
        if length % 2 == 0:
            mid = length//2
            if s_tested[:mid] == s_tested[mid:]:
                nb_ok += 1
                sum_ok += tested
            tested += 1
        else:
            tested = 10**(len(str(tested)))
    return nb_ok, sum_ok

def first():
    with open(sys.argv[1],"r") as f:
        content = f.read()
    content=content.strip()
    total_int = 0
    for range in content.split(","):
        start, end = [int(x) for x in range.split("-")]
        #print(start,end, end-start)
        nb_ok, sum_ok = identify_valid_id(start,end)
        total_int += sum_ok
    return total_int



def identify_valid_id_optimized(start, end):
    ## from gemini ! 
    total_count = 0
    total_sum = 0
    
    # On récupère le nombre de chiffres de start et end
    len_start = len(str(start))
    len_end = len(str(end))
    
    # On itère sur toutes les longueurs possibles
    for length in range(len_start, len_end + 1):
        # On ne s'intéresse qu'aux longueurs paires
        if length % 2 != 0:
            continue
            
        k = length // 2
        multiplier = 10**k + 1
        
        # Le motif x doit avoir k chiffres, donc x est dans [lower_bound_x, upper_bound_x]
        # Ex pour k=2 (nombres de 4 chiffres) : x est entre 10 et 99.
        min_x_theoretical = 10**(k - 1)
        max_x_theoretical = (10**k) - 1
        
        # On calcule les bornes de x qui satisfont : start <= x * multiplier <= end
        # x >= start / multiplier
        # x <= end / multiplier
        
        # Division entière plafond (ceil) pour le début
        min_x_req = (start + multiplier - 1) // multiplier
        # Division entière plancher (floor) pour la fin
        max_x_req = end // multiplier
        
        # On prend l'intersection entre les bornes théoriques (liées aux digits)
        # et les bornes requises (liées à start/end)
        current_min = max(min_x_theoretical, min_x_req)
        current_max = min(max_x_theoretical, max_x_req)
        
        if current_min <= current_max:
            # Nombre de termes
            count = current_max - current_min + 1
            
            # Somme d'une suite arithmétique : nombre_termes * (premier + dernier) / 2
            # Ici la somme des x est : count * (current_min + current_max) / 2
            # La somme des nombres complets est : multiplier * somme_des_x
            sum_x = count * (current_min + current_max) // 2
            current_sum = sum_x * multiplier
            
            total_count += count
            total_sum += current_sum

    return total_count, total_sum

def identify_valid_id_v2(start, end):
    # tester que les nombres qui ont un nombre de digits pairs
    # 10, 1000
    nb_ok = 0
    sum_ok = 0
    tested = start
    for tested in tqdm(range(start,end+1)):
        s_tested = str(tested)
        length = len(str(tested))
        is_ok = False
        for pot_subsize in range(1,(length//2)+1):
            if length % pot_subsize == 0:
                if len({s_tested[i:i+pot_subsize]for i in range(0,length,pot_subsize)})==1:
                    is_ok = True
                    #print(s_tested)
                    break
        if is_ok:
            sum_ok += tested
    return nb_ok, sum_ok


def second():
    with open(sys.argv[1],"r") as f:
        content = f.read()
    content=content.strip()
    total_int = 0
    for range in content.split(","):
        start, end = [int(x) for x in range.split("-")]
        #print(start,end, end-start)
        nb_ok, sum_ok = identify_valid_id_v2(start,end)
        total_int += sum_ok
    return total_int

if __name__ == "__main__":
    print(first())
    print(second())
