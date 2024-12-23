import networkx as nx
from aoc import *


def solve():
    G = nx.Graph()
    for line in data:
        a, b = line.split('-')
        G.add_edge(a, b)

    cliques = [c for c in nx.enumerate_all_cliques(G)]

    return \
        len(list(c for c in cliques if len(c) == 3 and any(node[0] == 't' for node in c))), \
        ','.join(sorted(max(cliques, key=len)))


setday(23)

data = parselines()

print('part1: %d\npart2: %s' % solve())

