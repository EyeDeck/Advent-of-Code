import sys
import re
# import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
from collections import *
from math import *
from pprint import pprint

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
    def get_dist(a, b):
        return math.sqrt(sum(abs(i)**2 for i in vsub(a, b)))

    dists = []

    for i, a in enumerate(data):
        for j, b in enumerate(data[i+1:]):
            dists.append((get_dist(a,b), a, b))

    dists.sort()

    G = nx.Graph()

    for connection in dists[:1000]:
        G.add_edge(connection[1], connection[2], weight=connection[0])

    # print(G)

    sorted_connected = sorted(nx.connected_components(G), key=len, reverse=True)
    # for cmp in sorted_connected:
    #     print(cmp)

    print([len(x) for x in sorted_connected])
    # print(len(dists))
    return len(sorted_connected[0]) * len(sorted_connected[1]) * len(sorted_connected[2])


def p2():
    def get_dist(a, b):
        return math.sqrt(sum(abs(i)**2 for i in vsub(a, b)))

    dists = []

    for i, a in enumerate(data):
        for j, b in enumerate(data[i+1:]):
            dists.append((get_dist(a,b), a, b))

    dists.sort()

    G = nx.Graph()

    G.add_nodes_from(data)
    for connection in dists:
        G.add_edge(connection[1], connection[2], weight=connection[0])
        if nx.is_connected(G):
            return connection[1][0] * connection[2][0]

    # print(G)

    sorted_connected = sorted(nx.connected_components(G), key=len, reverse=True)
    # for cmp in sorted_connected:
    #     print(cmp)

    print([len(x) for x in sorted_connected])
    # print(len(dists))
    return len(sorted_connected[0]) * len(sorted_connected[1]) * len(sorted_connected[2])


if __name__ == '__main__':
    setday(8)

    data = parselines(lambda x: tuple(get_ints(x)))
    # data = parselines(get_ints)
    # grid, inverse, unique = parsegrid()

    # with open_default() as file:
    #     data = get_ints(file.read())

    print('part1:', p1() )
    print('part2:', p2() )

    # print('part1: %d\npart2: %d' % solve())
