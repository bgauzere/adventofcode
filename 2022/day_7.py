import pickle
import sys
import pprint


def compute_size_dir(dir_as_dict, cur_name, sizes):
    if(isinstance(dir_as_dict, int)):
        return dir_as_dict
    size = sum([compute_size_dir(element, cur_name+name, sizes)
                for name, element in dir_as_dict.items()])
    sizes[cur_name] = size
    print(f"{cur_name}:{size}")
    return size


def get_argument_cd(command):
    return command[5:]


def explore_filesystem(commands, filesystem):
    '''
    filesystem is a list of list of list. Each final element is a file encoded by its size size
    '''
    if len(commands) == 0:
        return filesystem

    command = commands.pop()
    if command.startswith("$"):
        if "ls" in command:
            # mode list
            while len(commands) > 0 and not commands[-1].startswith("$"):
                item = commands.pop()
                item = item.strip()
                if item.startswith("dir"):
                    pass
                    # subdir = item[4:]
                    # filesystem[subdir] = {}
                else:
                    size_str, name = item.split(" ")
                    size = int(size_str)
                    filesystem[name] = size
            return explore_filesystem(commands, filesystem)

        if "cd" in command:
            command = command.strip()
            arg = get_argument_cd(command)
            if arg == "/":
                filesystem["/"] = explore_filesystem(commands, {})
                return filesystem
            elif arg == "..":
                return filesystem
            else:
                # on change de dir
                sub_dir = explore_filesystem(commands, {})
                filesystem[arg] = sub_dir
                return explore_filesystem(commands, filesystem)
    return filesystem


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        commands = f.readlines()
        commands = commands[::-1]
        filesystem = explore_filesystem(commands, {})
        pprint.pprint(filesystem)
        sizes = {}
        compute_size_dir(filesystem, "", sizes)

        print("------------")
        total_size = 0
        for name, size in sizes.items():
            if size <= 100000:
                total_size += size
                print(name, size)
        pickle.dump(sizes, open("data.pickle", "wb"))
        print(total_size)
