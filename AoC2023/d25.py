import random
from aoc import *

import networkx as nx
from networkx.algorithms.connectivity import minimum_st_edge_cut

def p1():
    G = nx.Graph()

    for line in data:
        a, b = line.split(': ')
        for x in b.strip().split():
            G.add_node(a)
            G.add_node(x)
            G.add_edge(a, x)

    while True:
        a, b = random.choice([*G.nodes()]), random.choice([*G.nodes()])
        cuts = minimum_st_edge_cut(G, a, b)
        if len(cuts) > 3:
            continue
        for cut in cuts:
            G.remove_edge(*cut)

        return len(nx.node_connected_component(G, a)) * len(nx.node_connected_component(G, b))

    return None


setday(25)

data = parselines()

print('part1:', p1() )
