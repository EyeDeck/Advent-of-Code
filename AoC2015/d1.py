import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)


def p1():
    ct = 0
    for c in data:
        if c == '(':
            ct += 1
        elif c == ')':
            ct -= 1
    return ct


def p2():
    ct = 0
    for i, c in enumerate(data):
        if c == '(':
            ct += 1
        elif c == ')':
            ct -= 1
        print(i, c, ct)
        if ct == -1:
            return i+1
    return ct


f = 'd1.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    # data = [line for line in file.readlines()]
    data = file.read()
    pass


print(f'part1: {p1()}')
print(f'part2: {p2()}')
