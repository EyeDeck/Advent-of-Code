import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)


def p1():
    x, y = 0, 0
    visited = {(0, 0)}
    for c in data:
        if c == '>':
            x += 1
        elif c == '^':
            y -= 1
        elif c == '<':
            x -= 1
        elif c == 'v':
            y += 1
        visited.add((x, y))
    return len(visited)


def p2():
    coords = [0, 0, 0, 0]
    visited = {(0, 0)}
    for i, c in enumerate(data):
        if c == '>':
            coords[0 + (i & 1)] += 1
        elif c == '^':
            coords[2 + (i & 1)] += 1
        elif c == '<':
            coords[0 + (i & 1)] -= 1
        elif c == 'v':
            coords[2 + (i & 1)] -= 1

        # if (i&1):
        #     print('ROBO', c, (coords[0 + (i & 1)], coords[2 + (i & 1)]))
        # else:
        #     print('SANAT', c, (coords[0 + (i & 1)], coords[2 + (i & 1)]))
        visited.add((coords[0 + (i & 1)], coords[2 + (i & 1)]))
        # print(visited)
    return len(visited)


f = 'd3.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read()

print(f'part1: {p1()}')
print(f'part2: {p2()}')
