import sys
from collections import defaultdict


def p1():
    found = []
    rtraverse(dirs, found, 100000)
    return sum(found)


def p2():
    if len(sys.argv) > 3:  # needed for bigboy input
        total_space = int(sys.argv[2])
        needed_space = int(sys.argv[3])
    else:
        total_space = 70000000
        needed_space = 30000000

    found = []
    rtraverse(dirs, found)
    free_space = total_space - max(found)
    return min([i for i in found if i >= needed_space - free_space])


def rtraverse(d, found, tgt=-1):
    acc = 0
    for k, v in d.items():
        if isinstance(v, int):
            acc += v
        else:
            acc += rtraverse(v, found, tgt)
    if tgt < 0 or acc <= tgt:
        found.append(acc)
    return acc


day = 7
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line for line in file.read().split('$') if line]


dirs = defaultdict(dict)
curr = []
for chunk in data:
    chunk = [[word for word in line.split()] for line in chunk.strip().split('\n')]

    if chunk[0][0] == 'cd':
        d = chunk[0][1]
        if d == '..':
            curr.pop()
        else:
            curr.append(d)
    else:
        access = dirs
        for level in curr:
            access = access[level]
        for line in chunk[1:]:
            if line[0] == 'dir':
                access[line[1]] = {}
            else:
                access[line[1]] = int(line[0])

print(f'part1: {p1()}')
print(f'part2: {p2()}')
