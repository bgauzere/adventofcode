import sys

def read_fs(filename):
    with open(filename, "r") as f:
        data = f.readlines()[0].strip()
        disk = []
        for i in range(0,len(data),2):
            id_file = i // 2
            l_file = int(data[i])
            disk.append(("f",id_file,l_file))
            if i+1 < len(data):
                disk.append(("s",int(data[i+1])))

    return disk

def second_gpt(filename):
    disk = read_fs(filename)
    gaps = [(i, block[1]) for i, block in enumerate(disk) if block[0] == "s"]  # Precompute gaps
    files = [(j, block) for j, block in enumerate(disk) if block[0] == "f"]  # Precompute files

    for j, file_block in reversed(files):  # Iterate over files in reverse order
        for i, (gap_index, gap_size) in enumerate(gaps):
            if gap_index >= j:  # Ignore gaps after the current file position
                break
            if gap_size >= file_block[2]:  # Check if the gap fits the file
                # Move the file
                disk[j] = ("s", file_block[2])
                disk[gap_index] = ("s", gap_size - file_block[2])
                disk.insert(gap_index, ("f", file_block[1], file_block[2]))
                
                if disk[gap_index + 1][1] == 0:  # Remove the empty gap if fully used
                    disk.pop(gap_index + 1)
                
                gaps[i] = (gap_index, gap_size - file_block[2])  # Update gap size
                if gaps[i][1] == 0:  # Remove gaps that are fully consumed
                    gaps.pop(i)
                break
    return disk


def second(filename):
    disk = read_fs(filename)
    j = len(disk) -1
    while j >= 0:
        #print(f"j : {j}, disk : {display(disk)}")
        if disk[j][0] == "f":
            # the file to move before "j" in the first gap with enough space
            i=0
            #print(f"File to move : {disk[j]}")
            while (i<j):
                if disk[i][0] == "s" and disk[i][1] >= disk[j][2]:
                    # move the file
                    #print(f"Find a spot for {disk[j]} : {disk[i]}")
                    file_to_move = disk[j]
                    disk[j] = ("s", disk[j][2])
                    # if disk[i][1] == file_to_move[2]:
                    #     disk.pop(i)
                    # else:
                    disk[i] = ("s", disk[i][1] - file_to_move[2])
                    disk.insert(i, ("f", file_to_move[1], file_to_move[2]))
                    break
                i += 1
        j -= 1
    return disk




def first(filename):
    disk = read_fs(filename)
    i = 0
    j = len(disk)
    id_file = None
    while(i<len(disk)):
        while disk[i][0] == "f": # temps d'accés !?
            i += 1
            if i == len(disk):
                return disk
        # filling space disk[i][0] == s
        cur_space = disk.pop(i)[1]
        while cur_space > 0:
            if id_file is None:
                while (disk[-1][0] == "s"):
                    disk.pop()
                _, id_file, l_file = disk.pop()
           
            if l_file == cur_space:
                disk.insert(i, ("f", id_file, l_file))  
                id_file = None
                cur_space=0
                i += 1
            elif l_file < cur_space:
                disk.insert(i, ("f", id_file, l_file))  
                id_file = None
                cur_space= cur_space - l_file
                i += 1
            else: # l_file > cur_space
                disk.insert(i, ("f", id_file, cur_space))
                l_file = l_file - cur_space
                cur_space = 0
                i += 1  
    if id_file is not None:
        disk.append(("f", id_file, l_file))
    return(disk)


def checksum(disk):

    total = 0
    index = 0
    for e in disk:
        if e[0] == "f":
            total += sum([e[1]* (index+j) for j in range(e[2])])
            index += e[2]
        else:
            index += e[1]
    return total


def display(disk):
    to_print = ""
    for i in range(len(disk)):
        if disk[i][0] == "f":
            to_print +=  ''.join([str(disk[i][1])]* disk[i][2])
        else:
            to_print += ''.join(['.'] * disk[i][1])
    return(to_print)

if __name__ == "__main__":
    disk = second_gpt(sys.argv[1])
    print(display(disk))
    print(checksum(disk))