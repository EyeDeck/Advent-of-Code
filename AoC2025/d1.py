import sys
import re
# import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
from collections import *
from math import *
from pprint import pprint

from aoc import *


# print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
# print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):
# INF = sys.maxsize
# @memo
# splat(f)
# bfs(src, tgt, {n1: [n2, n3, n4]})
# wbfs(src, tgt, edge_func)
# astar(src, tgt, edge_func, heur_func)
# ccs(srcs, neigh_func, filt_func?)
# Dedup().seen(x)


def p1():
    p = 50
    acc = 0
    for line in data:
        if line[0] == 'R':
            o = int(line[1:])
        else:
            o = -int(line[1:])
        p = ((p + o) % 100)

        if p == 0:
            acc += 1
    return acc


def p2():
    p = 50
    acc = 0
    for line in data:
        if line[0] == 'R':
            o = int(line[1:])
        else:
            o = -int(line[1:])
        prev = p
        p += o
        # if p < 0 or p >= 100:
        #     passes = abs(p // 100)
        #     acc += passes
        #     print(f'    yes ({passes})')

        passes = abs(p // 100)
        acc += passes
        print(f'{prev} -> {p} ({p%100}) = {passes}')

        p %= 100

        print(line, o)
    return acc


def p2():
    p = 50
    acc = 0
    for line in data:
        o = int(line[1:])
        if line[0] == 'R':
            for _ in range(o):
                p += 1
                p %= 100
                if p == 0:
                    acc += 1
                # print('\t', p)
        else:
            for _ in range(o):
                p -= 1
                p %= 100
                if p == 0:
                    acc += 1
                # print('\t', p)
        # print(p)
    return acc


if __name__ == '__main__':
    setday(1)

    data = parselines()
    # data = parselines(get_ints)
    # grid, inverse, unique = parsegrid()

    # with open_default() as file:
    #     data = get_ints(file.read())

    verbose = '-v' in sys.argv or '--verbose' in sys.argv

    print('part1:', p1())
    print('part2:', p2())

    # print('part1: %d\npart2: %d' % solve())
