import itertools
import math
from collections import Counter
from z3 import Ints, Solver, sat, Optimize, Reals

from ec import *


def parse_grid(data, ignore=None):
    grid = {}
    inverse = defaultdict(list)
    unique = {}
    non_unique = set()

    for y, line in enumerate(data.split('\n')):
        for x, c in enumerate(line):
            if ignore is None or c not in ignore:
                grid[x, y] = c

                inverse[c].append((x, y))

                if c in unique:
                    del unique[c]
                    non_unique.add(c)
                elif c not in non_unique:
                    unique[c] = (x, y)

    return grid, inverse, unique


def p1():
    data = parse_double_break(1)

    print(data)

    window_a = parse_grid(data[0])[0]
    window_b = parse_grid(data[1])[0]

    print(window_a, window_b)

    bins = defaultdict(int)
    for point in window_a:
        print('pt', point)
        a = window_a[point]
        b = window_b[point]
        a,b = sorted((a,b))
        if 'K' in (a, b):
            bins['K'] += 1
        elif a == 'C' and b == 'M':
            bins['B'] += 1
        elif a == 'C' and b == 'Y':
            bins['G'] += 1
        elif a == 'M' and b == 'Y':
            bins['R'] += 1

    print(bins.values())
    return math.prod(sorted(bins.values())[-3:])



def p2():
    data = parse_double_break(2)

    window_a = parse_grid(data[0])[0]
    window_b = parse_grid(data[1])[0]

    list_a = ['1','2','3','4']
    list_b = ['C', 'M', 'Y', 'K']

    best = 0

    for order in [list(zip(p, list_b)) for p in itertools.permutations(list_a)]:
        bins = defaultdict(int)
        color_map = {x[0]:x[1] for x in order}

        for point in window_a:
            # print('pt', point)
            a = window_a[point]
            b = color_map[window_b[point]]
            a,b = sorted((a,b))
            if 'K' in (a, b):
                bins['K'] += 1
            elif a == 'C' and b == 'M':
                bins['B'] += 1
            elif a == 'C' and b == 'Y':
                bins['G'] += 1
            elif a == 'M' and b == 'Y':
                bins['R'] += 1

        print(bins.values())
        best = max(best, math.prod(sorted(bins.values())[-3:]))
    return best


def p3():
    data = Counter(''.join(parse_lines(3)))

    data.pop('K')

    print(data)

    opt = Optimize()

    C, M, Y = data['C'], data['M'], data['Y']

    C_B, C_G = Ints('C_B C_G')
    M_B, M_R = Ints('M_B M_R')
    Y_G, Y_R = Ints('Y_G Y_R')

    for i in [C_B, C_G, M_B, M_R, Y_G, Y_R]:
        opt.add(i >= 0)

    opt.add(C_B + C_G == C)
    opt.add(M_B + M_R == M)
    opt.add(Y_G + Y_R == Y)

    R_SUM = M_R + Y_R
    G_SUM = C_G + Y_G
    B_SUM = C_B + M_B

    product = R_SUM * G_SUM * B_SUM

    opt.maximize(product)

    result = opt.check()
    print(result)

    if result == sat:
        model = opt.model()
        return model.eval(product)
    else:
        return die()


if __name__ == '__main__':
    setquest(19)

    # print('part1:', p1())
    # print('part2:', p2())
    print('part3:', p3())
