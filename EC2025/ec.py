import heapq
import re
import sys
from collections import defaultdict, deque
from functools import lru_cache
from operator import itemgetter

INF = sys.maxsize

memo = lru_cache(maxsize=None)
memo1m = lru_cache(maxsize=2 ** 20)

_QUEST = None

verbose = '-v' in sys.argv or '--verbose' in sys.argv

def setquest(n):
    global _QUEST
    assert isinstance(n, int), 'quest must be int, not %s' % (type(n),)
    assert n > 0, 'you forgot to set the quest again!'
    assert _QUEST is None, 'setquest() multiple times'
    _QUEST = n


class open_default(object):
    def __init__(self, n):
        if len(sys.argv) > 1 and sys.argv[1][1] != '-':
            self.fn = sys.argv[1]
        else:
            self.fn = f'q{_QUEST}_{n}.txt'

    def __enter__(self):
        self.file = open(self.fn)
        return self.file

    def __exit__(self, *args):
        self.file.close()


def get_ints(s):
    return [int(i) for i in re.findall(r'-?[0-9]+', s)]


def parse_lines(func=None):
    with open_default() as file:
        if func:
            return [func(line.strip('\r\n')) for line in file]
        else:
            return [line.strip('\r\n') for line in file]


def parse_double_break(n):
    with open_default(n) as file:
        return file.read().split('\n\n')


def parse_grid(n, ignore=None):
    grid = {}
    inverse = defaultdict(list)
    unique = {}
    non_unique = set()

    for y, line in enumerate(parse_lines(n)):
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


def print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
    print_2d_repl(padding, *([v, {}] for v in dicts), constrain=constrain)


def print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):
    points = []
    for d in dicts:
        points.extend([k for k, v in d[0].items() if isinstance(k, tuple)])
    from operator import itemgetter
    bounds = max(constrain[0], min(points, key=itemgetter(0))[0]), max(constrain[1], min(points, key=itemgetter(1))[1]), \
             min(constrain[2], max(points, key=itemgetter(0))[0]), min(constrain[3], max(points, key=itemgetter(1))[1])
    for y in range(bounds[1], bounds[3] + 1):
        for x in range(bounds[0], bounds[2] + 1):
            c = padding
            for i in range(len(dicts) - 1, -1, -1):
                d, repl = dicts[i]
                if (x, y) in d:
                    c = d[x, y]
                    c = repl[c] if c in repl else str(c)
                    c = c + padding[len(c):] if len(c) < len(padding) else c[:len(padding)]
                    break
            print(c, end='')
        print()


def grid_bounds(d):
    return min(d, key=itemgetter(0))[0], min(d, key=itemgetter(1))[1], \
           max(d, key=itemgetter(0))[0], max(d, key=itemgetter(1))[1]


def vadd(a, b):
    return tuple(c1 + c2 for c1, c2 in zip(a, b))


def vsub(a, b):
    return tuple(c1 - c2 for c1, c2 in zip(a, b))


def vmul(a, b):
    if isinstance(a, (int, float)):
        return tuple(a * c2 for c2 in b)
    elif isinstance(b, (int, float)):
        return tuple(c1 * b for c1 in a)
    else:
        return tuple(c1 * c2 for c1, c2 in zip(a, b))


def vdiv(a, b):
    if isinstance(a, (int, float)):
        return tuple(a / c2 for c2 in b)
    elif isinstance(b, (int, float)):
        return tuple(c1 / b for c1 in a)
    else:
        return tuple(c1 / c2 for c1, c2 in zip(a, b))

def vidiv(a, b):
    if isinstance(a, (int, float)):
        return tuple(a // c2 for c2 in b)
    elif isinstance(b, (int, float)):
        return tuple(c1 // b for c1 in a)
    else:
        return tuple(c1 // c2 for c1, c2 in zip(a, b))


def vmod(a, b):
    if isinstance(a, (int, float)):
        return tuple(a % c2 for c2 in b)
    elif isinstance(b, (int, float)):
        return tuple(c1 % b for c1 in a)
    else:
        return tuple(c1 % c2 for c1, c2 in zip(a, b))


def vdot(a, b):
    return sum(c1 * c2 for c1, c2 in zip(a, b))


def vmag2(a):
    """Magnitude"""
    return sum(c * c for c in a)


def vdist2(a, b):
    """Distance"""
    return vmag2(vsub(a, b))


def vmagm(a):
    """Magnitude, measured in Manhattan distance"""
    return sum(abs(c) for c in a)


def vdistm(a, b):
    """Manhattan distance"""
    return vmagm(vsub(a, b))


# starting from east, running ccw
DIRS = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

DIAGDIRS = [
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

HEXDIRS = [
    (0, 1, -1),
    (-1, 1, 0),
    (-1, 0, 1),
    (0, -1, 1),
    (1, -1, 0),
    (1, 0, -1),
]


def hexdist(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2


def bfs(src, tgt, neighbors):
    q = deque([src])

    parent = {}

    while q:
        cur = q.popleft()
        if cur == tgt:
            break

        for n in neighbors[cur]:
            if n in parent:
                continue
            parent[n] = cur
            q.append(n)

    if tgt not in parent:
        return None

    pos = tgt
    path = []
    while pos != src:
        path.append(pos)
        pos = parent[pos]
    path.append(src)
    path.reverse()
    return path


def wbfs(src, tgt, edges):
    """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
    a list of `(node, cost)` pairs."""
    q = [(0, src, None)]

    parent = {}

    while q:
        cost, cur, prev = heapq.heappop(q)
        if cur in parent:
            continue
        parent[cur] = prev
        if cur == tgt:
            break

        for (n, ncost) in edges(cur):
            if n in parent:
                continue
            heapq.heappush(q, (cost + ncost, n, cur))

    if tgt not in parent:
        return None

    pos = tgt
    path = []
    while pos != src:
        path.append(pos)
        pos = parent[pos]
    path.append(src)
    path.reverse()
    return path


def astar(src, tgt, edges, heur):
    """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
    a list of `(node, cost)` pairs.  `heur` takes a pair of node labels and
    returns an estimated cost to move between them."""
    q = [(0, 0, src, None)]

    parent = {}

    while q:
        f, g, cur, prev = heapq.heappop(q)
        if cur in parent:
            continue
        parent[cur] = prev
        if cur == tgt:
            break

        for (n, w) in edges(cur):
            if n in parent:
                continue
            ng = g + w
            nh = heur(n, tgt)
            nf = ng + nh
            heapq.heappush(q, (nf, ng, n, cur))

    if tgt not in parent:
        return None

    pos = tgt
    path = []
    while pos != src:
        path.append(pos)
        pos = parent[pos]
    path.append(src)
    path.reverse()
    return path


def die(msg='the impossible happened'):
    raise RuntimeError(msg)
