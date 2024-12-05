import functools

from aoc import *


def compare(a, b):
    if a in rules_before[b]:
        return -1
    elif a in rules_after[b]:
        return 1
    else:
        return 0


def solve():
    acc_p1 = 0
    acc_p2 = 0
    for pageset in pagesets_raw:
        sorted_pageset = sorted(pageset, key=functools.cmp_to_key(compare))
        middle = sorted_pageset[len(sorted_pageset) // 2]

        if sorted_pageset == pageset:
            acc_p1 += middle
        else:
            acc_p2 += middle

    return acc_p1, acc_p2


setday(5)

with open_default() as file:
    rules_raw, pagesets_raw = file.read().split('\n\n')

pagesets_raw = [[int(i) for i in line.split(',')] for line in pagesets_raw.strip().split('\n')]
rules_raw = [[int(i) for i in line.split('|')] for line in rules_raw.strip().split('\n')]

rules_before = defaultdict(set)
rules_after = defaultdict(set)
for rule in rules_raw:
    rules_before[rule[1]].add(rule[0])
    rules_after[rule[0]].add(rule[1])

print('part1: %d\npart2: %d' % solve())
