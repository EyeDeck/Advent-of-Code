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


def firstnum(line, r):
    # for c in line if not r else reversed(line):
    #     if c.isdigit():
    #         return c
    rpl = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0}
    if r:
        i = len(line)-1
        while i >= 0:
            if line[i].isdigit():
                return line[i]
            for k, v in rpl.items():
                if line[i:i + len(k)] == k:
                    return str(v)
            i -= 1
    else:
        i = 0
        while i <= len(line):
            # print(line[i])
            if line[i].isdigit():
                return line[i]
            for k, v in rpl.items():
                if line[i:i + len(k)] == k:
                    print(line[i:i + len(k)], v)
                    return str(v)
            i += 1
    die()

def p1():
    acc = 0
    for line in data:
        acc += int(firstnum(line, False) + firstnum(line, True))
    return acc

def p2():
    acc = 0
    for line in data:
        print(line)
        acc += int(firstnum(line, False) + firstnum(line, True))
    return acc

# def p2():
#     rpl = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0}
#     acc = 0
#     for line in data:
#         for k,v in rpl.items():
#             line = line.replace(k, str(v))
#         print(line)
#         acc += int(firstnum(line, False) + firstnum(line, True))
#     return acc

# def p2():
#     rpl = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0}
#     acc = 0
#     for line in data:
#         i = 0
#         oline = line
#         line = list(line)
#         while i < len(line):
#             # print(line[i:i + len(k)])
#             for k,v in rpl.items():
#                 if ''.join(line[i:i+len(k)]) == k:
#                     line[i:i+len(k)] = str(v)
#             i += 1
#         line = ''.join(line)
#         to_acc = int(firstnum(line, False) + firstnum(line, True))
#         print(oline, line, to_acc)
#         acc += to_acc
#     return acc
# not 55061?


setday(1)

data = parselines()
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
