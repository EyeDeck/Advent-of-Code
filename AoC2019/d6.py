import sys
from collections import defaultdict


def count_orbits(key):
    ct = 0
    for o in orbits[key]:
        ct += 1
        if o in orbits:
            ct += count_orbits(o)
    return ct


def bfs(nodes, visited, end, depth=-1):
    visited.update(nodes)
    new = set()
    for n in nodes:
        new.update(set(orbiters[n]))
        new.update(set(orbits[n]))
    new.difference_update(visited)
    nodes = new
    # print(neighbors)
    if end in nodes:
        return depth
    else:
        return bfs(nodes, visited, end, depth + 1)


f = 'd6.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [i.strip().split(')') for i in open(f).readlines()]

orbits = defaultdict(set)
orbiters = defaultdict(set)
total = 0
for orbit in inp:
    orbits[orbit[0]].add(orbit[1])
    orbiters[orbit[1]].add(orbit[0])
    total += 1

p1 = 0
for orbit in orbits:
    p1 += count_orbits(orbit)

p2 = bfs({'YOU'}, set(), 'SAN')

print('p1: {}\np2: {}'.format(p1, p2))
