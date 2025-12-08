import networkx as nx

from aoc import *


def solve():
    def get_dist(a, b):
        return sum(abs(i) ** 2 for i in vsub(a, b))

    dists = []
    for i, a in enumerate(data):
        for j, b in enumerate(data[i + 1:]):
            dists.append((get_dist(a, b), a, b))
    dists.sort()

    G = nx.Graph()
    G.add_nodes_from(data)
    for i, connection in enumerate(dists):
        dist, a, b = connection
        G.add_edge(a, b)
        if i == 1000:
            s_c = sorted(nx.connected_components(G), key=len, reverse=True)
            yield math.prod(len(x) for x in s_c[:3])
        if nx.is_connected(G):
            yield a[0] * b[0]


if __name__ == '__main__':
    setday(8)

    data = parselines(lambda x: tuple(get_ints(x)))

    solver = solve()
    print('part1:', next(solver))
    print('part2:', next(solver))
