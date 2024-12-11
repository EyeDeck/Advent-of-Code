import networkx as nx

from aoc import *


def solve():
    G = nx.DiGraph()
    sources = set()
    targets = set()
    for coord, v in grid.items():
        if v == 0:
            sources.add(coord)
        elif v == 9:
            targets.add(coord)
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
    for i, source in enumerate(sources):
        print(f'calculating ({i}/{len(sources)}...', end='\r')
        reachable = set(nx.descendants(G, source)) & targets
        p1_acc += len(reachable)
        for target in reachable:
            for _ in nx.all_simple_paths(G, source, target):
                p2_acc += 1
    sys.stdout.write('\x1b[2K')  # ANSI erase line

    return p1_acc, p2_acc


setday(10)

grid, inverse, unique = parsegrid()
for coord, v in grid.items():
    grid[coord] = int(v)

print('part1: %d\npart2: %d' % solve())
