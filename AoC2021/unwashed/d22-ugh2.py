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
        if min(coords) < -50 or max(coords) > 50:
            continue
        for x in range(coords[0], coords[1] + 1):
            for y in range(coords[2], coords[3] + 1):
                for z in range(coords[4], coords[5] + 1):
                    cubes[x, y, z] = state
        print('area:', get_cuboid_area(coords))
        print(coords, state, '=', sum([v for v in cubes.values() if v == 1]))

    return sum([v for v in cubes.values() if v == 1])


def get_cuboid_area(coords):
    return abs(coords[0] - (coords[1] + 1)) * abs(coords[2] - (coords[3] + 1)) * abs(coords[4] - (coords[5] + 1))


def check_overlap(a, b):
    (amx, amy, amz), (aMx, aMy, aMz) = a
    (bmx, bmy, bmz), (bMx, bMy, bMz) = b
    return amx <= bMx and aMx >= bmx \
       and amy <= bMy and aMy >= bmy \
       and amz <= bMz and aMz >= bmz


def get_overlap(a, b):
    mn = max(a[0][0], b[0][0]), max(a[0][1], b[0][1]), max(a[0][2], b[0][2])
    mx = min(a[1][0], b[1][0]), min(a[1][1], b[1][1]), min(a[1][2], b[1][2])
    return mn, mx


# def split_big_cuboid_from_small_cuboid(a, b):
#     (amx, amy, amz), (aMx, aMy, aMz) = a
#     (bmx, bmy, bmz), (bMx, bMy, bMz) = b
#
#     # amx to bmx
#     # bMx to aMx
#
#     xB = [amx, bmx, bMx, aMx]
#     yB = [amy, bmy, bMy, aMy]
#     zB = [amz, bmz, bMz, aMz]
#
#     n = set()
#     for x in range(3):
#         for y in range(3):
#             for z in range(3):
#                 nA = (xB[x], yB[y], zB[z])
#                 nB = (xB[x+1]-1, yB[y+1]-1, zB[z+1]-1)
#                 n.add((nA, nB))
#     return n


def insert_cuboid(cuboids, cuboid):
    new_cuboids = set()
    for existing in cuboids:
        if check_overlap(existing, cuboid):

            split_cuboids = split_big_cuboid_from_small_cuboid
        else:
            new_cuboids.add(existing)


        print(f'{existing} and {cuboid} overlap? {check_overlap(existing, cuboid)}, bb: {get_overlap(existing, cuboid)}')


def p2():
    ranges = set()
    for line in data:
        state, coords = line
        state = 1 if state == 'on' else 0
        xs, ys, zs = sorted(coords[0:2]), sorted(coords[2:4]), sorted(coords[4:6])
        coords = ((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs)))
        insert_cuboid(ranges, coords)
        ranges.add(coords)
        # ranges = simplify_overlaps(ranges)
    # for k,v in ranges.items():
    #     print(k,v)
    for k in ranges:
        print(k)
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
