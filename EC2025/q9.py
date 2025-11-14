import itertools
import math
from collections import defaultdict

import networkx as nx

from ec import *


def read_input(n):
    return {k: v for k, v in parse_lines(n, lambda x: x.split(':'))}


def validate_child(parent_a, parent_b, child):
    for (x, y), z in zip(zip(parent_a, parent_b), child):
        if z not in (x, y):
            return False
    return True


def get_parents(data):
    known_parents = defaultdict(set)
    for (parent_id_a, parent_genes_a), (parent_id_b, parent_genes_b) in itertools.combinations(data.items(), 2):
        for child_id, child_genes in data.items():
            if child_id == parent_id_a or child_id == parent_id_b:
                continue
            if validate_child(parent_genes_a, parent_genes_b, child_genes):
                known_parents[child_id].add(parent_id_a)
                known_parents[child_id].add(parent_id_b)
    return known_parents


def calc_similarity(parents, child):
    return math.prod(sum(1 for x in zip(parent, child) if x[0] == x[1]) for parent in parents)


def p1():
    data = read_input(1)

    known_parents = get_parents(data)
    child, (parents) = known_parents.popitem()

    return calc_similarity((data[p] for p in parents), data[child])


def p2():
    data = read_input(2)

    known_parents = get_parents(data)

    acc = 0
    for child, parents in known_parents.items():
        acc += calc_similarity((data[p] for p in parents), data[child])

    return acc


def p3():
    data = read_input(3)

    known_parents = get_parents(data)

    G = nx.Graph()
    for child, parents in known_parents.items():
        for parent in parents:
            G.add_edge(child, parent)

    largest_connected = sorted(nx.connected_components(G), key=len)[-1]

    return sum(int(i) for i in largest_connected)


setquest(9)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
