from collections import Counter
from aoc import *


def p1():
    return sum(abs(x - y) for x, y in zip(a, b))


def p2():
    rlist = Counter(b)
    return sum(n * rlist[n] for n in a)


setday(1)

data = parselines()
a, b = [], []
for line in data:
    x, y = [int(i) for i in line.split()]
    a.append(x)
    b.append(y)
a.sort()
b.sort()

print('part1:', p1() )
print('part2:', p2() )
