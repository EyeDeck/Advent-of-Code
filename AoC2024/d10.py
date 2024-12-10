import itertools
import networkx as nx

from aoc import *


def solve():
    G = nx.DiGraph()
    sources = []
    targets = []
    for coord, v in grid.items():
        if v == 0:
            sources.append(coord)
        elif v == 9:
            targets.append(coord)
        G.add_node(coord)

        for dir in DIRS:
            neighbor = vadd(coord, dir)
            if neighbor not in grid:
                continue
            n_v = grid[neighbor]
            if n_v == v + 1:
                G.add_edge(coord, neighbor)

    p1_acc = 0
    p2_acc = 0
    for pair in itertools.product(sources, targets):
        if nx.has_path(G, pair[0], pair[1]):
            p1_acc += 1
            for _ in nx.all_simple_paths(G, pair[0], pair[1]):
                p2_acc += 1

    return p1_acc, p2_acc


setday(10)

grid, inverse, unique = parsegrid()
for coord, v in grid.items():
    grid[coord] = int(v)

print('part1: %d\npart2: %d' % solve())
