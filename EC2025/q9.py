import itertools
from collections import defaultdict

import networkx as nx

from ec import *


def check_parent(a, b, c):
    # parent a and b, child c
    for (x, y), z in zip(zip(a, b), c):
        # print(x, y, z)
        if z not in (x, y):
            return False
    return True


def p1():
    data = {k: v for k, v in parse_lines(1, lambda x: x.split(':'))}

    for perm in itertools.permutations(data.values(), 3):
        if check_parent(*perm):
            a_sum = sum(1 for x in zip(perm[0], perm[2]) if x[0] == x[1])
            b_sum = sum(1 for x in zip(perm[1], perm[2]) if x[0] == x[1])
            return a_sum * b_sum


def p2():
    data = {k: v for k, v in parse_lines(2, lambda x: x.split(':'))}

    known_parents = defaultdict(set)
    for perm in itertools.permutations(data.items(), 3):
        a,b,c = perm
        if check_parent(a[1], b[1], c[1]):
            known_parents[c[0]].add(a[0])
            known_parents[c[0]].add(b[0])
    # print(known_parents)

    acc = 0
    for child, parents in known_parents.items():
        parents = list(parents)
        a_sum = sum(1 for x in zip(data[child], data[parents[0]]) if x[0] == x[1])
        b_sum = sum(1 for x in zip(data[child], data[parents[1]]) if x[0] == x[1])
        acc += a_sum * b_sum
    # if check_parent(*perm):

    return acc


def p3():
    data = {k: v for k, v in parse_lines(3, lambda x: x.split(':'))}

    known_parents = defaultdict(set)
    for perm in itertools.permutations(data.items(), 3):
        a,b,c = perm
        if check_parent(a[1], b[1], c[1]):
            known_parents[c[0]].add(a[0])
            known_parents[c[0]].add(b[0])
    print(known_parents)

    G = nx.Graph()
    G.add_nodes_from(known_parents.keys())
    for child, parents in known_parents.items():
        for parent in parents:
            G.add_edge(child, parent)
            print('added edge', child, parent)

    largest_connected = sorted(nx.connected_components(G), key=len)[-1]

    return sum(int(i) for i in largest_connected)


setquest(9)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
