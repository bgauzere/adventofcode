import sys
import logging 

#logging.basicConfig(level=logging.DEBUG)


def is_accessible(case, list_nodes, nb_lines, nb_cols):
    nb_neighbours = 0
    for i in range(max(case[0]-1,0),min(case[0]+2,nb_lines)):
        for j in range(max(case[1]-1,0), min(case[1]+2, nb_cols)):
            if (i,j) in list_nodes:
                nb_neighbours += 1
                logging.debug(f"+1 : {(i,j)} ~ {case}")
    # on retire le centre
    nb_neighbours -= 1
    logging.debug(nb_neighbours)
    return nb_neighbours < 4 
    
def second(to_fork, toilet_papers, nb_lines, nb_cols):
    nb_forked = len(to_fork)
    while(to_fork):
        for toilet_paper in to_fork:
            toilet_papers.remove(toilet_paper)
        to_fork = [c for c in toilet_papers if is_accessible(c,toilet_papers, nb_lines, nb_cols)]
        nb_forked += len(to_fork)
    return nb_forked
        
        
def first():
    n_to_fork = 0
    with open(sys.argv[1],"r") as f:
        content = [c.strip() for c in f.readlines()]
        
        toilet_papers = set()
        nb_lines = len(content)
        nb_cols = len(content[0])
        
        for i,l in enumerate(content):
            for j, c in enumerate(l):
                if c == "@":
                    toilet_papers.add((i,j))
        is_accessible((0,2), toilet_papers, nb_lines, nb_cols)
        to_fork = [c for c in toilet_papers if is_accessible(c,toilet_papers, nb_lines, nb_cols)]
        logging.debug(to_fork)
        return to_fork, toilet_papers, nb_lines, nb_cols
        
               
    
if __name__ == "__main__":
    to_fork, toilet_papers, nb_lines, nb_cols = first()
    print(len(to_fork))
    print(second(to_fork, toilet_papers, nb_lines, nb_cols)) ## un peu long à calculer, ça pourrait etre amélioré