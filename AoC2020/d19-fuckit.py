import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
# from blist import blist
from collections import *
from math import *
from pprint import pprint
import re
import sys

from aoc import *
# INF = 999999999
# mkmat(sx, sy, val=0)
# fw(m)
# get0()
# get1(cvt=str)
# get2(cvt=str)
# @memo
# splat(f)
# bfs(src, tgt, {n1: [n2, n3, n4]})
# wbfs(src, tgt, edge_func)
# astar(src, tgt, edge_func, heur_func)
# ccs(srcs, neigh_func, filt_func?)
# Dedup().seen(x)
# mkcls('Name', f1=v1, f2=v2, ...)

# memory = {}
# # def get_regex_for_ind(s):
# #     expr = ''
# #     if s in memory:
# #         return memory[s]
# #
# #     if isinstance(s, str):
# #         if s.isdigit():
# #             expr += get_regex_for_ind(s)
# #         else:
# #             expr += s
# #     elif isinstance(s, list):
# #         for part in s:
# #             expr += get_regex_for_ind(part)
# #
# #     # for part in s:
# #     #     print(part)
# #     #     input()
# #     #     if isinstance(part, str):
# #     #         if part.isdigit():
# #     #             expr += get_regex_for_ind(part)
# #     #         else:
# #     #             expr += s
# #     #     elif isinstance(part, list):
# #     #         p_rule = r_raw[part]
# #     #         print(p_rule)
# #
# #     memory[s] = expr
# #     return expr
#
#
# # def parse_rules():
# #     # r = {}
# #     # for rule in rules:
# #     #     s = rule.split(':')
# #     #     r[s[0]] = [[c.strip().strip('"') for c in n.strip().split(' ')] for n in s[1].split('|')]
# #
# #     # r = {}
# #     # for rule in rules:
# #     #     s = rule.split(':')
# #     #     r[s[0]] = [c.strip().strip('"') for c in n.strip().split(' ') for n in s[1]]
# #
# #     #return r
#
#
# def p1():
#     while True:
#         # print(regex)
#         # for k in regex.keys():
#         #     expr = ''
#         #     for lst in regex[k]:
#         #         print(lst)
#         #         for i, c in enumerate(lst):
#         #             if isinstance(c, str) and c.isnumeric():
#         #                 lst[i] = regex[c]
#         #             else:
#         #                 break
#         #     # print(regex[k])
#         # for k,v in regex.items():
#         #     if isinstance(v, list):
#         #         if len(v) == 1:
#         #             regex[k] = v[0]
#         #             print('hit')
#         #         else:
#         #             for i,v2 in enumerate(v):
#         #                 if isinstance(v2, str):
#         #                     if v2.isdigit():
#         #                         if isinstance(regex[v2], str):
#         #                             v[i] = regex[v2]
#         #                 print(i, v2)
#
#             print(regex)
#             input()
#
#             # if isinstance(regex[a])
#
#     return None
#
# def p2():
#     return None


f = 'd19.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().split('\n\n')
    print(data)
    rules = [line.strip() for line in data[0].split('\n')]
    msgs = [line.strip() for line in data[1].split('\n')]

# regex = {k:v for k,v in rules.split(':')}
regex = {}
for line in rules:
    k,v = line.strip().split(':')
    regex[k] = v.strip().strip('"').split(' ')

print(regex)


def any_numbers(l):
    for i in l:
        if i.isdigit():
            return True
    return False


def iterative_parse(rx):
    worked = False
    for k,v in regex.items():
        if isinstance(v,list):
            if len(v) == 1:
                regex[k] = v[0]
                worked = True
                continue
            else:
                for i, n in enumerate(v):
                    if n.isdigit() and isinstance(regex[n], str):
                        v[i] = regex[n]
                        worked = True
            if not any_numbers(v):
                regex[k] = '(' + ''.join(v) + ')'
                worked = True
    if not worked:
        print('no work 8', regex['8'], '\n\n\n')
        for k,v in regex.items():
            if isinstance(v, list):

                # if len(regex[k]) > 20:
                #     break
                # for i, n in enumerate(v):
                #     if n.isdigit():
                #         regex[k] = v[:i] + v
                #         iterative_parse(rx)
                for i, n in enumerate(v):
                    if n.isdigit():
                        regex[k][i] = '+'
                        iterative_parse(rx)

        print('post 8', regex['8'], '\n\n\n')
    return worked


def finish():
    for k, v in regex.items():
        if isinstance(v, list):
            for i in v:
                if i.isdigit():
                    v.remove(i)
        if not any_numbers(v):
            regex[k] = '(' + ''.join(v) + ')'


def p1():
    while iterative_parse(regex):
        pass #print(regex)
    finish()
    while iterative_parse(regex):
        pass
    #print(regex)
    #print('last:', regex['0'])
    ct = 0
    for s in msgs:
        founds = re.findall('^' + regex['0'] + '$', s)
        if len(founds) == 1:
            ct += 1
            # print(founds, regex['0'])

    return ct

print(f'part1: {p1()}')
# print(f'part2: {p2()}')

#260 too low