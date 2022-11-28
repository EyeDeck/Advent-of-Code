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
    ans = 0
    for i in range(len(data)-1):
        if data[i+1] > data[i]:
            ans += 1
    return ans


def p2():
    ans = 0
    for i in range(0, len(data)-3):
        # if data[i + 3] > data[i]: # this works too but I don't know why
        if sum(data[i+1:i+4]) > sum(data[i:i+3]):
            ans += 1
    return ans


f = 'd1.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [int(line.strip()) for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
