import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
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
# print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
# print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):


def p1():
    for line in data:
        print(line)
    return None


def p2():
    return None


day = 0
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

# with open(f) as file:
#     data = [line.strip() for line in file]
data = heurparse(f)

print('part1:', p1() )
print('part2:', p2() )
