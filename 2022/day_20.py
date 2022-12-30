from tqdm import tqdm
import sys


class ListDC():
    def __init__(self, element, p=None, n=None):
        self.element = element
        self.lprev = p
        self.lnext = n

    def __str__(self):
        # ({self.lprev.element}, {self.lnext.element})"
        n = self.lnext.element if self.lnext is not None else "None"
        p = self.lprev.element if self.lprev is not None else "None"

        return f"{self.element} ({p,n})"

    def swap_fw(self):
        """z <-> self <-> b <->c
           z <-> b <-> self <->c
        """
        z = self.lprev
        b = self.lnext
        if b is not None:
            c = b.lnext
        else:
            c = None

        self.lprev = b
        self.lnext = c
        if c is not None:
            c.lprev = self
        if b is not None:
            b.lprev = z
            b.lnext = self
        if z is not None:
            z.lnext = b

    def swap_bw(self):
        """
        w<->z<->self<->b
        w<->self<->z<->b
        """
        z = self.lprev
        b = self.lnext
        if z is not None:
            w = z.lprev
        else:
            w = None
        if w is not None:
            w.lnext = self
        self.lprev = w
        self.lnext = z
        if z is not None:
            z.lprev = self
            z.lnext = b
        if b is not None:
            b.lprev = z


def parse_file(filename):
    with open(filename, "r") as f:
        elements = [int(line.strip()) for line in f.readlines()]

    return elements


def as_list(liste, n):
    l = []
    for _ in range(n):
        l.append(liste)
        liste = liste.lnext
    return l


def process_list(l, elements, verbose=False):
    if(verbose):
        print("-----before-----")
        liste = as_list(elements[0], len(elements))
        print([l.element for l in liste])
    for e in tqdm(elements):
        if verbose:
            print(f"#### {e.element} ####")

        if e.element < 0:
            for _ in range(abs(e.element)):
                e.swap_bw()
        elif e.element > 0:
            for _ in range(e.element):
                e.swap_fw()

        if verbose:
            liste = as_list(elements[0], len(elements))
            print([l.element for l in liste])


def get_0_index(liste):
    for i, l in enumerate(liste):
        if l.element == 0:
            return i


def grove_coordinates(elements):
    liste = as_list(elements[0], len(elements))
    idx = get_0_index(liste)
    n = len(liste)
    coords = []
    for i in [1000, 2000, 3000]:
        coords.append(liste[(idx+i) % len(liste)].element)
    return coords


if __name__ == '__main__':
    filename = sys.argv[1]
    elements = parse_file(filename)
    elements = [ListDC(e) for e in elements]

    for i, e in enumerate(elements):
        e.lnext = elements[(i+1) % len(elements)]
        e.lprev = elements[i-1]

    process_list(elements[0], elements)
    coords = grove_coordinates(elements)
    print(coords)
    print(sum(coords))
