import itertools
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


def solve():
    h = []
    n = len(adj)
    for p in itertools.permutations(adj.keys()):
        cum = 0
        for i in range(0, n):
            l, m, r = p[(i-1) % n], p[i], p[(i+1) % n]
            cum += adj[m][l] + adj[m][r]
        h.append(cum)
    return max(h)


day = 13
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

adj = defaultdict(dict)
with open(f) as file:
    for line in file:
        sp = line.split()
        subject, object, diff = sp[0], sp[-1][:-1], int(sp[3]) * (1 if sp[2] == 'gain' else -1)
        adj[subject][object] = diff
# print(adj)

print(f'part1: {solve()}')
me = 'idek'
adj[me] = {}
for k in adj.keys():
    adj[k][me] = 0
    adj[me][k] = 0
# print(adj)

print(f'part2: {solve()}')
