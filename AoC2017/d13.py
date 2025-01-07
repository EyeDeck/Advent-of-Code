from aoc import *


def p1():
    acc = 0
    for line in data:
        d, r = line
        if d % ((r - 1) * 2) == 0:
            acc += d * r
    return acc


def p2():
    i = 0
    while True:
        for line in data:
            d, r = line
            if (d + i) % ((r - 1) * 2) == 0:
                break
        else:
            return i
        i += 1


setday(13)

data = parselines(get_ints)

print('part1:', p1())
print('part2:', p2())
