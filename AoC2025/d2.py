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
    acc = 0
    for i_range in data.split(','):
        a, b = (int(i) for i in i_range.split('-'))
        for i in range(a, b + 1):
            i_s = str(i)
            m = len(i_s) // 2
            if i_s[:m] == i_s[m:]:
                acc += i
    return acc


def p2():
    def is_invalid(i):
        i_s = str(i)
        ln = len(i_s)
        for d in range(2, ln + 1):
            # print(d)
            if ln % d != 0:
                continue

            interval = len(i_s) // d
            base = i_s[:interval]
            # print(f'{i_s}, ln={ln}, base={base}, interval={interval}, divisor={d}')
            for offset in range(interval, ln, interval):
                # print(offset, i_s[offset:offset + interval], '==', base)
                # input()
                if i_s[offset:offset + interval] != base:
                    break
            else:
                # print('passed = invalid')
                return True
        return False

    acc = 0
    for i_range in data.split(','):
        a, b = (int(i) for i in i_range.split('-'))
        for i in range(a, b + 1):
            if is_invalid(i):
                acc += i
    return acc


if __name__ == '__main__':
    setday(2)

    data = parselines()[0]
    # data = parselines(get_ints)
    # grid, inverse, unique = parsegrid()

    # with open_default() as file:
    #     data = get_ints(file.read())

    print('part1:', p1())
    print('part2:', p2())

    # print('part1: %d\npart2: %d' % solve())
