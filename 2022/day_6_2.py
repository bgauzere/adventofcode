import sys


def is_start_marker(code):
    return len(code) == 14 and len(code) == len(set(code))


def detect_start_marker(content):
    code = []
    for i in range(14, len(content)):
        code = content[i-14:i]
        if is_start_marker(code):
            return i
    raise Exception("pas de marqueur trouvé")


if __name__ == '__main__':
    with open(sys.argv[1], "r") as f:
        line = f.readlines()
        content = line[0].strip()
        index_marker = detect_start_marker(content)
    print(index_marker)
