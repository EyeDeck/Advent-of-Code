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
    cubes = {}
    for line in data:
        state, coords = line
        state = 1 if state == 'on' else 0
        # rint(state, coords)
        if min(coords) < -50 or max(coords) > 50:
            continue
        for x in range(coords[0], coords[1]+1):
            for y in range(coords[2], coords[3]+1):
                for z in range(coords[4], coords[5]+1):
                    cubes[x,y,z] = state
        print('area:', get_cuboid_area(coords))
        print(coords,state,'=',sum([v for v in cubes.values() if v == 1]))

    return sum([v for v in cubes.values() if v == 1])


def get_cuboid_area(coords):
    return abs(coords[0]-(coords[1]+1)) * abs(coords[2]-(coords[3]+1)) * abs(coords[4]-(coords[5]+1))


def check_overlap(c1,c2):
    # ax1, ax2, ay1, ay2, az1, az2 = c1
    # bx1, bx2, by1, by2, bz1, bz2 = c1
    # if ax1
    #     pass
    pass


def get_overlap(a,b):
    # mn = max(a[0], b[0]), max(a[2],b[2],), max(a[4],b[4])
    # mx = min(a[1], b[1]), min(a[3],b[3],), min(a[3],b[3])
    # return (*mn, *mx)
    return max(a[0], b[0]), min(a[1], b[1]), max(a[2],b[2],), min(a[3],b[3],), max(a[4],b[4]), min(a[3],b[3])


def simplify_overlaps(ranges):
    for k,v in ranges.items():
        for k2,v2 in ranges.items():
            if k == k2:
                continue
            print(f'overlap of {k}, {k2} = {get_overlap(k,k2)}')

    return ranges

def p2():
    ranges = {}
    for line in data:
        state, coords = line
        state = 1 if state == 'on' else 0
        coords = sorted(coords[0:2]), sorted(coords[2:4]), sorted(coords[4:6])
        coords = [item for sublist in coords for item in sublist]
        ranges[tuple(coords)] = state
        ranges = simplify_overlaps(ranges)
    for k,v in ranges.items():
        print(k,v)
    # print(ranges)



day = 22
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

exp = re.compile('([-\d]+)')
with open(f) as file:
    data = [(line.split(' ')[0], [int(i) for i in re.findall(exp, line)]) for line in file]

# print(f'part1: {p1()}')
print(f'part2: {p2()}')
