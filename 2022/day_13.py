import sys


def compare_items(item1, item2):
    if (item1 != item2):
        return item1 < item2
    return None


def compare_lists(l1, l2):
    if isinstance(l1, list) and isinstance(l2, list):
        if len(l2) == 0 and len(l1) > 0:
            return False
        elif len(l1) == 0 and len(l2) > 0:
            return True
        elif len(l1) == 0 and len(l2) == 0:
            return None
        else:
            comp_first_item = compare_lists(l1[0], l2[0])
            if comp_first_item is not None:
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
        content = [line.strip() for line in content]
        print(len(content))
        pairs_of_lists = []
        for i in range(0, len(content), 3):
            left_list = eval(content[i])
            right_list = eval(content[i+1])
            # print(left_list, right_list)
            pairs_of_lists.append([left_list, right_list])
        indices = []
        for i, pair in enumerate(pairs_of_lists, start=1):
            if compare_lists(*pair):
                indices.append(i)

            #print(f"{i} : {compare_lists(*pair)}")
        print(sum(indices))
