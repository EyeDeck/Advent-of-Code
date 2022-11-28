import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
from aoc import *


def p1():
    earliest = int(data[0])
    db = [int(x) for x in data[1].split(',') if x != 'x']
    # print(db)
    nxt = {}
    for bus in db:
        next_time = (earliest // bus) * bus + bus
        # print(bus, next_time)
        nxt[bus] = next_time - earliest
    # print(nxt)
    mn = min(nxt.items(), key=lambda x: x[1])
    return mn[0] * mn[1]


def p2():
    """FUCK this problem and fuck number theory"""
    db = {i:int(x) for i, x in enumerate(data[1].split(',')) if x != 'x'}
    print(db)
    base = 0
    cum = 1
    for offset, bus in db.items():
        while (base+offset) % bus != 0:
            base += cum
        cum *= bus
        print(base, cum, offset)
    return base


f = 'dx.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]


print(f'part1: {p1()}')
print(f'part2: {p2()}')
