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
    def get_neighbors(node):
        neighbors = []
        for dir in DIRS:
            n = vadd(node, dir)
            if n not in grid and n[0] >= 0 and n[1] >= 0 and n[0] <= WIDTH and n[1] <= HEIGHT:
                neighbors.append((n, 1))
        return neighbors

    # grid = {tuple(c) for c in data[:1024]}
    grid = {tuple(c) for c in data[:12]}
    print_2d('.', {k: '#' for k in grid})

    # result = wbfs((0,0), (70,70), get_neighbors)
    result = wbfs((0,0), (6,6), get_neighbors)
    print(result)
    print_2d('.', {k:'#' for k in grid}, {k:'O' for k in result})

    return len(result)
# not 227 ?

def p2():
    def wbfs(src, tgt, edges):
        """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
        a list of `(node, cost)` pairs."""
        q = [(0, src, None)]

        parent = {}

        while q:
            cost, cur, prev = heapq.heappop(q)
            if cur in parent:
                continue
            parent[cur] = prev
            if cur == tgt:
                break

            for (n, ncost) in edges(cur, cost):
                if n in parent:
                    continue
                heapq.heappush(q, (cost + ncost, n, cur))

        if tgt not in parent:
            return None

        pos = tgt
        path = []
        while pos != src:
            path.append(pos)
            pos = parent[pos]
        path.append(src)
        path.reverse()
        return path

    grids = []
    for i in range(len(data)):
        grids.append({tuple(c) for c in data[:i]})
    print(grids)
    return None

def p2():
    def get_neighbors(node, grid):
        neighbors = []
        for dir in DIRS:
            n = vadd(node, dir)
            if n not in grid and n[0] >= 0 and n[1] >= 0 and n[0] <= WIDTH and n[1] <= HEIGHT:
                neighbors.append((n, 1))
        return neighbors

    for i in range(len(data)):
        grid = {tuple(c) for c in data[:i]}
        # grid = {tuple(c) for c in data[:12]}
        # print_2d('.', {k: '#' for k in grid})

        result = wbfs((0,0), (70,70), get_neighbors, grid)
        # result = wbfs((0,0), (6,6), get_neighbors)
        # print(result)
        # print_2d('.', {k:'#' for k in grid}, {k:'O' for k in result})
        if result == None:
            return data[:i][-1]

    # return len(result)


setday(18)

# data = parselines()
data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

# with open_default() as file:
#     data = get_ints(file.read())

verbose = '-v' in sys.argv or '--verbose' in sys.argv

WIDTH, HEIGHT = 70, 70
# WIDTH, HEIGHT = 6,6

print('part1:', p1() )
print('part2:', p2() )

# print('part1: %d\npart2: %d' % solve())
