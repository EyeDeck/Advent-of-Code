import re
import sys
from collections import defaultdict


def write_line(b, line):
    x1, y1, x2, y2 = line
    # stepx = -min(max(x1 - x2, -1), 1)  # this works too
    # stepy = -min(max(y1 - y2, -1), 1)
    stepx = 0 if x1 == x2 else 1 if x1 < x2 else -1
    stepy = 0 if y1 == y2 else 1 if y1 < y2 else -1
    length = max(abs(x1 - x2), abs(y1 - y2)) + 1
    for i in range(length):
        nx = x1 + (i * stepx)
        ny = y1 + (i * stepy)
        b[nx, ny] += 1


def p1():
    for line in data:
        x1, y1, x2, y2 = line
        if x1 != x2 and y1 != y2:
            continue
        write_line(board, line)
    return calcall()


def p2():
    for line in data:
        x1, y1, x2, y2 = line
        if x1 == x2 or y1 == y2:
            continue
        write_line(board, line)
    return calcall()


def calcall():
    cum = 0
    for k, v in board.items():
        if v > 1:
            cum += 1
    return cum


day = 5
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    pat = re.compile("([\\d]+),([\\d]+) -> ([\\d]+),([\\d]+)")
    data = [[int(i) for i in re.findall(pat, line.strip())[0]] for line in file]
    board = defaultdict(int)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
