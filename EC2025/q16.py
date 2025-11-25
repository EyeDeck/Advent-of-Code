import math

from ec import *


def build_wall(d, ln):
    l = [0 for _ in range(ln)]
    for interval in d:
        for i in range(interval - 1, ln, interval):
            l[i] += 1
    return l


def get_blocks_for_len(seq, ln):
    return sum(ln // i for i in seq)


def p1():
    data = parse_lines(1, get_ints)[0]

    return get_blocks_for_len(data, 90)


def r_search(wall, seq, ln, n, max_n):
    test_wall = wall.copy()

    for i in range(n - 1, ln, n):
        test_wall[i] -= 1

        if test_wall[i] < 0:
            return False

    if all(i == 0 for i in test_wall):
        return seq

    for i in range(n, max_n):
        r = r_search(test_wall, seq + [i + 1], ln, i + 1, max_n)
        if r:
            return r


def p2():
    data = parse_lines(2, get_ints)[0]
    seq = [1]

    seq = r_search(data, seq, len(data), 1, len(data))
    test_build = build_wall(seq, len(data))
    assert (test_build == data)

    return math.prod(seq)


def p3():
    data = parse_lines(3, get_ints)[0]
    seq = [1]

    seq = r_search(data, seq, len(data), 1, len(data))
    test_build = build_wall(seq, len(data))
    assert (test_build == data)

    target = 202520252025000
    low = 0
    high = target
    while low < high:
        mid = low + (high - low) // 2
        mid_v = get_blocks_for_len(seq, mid)
        if mid_v == target:
            return mid
        elif target < mid_v:
            high = mid
        else:
            low = mid + 1
    if low == high:
        return low-1
    return


setquest(16)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
