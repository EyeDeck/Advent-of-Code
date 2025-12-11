import networkx as nx

from aoc import *


@memo
def count_paths(G, src, tgt):
    if src == tgt:
        return 1
    count = 0

    for successor in G.successors(src):
        count += count_paths(G, successor, tgt)

    return count


if __name__ == '__main__':
    setday(11)

    data = parselines(str.split)
    G = nx.DiGraph()
    for line in data:
        s = line[0][:-1]
        for e in line[1:]:
            G.add_edge(s, e)

    print('part1:', count_paths(G, 'you', 'out'))
    print('part2:', count_paths(G, 'svr', 'fft') * count_paths(G, 'fft', 'dac') * count_paths(G,'dac', 'out'))
