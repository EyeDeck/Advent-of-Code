import itertools
import sys
import math
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)


def p1():
    total = 0
    for line in data:
        total += sum(math.prod(x) for x in itertools.combinations(line, 2))*2 + math.prod(sorted(line)[:2])
    return total


def p2():
    total = 0
    for line in data:
        total += sum(sorted(line)[:2]) * 2 + math.prod(line)
    return total


f = 'd2.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(x) for x in line.split('x')] for line in file]



print(f'part1: {p1()}')
print(f'part2: {p2()}')
