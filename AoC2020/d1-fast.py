from itertools import combinations
import sys


def p1(ints, target):
    inv_set = set()
    for i in ints:
        inv = target - i
        if i in inv_set:
            return i * inv
        inv_set.add(inv)


def p2(ints, target):
    inv_set = {target-i for i in ints}
    for t in combinations(ints, 2):
        s = sum(t)
        if s >= target:
            continue
        inv = target - s
        if s in inv_set:
            if len({t[0], t[1], inv}) != 3:
                continue
            return t[0] * t[1] * inv, (t[0], t[1], inv)


f = 'd1.txt'
tgt = 2020
if len(sys.argv) > 1:
    f = sys.argv[1]
    tgt = int(sys.argv[2])

with open(f) as file:
    data = {int(line) for line in file.readlines()}

print(f'part1: {p1(data, tgt)}')
print(f'part2: {p2(data, tgt)}')
