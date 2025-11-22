from aoc import *


def p1():
    acc = 0
    g_a, g_b = data
    mask = (1 << 16) - 1
    for _ in range(40_000_000):
        g_a = (g_a * 16807) % 2147483647
        g_b = (g_b * 48271) % 2147483647
        if g_a & mask == g_b & mask:
            acc += 1
    return acc


def p2():
    acc = 0
    g_a, g_b = data
    mask = (1 << 16) - 1
    for _ in range(5_000_000):
        while True:
            g_a = (g_a * 16807) % 2147483647
            if g_a % 4 == 0:
                break
        while True:
            g_b = (g_b * 48271) % 2147483647
            if g_b % 8 == 0:
                break
        if g_a & mask == g_b & mask:
            acc += 1
    return acc


setday(15)

data = [l[0] for l in parselines(get_ints)]

print('part1:', p1())
print('part2:', p2())
