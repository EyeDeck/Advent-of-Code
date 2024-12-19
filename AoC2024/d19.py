from aoc import *


@memo
def count(pattern):
    if pattern == '':
        return 1

    # return sum(count(pattern[len(t):]) for t in towels if pattern.startswith(t))
    acc = 0
    for t in towels:
        if pattern.startswith(t):
            acc += count(pattern[len(t):])
    return acc


def solve():
    acc_p1 = 0
    acc_p2 = 0
    for pattern in patterns:
        s = count(pattern)
        if s:
            acc_p1 += 1
            acc_p2 += s
    return acc_p1, acc_p2


setday(19)

with open_default() as file:
    towels, patterns = file.read().strip().split('\n\n')
towels = set(towels.split(', '))
patterns = patterns.split('\n')

print('part1: %d\npart2: %d' % solve())
