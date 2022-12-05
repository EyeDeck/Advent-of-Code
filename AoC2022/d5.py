import copy
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
    c = copy.deepcopy(crates)
    for line in moves_raw.split('\n'):
        m, f, t = [int(i) for i in re.findall(r'(\d+)', line)]
        print(m, f, t)
        print(line)
        for _ in range(m):
            c[t-1].append(c[f-1].pop())
    return ''.join([l.pop() for l in c])


def p2():
    c = copy.deepcopy(crates)
    for line in moves_raw.split('\n'):
        m, f, t = [int(i) for i in re.findall(r'(\d+)', line)]
        print(m, f, t)
        print(line)
        c[t - 1].extend(c[f - 1][-m:])
        c[f-1] = c[f - 1][:-m]
    return ''.join([l.pop() for l in c])


day = 5
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    crates_raw, moves_raw = file.read().split('\n\n')
#
# crates_raw = crates_raw.replace('[', ' ')
# crates_raw = crates_raw.replace(']', ' ')
#
# crates = {}
# for y, line in enumerate(crates_raw.split('\n')):
#     for x, char in enumerate(line):
#         if char != ' ' and not char.isdigit():
#             crates[rotate_point_around_origin(x//4,y, 0, 0, 270)] = char
#
# bounds = min(crates, key=itemgetter(0))[0], min(crates, key=itemgetter(1))[1], \
#          max(crates, key=itemgetter(0))[0], max(crates, key=itemgetter(1))[1]
# print(bounds)

# crates = {}
# l = 0
# for (x,y), char:
#     if char != ' ':
#
#     print(x,y, char)

# print_2d(' ', crates, constrain=(0,0,100,100))
# print(crates)
# print(crates_raw, moves_raw)

crates = '''MJCBFRLH
ZCD
HJFCNGW
PJDMTSB
NCDRJ
WLDQPJGZ
PZTFRH
LVMG
CBGPFQRJ'''

# crates = '''ZN
# MCD
# P'''
#
# moves_raw = '''move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2'''

crates = [[c for c in line] for line in crates.split('\n')]
print(crates)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
