import itertools
import math
from collections import Counter

from ec import *


def p1():
    data = parse_double_break(1)

    window_a = parse_grid_raw(data[0].split('\n'))[0]
    window_b = parse_grid_raw(data[1].split('\n'))[0]

    bins = defaultdict(int)
    for point in window_a:
        a = window_a[point]
        b = window_b[point]
        a, b = sorted((a, b))
        if 'K' in (a, b):
            bins['K'] += 1
        elif a == 'C' and b == 'M':
            bins['B'] += 1
        elif a == 'C' and b == 'Y':
            bins['G'] += 1
        elif a == 'M' and b == 'Y':
            bins['R'] += 1

    return math.prod(sorted(bins.values())[-3:])


def p2():
    data = parse_double_break(2)

    window_a = parse_grid_raw(data[0].split('\n'))[0]
    window_b = parse_grid_raw(data[1].split('\n'))[0]

    list_a = ['1', '2', '3', '4']
    list_b = ['C', 'M', 'Y', 'K']

    best = 0

    for order in [list(zip(p, list_b)) for p in itertools.permutations(list_a)]:
        bins = defaultdict(int)
        color_map = {x[0]: x[1] for x in order}

        for point in window_a:
            a = window_a[point]
            b = color_map[window_b[point]]
            a, b = sorted((a, b))
            if 'K' in (a, b):
                bins['K'] += 1
            elif a == 'C' and b == 'M':
                bins['B'] += 1
            elif a == 'C' and b == 'Y':
                bins['G'] += 1
            elif a == 'M' and b == 'Y':
                bins['R'] += 1

        best = max(best, math.prod(sorted(bins.values())[-3:]))
    return best


def p3():
    data = Counter(''.join(parse_lines(3)))
    k = data.pop('K') if 'K' in data else 0

    ints = sorted(list(data.values()))
    total = sum(ints)

    n = 2 if (sum(ints) // 3) <= k else 3

    if ints[-1] > math.floor(total * (1 / (n / (n - 1)))):
        print('warning: the following may be incorrect')

    avg = total // n
    r = total % n
    ints = [avg + (1 if i < r else 0) for i in range(n)] + [k]
    ints.append(k)

    return math.prod(sorted(ints)[-3:])


if __name__ == '__main__':
    setquest(19)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
