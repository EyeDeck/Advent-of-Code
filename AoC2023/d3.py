import math
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
    def has_symbol():
        for x in range(bb[0][0], bb[1][0]):
            for y in range(bb[0][1], bb[1][1] + 1):
                if (x,y) not in grid:
                    continue
                adj = grid[(x,y)]
                if adj != '.' and not adj.isnumeric():
                    # print('asd')
                    return True
        return False

    acc = 0
    for k,v in grid.items():
        if v == '.':
            continue

        to_left = vadd(k, (-1,0))
        if v.isnumeric() and (to_left in grid and not grid[to_left].isnumeric()) or (to_left not in grid):
            coord = k
            num_str = ''
            while coord in grid and grid[coord].isnumeric():
                num_str += grid[coord]
                coord = vadd(coord, (1,0))
            bb = (vadd(k, (-1,-1)), vadd(coord, (1,1)))
            # print(num_str, bb)

            if has_symbol():
                # print(num_str)
                acc += int(num_str)
            # else:
            #     print('not', num_str)

    return acc
# not 548609


def p2():
    acc = 0
    for k,v in grid.items():
        if v != '*':
            continue
        numeric = {}
        # print(k,v)
        bb = (vadd(k, (-1,-1)), vadd(k, (1,1)))
        for x in range(bb[0][0], bb[1][0] + 1):
            for y in range(bb[0][1], bb[1][1] + 1):
                if (x,y) in grid and grid[x,y].isnumeric():
                    numeric[(x,y)] = grid[x,y]

        seen = set()
        adj_numbers = []
        for k,v in numeric.items():
            if k in seen:
                continue
            while k in grid and grid[k].isnumeric():
                k = vadd(k, (-1,0))
            # print('left = ', k)

            num_str = ''
            k = vadd(k, (1, 0))
            while k in grid and grid[k].isnumeric():
                seen.add(k)
                num_str += grid[k]
                k = vadd(k, (1,0))
                # print('at', k, num_str)

            adj_numbers.append(int(num_str))
        # print(adj_numbers)
            # # print(coord)
            # while coord in grid and grid[coord].isnumeric():
            #     # print(coord)
            #     numeric_lr[coord] = grid[coord]
            #     coord = vadd(coord, (1,0))
            #
            # coord = k

        if len(adj_numbers) == 2:
            # print(adj_numbers)
            acc += math.prod(adj_numbers)



        # print(numeric_lr)

    return acc


setday(3)

data = parselines()
# data = parselines(get_ints)
grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
