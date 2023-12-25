import math

from aoc import *
import networkx as nx

def p1():
    G = nx.Graph()

    for line in data:
        a, b = line.split(': ')
        for c in b.strip().split():
            G.add_edge(a, c)

    for cut in nx.minimum_edge_cut(G):
        G.remove_edge(*cut)

    return math.prod(len(c) for c in nx.connected_components(G))

setday(25)

data = parselines()

print('part1:', p1() )
