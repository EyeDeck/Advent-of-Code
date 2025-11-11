import collections

from ec import *


def p1():
    return sum(set(parse_lines(1, get_ints)[0]))


def p2():
    return sum(sorted(list(set(parse_lines(2, get_ints)[0])))[:20])


def p3():
    return max(collections.Counter(parse_lines(3, get_ints)[0]).values())


setquest(3)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
