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
    for line in data:
        for l,r in [(str(l), str(r)) for l in range(9,-1,-1) for r in range(9, -1, -1)]:
            if re.search(f'{l}.*{r}', line) is not None:
                acc += int(l+r)
                break
    return acc


def p2():
    acc = 0
    for line in data:
        print(line)
        i = 1
        line = list(line)
        while len(line) > 12 and i < 10:
            i_s = str(i)
            while len(line) > 12 and i_s in line:
                line.remove(i_s)
                print(line)
            i += 1
        i_rev = int(''.join(line))
        print(i_rev)
        acc += i_rev
    return acc


def p2():
    def dfs(src, length, neighbors):
        q = deque([(-int(line[src]), -1, src, [src])])
        # q = [(src, 1, [src])]

        parent = {}

        while q:
            # cur, d, path = q.popleft()
            # cur, d, path = q.pop()
            _, d, cur, path = heapq.heappop(q)
            print(d, _)
            # print(cur, d)
            if d == -length:
                break

            for n in neighbors[cur]:
                # if n in parent:
                #     continue
                parent[n] = cur
                n_list = path + [n]
                q.append((-int(''.join(line[i] for i in n_list)), d-1, n, n_list))

        # pos = cur
        # path = []
        # while pos != src:
        #     # print(path)
        #     path.append(pos)
        #     pos = parent[pos]
        # path.append(src)
        # path.reverse()
        return path

    acc = 0
    for line in data:
        neighbors = {}
        for i, c in enumerate(line):
            i_neighbors = []
            for n in range(9,0,-1):
                n_s = str(n)
                for j, c2 in enumerate(line[i+1:]):
                    if c2 == n_s:
                        i_neighbors.append(i+j+1)
            neighbors[i] = i_neighbors
        print(line)
        print(neighbors)
        # input()

        start_pos = INF
        ln = len(line)
        for i in range(9,0,-1):
            loc = line.find(str(i))
            print(i, loc)
            if 0 <= loc <= (ln - 12):
                start_pos = loc
                break
        print(start_pos, '=', line[start_pos])
        # continue

        r = dfs(start_pos, 12, neighbors)
        n = int(''.join(line[i] for i in r))
        print('as n:', n)

        # print('best in line', line, ':', best)
        acc += n
    return acc
        # print('r:', best)



def p2():
    acc = 0
    for line in data:
        built = []
        current_index = 0
        ln = len(line)
        for limit in range(12,0,-1):
            search_space = line[current_index:ln-limit+1]
            print('biggest number in', search_space, 'current_index:', current_index)
            for i in range(9,0,-1):
                # print('bb', ln, limit, (ln-limit))
                # print('aa', search_space)
                loc = search_space.find(str(i))
                print(i, loc)
                if loc >= 0:
                    built.append(line[current_index + loc])
                    current_index = current_index + loc + 1
                    break
            print(built)
        print(built)

        # continue

        # r = dfs(start_pos, 12, neighbors)
        # n = int(''.join(line[i] for i in r))
        # print('as n:', n)

        # print('best in line', line, ':', best)
        acc += int(''.join(built))
    return acc
        # print('r:', best)



if __name__ == '__main__':
    setday(3)

    data = parselines()
    # data = parselines(get_ints)
    # grid, inverse, unique = parsegrid()

    # with open_default() as file:
    #     data = get_ints(file.read())

    print('part1:', p1() )
    print('part2:', p2() )

    # print('part1: %d\npart2: %d' % solve())
