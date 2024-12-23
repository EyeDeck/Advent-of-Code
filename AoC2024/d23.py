import itertools
import networkx as nx

from aoc import *


def solve():
    G = nx.Graph()
    for line in data:
        a, b = line.split('-')
        G.add_edge(a, b)

    sets = set()
    for node in G.nodes():
        if node[0] != 't':
            continue
        neighbors = [n for n in G.neighbors(node)]
        sets |= {frozenset([node, a, b]) for a, b in itertools.combinations(neighbors, 2)}

    interconnected = set()
    for s in sets:
        a, b, c = s
        if G.has_edge(a, b) and G.has_edge(b, c) and G.has_edge(a, c):
            interconnected.add(s)

    yield len(interconnected)

    yield ','.join(sorted(sorted(list(nx.find_cliques(G)), key=len, reverse=True)[0]))


setday(23)

data = parselines()

gen = solve()
print('part1:', next(gen))
print('part2:', next(gen))
