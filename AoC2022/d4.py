import sys
from operator import itemgetter


def solve():
    p1, p2 = 0, 0
    for line in data:
        line = sorted(line, key=itemgetter(1), reverse=True)
        line = sorted(line, key=itemgetter(0))

        if line[0][1] >= line[1][1]:
            p1 += 1

        if line[1][0] <= line[0][1]:
            p2 += 1
    return p1, p2


day = 4
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[[int(i) for i in r.split('-')] for r in line.strip().split(',')] for line in file]

print(f'part1: %s\npart2: %s' % solve())
