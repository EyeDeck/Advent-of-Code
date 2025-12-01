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
    for line in data:
        print(line)
    return None


def p2():
    return None


setday(0)

data = parselines()
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

# with open_default() as file:
#     data = get_ints(file.read())

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2() )

# print('part1: %d\npart2: %d' % solve())
