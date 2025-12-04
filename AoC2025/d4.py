from aoc import *


def p1():
    return sum(1 for p in rolls if sum(1 for d in DIAGDIRS if vadd(d, p) in rolls) < 4)


def p2():
    r = rolls.copy()
    while (n := {p for p in r if sum(vadd(d, p) in r for d in DIAGDIRS) >= 4}) != r:
        r = n
    return len(rolls) - len(r)


if __name__ == '__main__':
    setday(4)

    grid, inverse, unique = parsegrid()
    rolls = set(inverse['@'])

    print('part1:', p1())
    print('part2:', p2())
