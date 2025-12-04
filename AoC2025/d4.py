
from aoc import *


def p1():
    acc = 0

    rolls = set(inverse['@'])
    for point in rolls:
        ct = 0
        for d in DIAGDIRS:
            o = vadd(d, point)
            if o in rolls:
                ct += 1
        if ct < 4:
            acc += 1

    return acc


def p2():
    rolls = set(inverse['@'])
    start = len(rolls)
    last = 0
    while True:
        to_remove = set()
        for point in rolls:
            ct = 0
            for d in DIAGDIRS:
                o = vadd(d, point)
                if o in rolls:
                    ct += 1
            if ct < 4:
                to_remove.add(point)
        rolls -= to_remove
        last_temp = last
        last = len(rolls)
        if last_temp == last:
            return start - last


if __name__ == '__main__':
    setday(4)

    grid, inverse, unique = parsegrid()

    print('part1:', p1() )
    print('part2:', p2() )
