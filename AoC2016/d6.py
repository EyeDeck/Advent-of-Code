from collections import *
from aoc import *


def solve(p2):
    frequencies = [defaultdict(int) for _ in data[0]]
    for line in data:
        for i, c in enumerate(line):
            frequencies[i][c] += 1
    return ''.join([sorted(f, key=f.get)[0 if p2 else -1] for f in frequencies])


day = 6
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {solve(False)}')
print(f'part2: {solve(True)}')
