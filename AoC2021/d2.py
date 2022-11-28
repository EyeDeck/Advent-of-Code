import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
# from blist import blist
from collections import *
from math import *
from pprint import pprint

from aoc import *
# INF = 999999999
# mkmat(sx, sy, val=0)
# fw(m)
# get0()
# get1(cvt=str)
# get2(cvt=str)
# @memo
# splat(f)
# bfs(src, tgt, {n1: [n2, n3, n4]})
# wbfs(src, tgt, edge_func)
# astar(src, tgt, edge_func, heur_func)
# ccs(srcs, neigh_func, filt_func?)
# Dedup().seen(x)
# mkcls('Name', f1=v1, f2=v2, ...)


def p1():
    x, y = 0, 0
    for line in data:
        d, amt = line.split()
        amt = int(amt)
        if d == 'forward':
            x += amt
        elif d == 'down':
            y += amt
        elif d == 'up':
            y -= amt
    return x * y


def p2():
    x, y, aim = 0, 0, 0
    for line in data:
        d, amt = line.split()
        amt = int(amt)
        if d == 'forward':
            x += amt
            y += aim * amt
        elif d == 'down':
            aim += amt
        elif d == 'up':
            aim -= amt
    return x * y


day = 2
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
