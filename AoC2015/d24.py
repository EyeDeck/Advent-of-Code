import math
from aoc import *


def solve(groupct):
    total = sum(data)
    target = total // groupct

    found = [len(data), []]
    rsearch(set(), 0, found, target)

    min_qe = sys.maxsize
    for v in found[1]:
        p = math.prod(v)
        if p < min_qe:
            min_qe = p

    return min_qe


def rsearch(cur, index, valid, target):
    sm = sum(cur)
    for i, n in enumerate(data[index:]):

        # skips a ton of unnecessary computation
        if len(cur) >= valid[0]:
            continue

        smn = sm+n
        if smn <= target:
            nxt = cur.copy()
            nxt.add(n)
            if smn == target:
                ln = len(nxt)
                if ln < valid[0]:
                    valid[0] = ln
                    valid[1] = []
                if ln == valid[0]:
                    valid[1].append(nxt)
            else:
                rsearch(nxt, index+i+1, valid, target)


day = 24
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [int(line.strip()) for line in file]
    print(data)

print(f'part1: {solve(3)}')
print(f'part2: {solve(4)}')
