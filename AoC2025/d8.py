import networkx as nx

from aoc import *


def solve():
    dists = []
    for i, a in enumerate(data):
        for j, b in enumerate(data[i + 1:]):
            dists.append((math.dist(a, b), a, b))
    dists.sort()

    G = nx.Graph()
    G.add_nodes_from(data)
    for i, connection in enumerate(dists):
        if i == p1_pairs:  # part 1
            s_c = sorted(nx.connected_components(G), key=len, reverse=True)
            yield math.prod(len(x) for x in s_c[:3])

        dist, a, b = connection
        G.add_edge(a, b)

        if nx.is_connected(G):  # part 2
            yield a[0] * b[0]


if __name__ == '__main__':
    setday(8)

    data = parselines(lambda x: tuple(get_ints(x)))
    p1_pairs = 1000 if '-p' not in sys.argv else int(sys.argv[sys.argv.index('-p') + 1])

    solver = solve()
    print('part1:', next(solver))
    print('part2:', next(solver))
