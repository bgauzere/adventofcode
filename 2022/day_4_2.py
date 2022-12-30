def contains_other(l, other_list):
    """
    on pourrait refaire en comparant les min et max des listes étant donné le coté séquentiel
    """
    return any(other_item in l for other_item in other_list)


if __name__ == '__main__':
    nb_overlaps = 0
    with open("input_day4.txt", "r") as f:
        for line in f:
            line = line.strip()
            first_elf, second_elf = line.split(",")
            ass_first_elf = [int(section) for section in first_elf.split("-")]
            ass_second_elf = [int(section)
                              for section in second_elf.split("-")]
            list_ass_first = list(
                range(ass_first_elf[0], ass_first_elf[1] + 1))
            list_ass_second = list(
                range(ass_second_elf[0], ass_second_elf[1] + 1))
            if contains_other(list_ass_first, list_ass_second) or contains_other(list_ass_second, list_ass_first):
                nb_overlaps += 1
    print(nb_overlaps)
