import itertools
import sys
import re
# import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
from collections import *
from math import *
from pprint import pprint
import networkx
import networkx as nx

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
    G = nx.DiGraph()
    sources = []
    targets = []
    for coord, v in grid.items():
        if v == 0:
            sources.append(coord)
        elif v == 9:
            targets.append(coord)
        G.add_node(coord, value=v)
    for coord, v in grid.items():
        for dir in DIRS:
            neighbor = vadd(coord, dir)
            if neighbor not in grid:
                continue
            n_v = grid[neighbor]
            if n_v == v+1:
                G.add_edge(coord, neighbor)
    acc = 0
    for pair in itertools.product(sources, targets):
        acc += 1 if networkx.has_path(G, pair[0], pair[1]) else 0
    return acc


def p2():
    G = nx.DiGraph()
    sources = []
    targets = []
    for coord, v in grid.items():
        if v == 0:
            sources.append(coord)
        elif v == 9:
            targets.append(coord)
        G.add_node(coord, value=v)
    for coord, v in grid.items():
        for dir in DIRS:
            neighbor = vadd(coord, dir)
            if neighbor not in grid:
                continue
            n_v = grid[neighbor]
            if n_v == v+1:
                G.add_edge(coord, neighbor)
    acc = 0
    for pair in itertools.product(sources, targets):
        for path in networkx.all_simple_paths(G, pair[0], pair[1]):
            acc += 1
    return acc


setday(10)

grid, inverse, unique = parsegrid()
for coord, v in grid.items():
    grid[coord] = int(v)

print('part1:', p1() )
print('part2:', p2() )
