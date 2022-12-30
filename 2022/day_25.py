import sys

M2 = "="
M1 = "-"


def dig2snafu(n):
    assert(-2 <= n <= 2)
    if n == -2:
        return M2
    if n == -1:
        return M1
    return str(n)


def snafu2dig(c):
    if c == M2:
        return -2
    elif c == M1:
        return -1
    else:
        return int(c)


def snafu2int(s):
    p = len(s)-1
    n = 0
    for c in s:
        n += snafu2dig(c)*(5**p)
        p -= 1
    return n


def int2snafu(n):
    if n <= 2:
        return dig2snafu(n)
    reste = n % 5
    q = n // 5
    if reste > 2:
        q += 1
        reste = -5 + reste
    s = int2snafu(q)
    return s+dig2snafu(reste)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        content = [line.strip() for line in f.readlines()]
        sum_snafu = 0
        for number in content:
            n_dec = snafu2int(number)
            print(n_dec)
            sum_snafu += n_dec
        print(sum_snafu)
        print(int2snafu(sum_snafu))

    for n in [1, 3, 5, 10, 15, 20, 2022, 12345, 314159265]:
        print(f"{n:10} -> {int2snafu(n)}")
