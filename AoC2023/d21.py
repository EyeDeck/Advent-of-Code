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
    tiles = {unique['S']}
    for step in range(64):
        new_tiles = set()
        while tiles:
            tile = tiles.pop()
            for dir in DIRS:
                neighbor = vadd(tile, dir)
                if grid[neighbor] != '#':
                    new_tiles.add(neighbor)
        tiles = new_tiles
        # print_2d(' ', grid, {k:'@' for k in tiles})
        # print(len(tiles))
    return len(tiles)


# def p2():
#     _, _, w, h = grid_bounds(grid)
#     print(w,h)
#
#     tiles = {unique['S']}
#     for step in range(w + w + (26501365 % w)):
#         new_tiles = set()
#         while tiles:
#             tile = tiles.pop()
#             for dir in DIRS:
#                 neighbor = vadd(tile, dir)
#                 # print(neighbor, (neighbor[0] % w, neighbor[1] % h))
#                 if grid[(neighbor[0] % (w), neighbor[1] % (h))] != '#':
#                     new_tiles.add(neighbor)
#         tiles = new_tiles
#         full = len([c for c in grid.keys() if c in tiles])
#         print(full)
#
#     print_2d(' ', grid, {k:'@' for k in tiles}, constrain=(-1000, -1000, 1000, 1000))
#     print(w + (26501365 % w))
#     print(len(tiles))
#
#     return None


setday(21)

grid, inverse, unique = parsegrid()

print('part1:', p1() )
# print('part2:', p2() )
