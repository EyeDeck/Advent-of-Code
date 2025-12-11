import networkx as nx

from aoc import *


def p1():
    G = nx.DiGraph()
    for line in data:
        s = line[0][:-1]
        for e in line[1:]:
            G.add_edge(s, e)
    return len(list(nx.all_simple_paths(G, 'you', 'out')))


def p2():
    G = nx.DiGraph()
    for line in data:
        s = line[0][:-1]
        for e in line[1:]:
            G.add_edge(s, e)

    @memo
    def count_paths(src, tgt):
        if src == tgt:
            return 1
        count = 0

        for successsor in G.successors(src):
            count += count_paths(successsor, tgt)

        return count

    # nx.draw(G)
    # matplotlib.pyplot.show()

    a = count_paths('svr', 'fft')
    b = count_paths('fft', 'dac')
    c = count_paths('dac', 'out')


    # print(next(nx.all_simple_paths(G, 'svr', 'out')))
    # die()
    # a = len(list(nx.all_simple_paths(G, 'svr', 'fft')))
    # print(a)
    # b = len(list(nx.all_simple_paths(G, 'fft', 'dac')))
    # print(b)
    # c = len(list(nx.all_simple_paths(G, 'dac', 'out')))
    # print(c)

    return a * b * c


if __name__ == '__main__':
    setday(11)

    data = parselines(str.split)

    print('part1:', p1() )
    print('part2:', p2() )
