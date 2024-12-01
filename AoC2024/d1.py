import sys
import re
# import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
from collections import *
from math import *
from pprint import pprint

from aoc import *


# print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
# print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):
# INF = sys.maxsize
# @memo
# splat(f)
# bfs(src, tgt, {n1: [n2, n3, n4]})
# wbfs(src, tgt, edge_func)
# astar(src, tgt, edge_func, heur_func)
# ccs(srcs, neigh_func, filt_func?)
# Dedup().seen(x)


def p1():
    a, b = [], []
    for line in data:
        x, y = [int(i) for i in line.split()]
        a.append(x)
        b.append(y)
    a.sort()
    b.sort()
    acc = 0
    for x,y in zip(a,b):
        acc += abs(x-y)
    return acc


def p2():
    a, b = [], []
    for line in data:
        x, y = [int(i) for i in line.split()]
        a.append(x)
        b.append(y)
    rlist = Counter(b)
    acc = 0
    for n in a:
        acc += n * rlist[n]
    return acc


setday(1)

data = parselines()
# parsed = [[int(i) for i in line.split()] for line in data]
# print(parsed)
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
