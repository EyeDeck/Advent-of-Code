import sys
from collections import *



day = 6
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [int(i) for i in file.read().strip().split(',')]
    bins = defaultdict(int)
    for v in data:
        bins[v] += 1

print(f'part1: {solve_n(bins, 80)}')
print(f'part2: {solve_n(bins, 256)}')
print(f'6969: {solve_n(bins, 6969)}')
print(f'9999999: {solve_n(bins, 9999999)}')
