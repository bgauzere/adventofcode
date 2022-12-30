import sys
from functools import cmp_to_key


def compare_items(item1, item2):
    if (item1 == item2):
        return 0
    elif item1 < item2:
        return -1
    else:
        return 1


def compare_lists(l1, l2):
    if isinstance(l1, list) and isinstance(l2, list):
        if len(l2) == 0 and len(l1) > 0:
            return 1
        elif len(l1) == 0 and len(l2) > 0:
            return -1
        elif len(l1) == 0 and len(l2) == 0:
            return 0
        else:
            comp_first_item = compare_lists(l1[0], l2[0])
            if comp_first_item != 0:
                return comp_first_item
            else:
                return compare_lists(l1[1:], l2[1:])

    if isinstance(l1, int) and isinstance(l2, int):
        return compare_items(l1, l2)
    if isinstance(l1, int) and isinstance(l2, list):
        return compare_lists([l1], l2)
    if isinstance(l1, list) and isinstance(l2, int):
        return compare_lists(l1, [l2])

    print(f"problemos: {l1, l2}, {type(l1), type(l2)}")


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.readlines()
        content = [line.strip() for line in content if line.strip() != ""]
        list_of_lists = [eval(line) for line in content]
        div_1 = [[2]]
        div_2 = [[6]]
        list_of_lists.append(div_1)
        list_of_lists.append(div_2)
        list_of_lists.sort(key=cmp_to_key(compare_lists))
        for l in list_of_lists:
            print(l)
        ind_1 = list_of_lists.index(div_1)+1
        ind_2 = list_of_lists.index(div_2)+1
        print(ind_1*ind_2)
