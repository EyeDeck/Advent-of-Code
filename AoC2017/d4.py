from collections import *

from aoc import *


def p1():
    return sum(len(line) == len(set(line)) for line in data)


def p2():
    acc = 0
    for line in data:
        counters = [frozenset((k,v) for k,v in Counter(word).items()) for word in line]
        if len(counters) == len(set(counters)):
            acc += 1
    return acc


setday(4)

data = parselines(lambda x:x.split())

print('part1:', p1() )
print('part2:', p2() )