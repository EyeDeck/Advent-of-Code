import networkx as nx

from aoc import *


def solve():
    G = nx.Graph()
    for line in data:
        for tgt in line[1:]:
            G.add_edge(line[0], tgt)
    c = list(nx.connected_components(G))
    return next(len(x) for x in c if 0 in x), len(c)


setday(12)

data = parselines(get_ints)

print('part1: %d\npart2: %d' % solve())
