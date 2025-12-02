from aoc import *


def is_invalid(i):
    i_str = str(i)
    i_str_len = len(i_str)
    for divisor in range(2, i_str_len + 1):
        if i_str_len % divisor != 0:
            continue

        interval = len(i_str) // divisor
        base = i_str[:interval]
        for offset in range(interval, i_str_len, interval):
            if i_str[offset:offset + interval] != base:
                break
        else:
            return True
    return False


def solve():
    acc_p1 = 0
    acc_p2 = 0
    for range_str in data.split(','):
        l, r = (int(i) for i in range_str.split('-'))
        for i in range(l, r + 1):
            # part 1
            i_str = str(i)
            midpoint = len(i_str) // 2
            if i_str[:midpoint] == i_str[midpoint:]:
                acc_p1 += i

            # part 2
            if is_invalid(i):
                acc_p2 += i
    return acc_p1, acc_p2


if __name__ == '__main__':
    setday(2)

    data = parselines()[0]

    print('part1: %d\npart2: %d' % solve())
