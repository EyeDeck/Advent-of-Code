# 193354 posted his library one time, so I copied the entire thing
# I've since edited it it a fair bit, but credit still goes to that good lad

import string
from collections import deque, defaultdict
import heapq
from functools import lru_cache
import re
import sys
from operator import itemgetter

# setday(n)
# parselines(function_to_run_each_line_through=None)
# parsegrid()
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
# mkcls('Name', f1=v1, f2=v2, ...)

INF = sys.maxsize

_PROBLEM = None

fst = lambda x: x[0]
snd = lambda x: x[1]
nth = lambda n: lambda x: x[n]

memo = lru_cache(maxsize=None)
memo1m = lru_cache(maxsize=2 ** 20)


def print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
    print_2d_repl(padding, *([v, {}] for v in dicts), constrain=constrain)


def print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):
    points = []
    for d in dicts:
        points.extend([k for k, v in d[0].items() if isinstance(k, tuple)])
    from operator import itemgetter
    bounds = max(constrain[0], min(points, key=itemgetter(0))[0]), max(constrain[1], min(points, key=itemgetter(1))[1]), \
             min(constrain[2], max(points, key=itemgetter(0))[0]), min(constrain[2], max(points, key=itemgetter(1))[1])
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


def rotate_point_around_origin(x, y, origin_x, origin_y, angle, clockwise=True):
    offset_x = x - origin_x
    offset_y = y - origin_y
    if angle % 90 == 0:
        if angle == 180:
            offset_x *= -1
            offset_y *= -1
        else:
            offset_x, offset_y = offset_y, offset_x
            if clockwise:
                if angle == 90:
                    offset_y *= -1
                elif angle == 270:
                    offset_x *= -1
            else:
                if angle == 90:
                    offset_x *= -1
                elif angle == 270:
                    offset_y *= -1
        return offset_x + origin_x, offset_y + origin_y
    else:
        die('unimplemented angle')


def setday(n):
    global _PROBLEM
    assert isinstance(n, int), 'day must be int, not %s' % (type(n),)
    assert n > 0, 'you forgot to set the day again!'
    assert _PROBLEM is None, 'setproblem() multiple times'
    _PROBLEM = n


class open_default(object):
    def __init__(self):
        if len(sys.argv) > 1:
            self.fn = sys.argv[1]
        else:
            self.fn = f'd{_PROBLEM}.txt'

    def __enter__(self):
        self.file = open(self.fn)
        return self.file

    def __exit__(self, *args):
        self.file.close()


def parselines(func=None):
    with open_default() as file:
        if func:
            return [func(line.strip()) for line in file]
        else:
            return [line.strip() for line in file]


def parsegrid(ignore=None):
    grid = {}
    inverse = defaultdict(list)
    unique = {}
    non_unique = set()

    for y, line in enumerate(parselines()):
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


def get_ints(s):
    return [int(i) for i in re.findall(r'-?[0-9]+', s)]


def do_scrub(s, scrub='[^a-zA-Z0-9]'):
    """Remove characters designated by `scrub` from `s`."""
    # If it starts with '[' then it's probably a regex character class.
    # Otherwise, assume it's a normal list of characters.
    if scrub.startswith('['):
        s = re.sub(scrub, ' ', s)
    else:
        for c in scrub:
            s = s.replace(c, ' ')
    return s


def die(msg='the impossible happened'):
    raise RuntimeError(msg)


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


def ccs(srcs, neigh, filt=None):
    """Compute connected components containing `srcs`.  `neigh` takes a node
    label and returns a list of neighboring nodes.  `filt` returns `False` if a
    node should be ignored."""
    seen = set()

    def go(start):
        if start in seen:
            return None

        stk = [start]
        comp = set()

        while stk:
            cur = stk.pop()
            if cur in seen:
                continue
            seen.add(cur)
            comp.add(cur)

            for n in neigh(cur):
                if filt is None or filt(n):
                    stk.append(n)

        return comp

    comps = []

    for s in srcs:
        if filt is not None and not filt(s):
            continue

        comp = go(s)
        if comp is not None:
            comps.append(comp)

    return comps


def splat(f):
    def g(t):
        return f(*t)

    return g


# starting from north, running ccw
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


def plot(pts, on='@', off='.', bbox=None):
    pts = set(pts)

    if bbox is not None:
        x0, y0, x1, y1 = bbox
    else:
        x0 = min(x for x, y in pts)
        x1 = max(x for x, y in pts)
        y0 = min(y for x, y in pts)
        y1 = max(y for x, y in pts)

    rows = ['%d %d %d %d' % (x0, y0, x1, y1)]
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            if (x, y) in pts:
                row.append(on)
            else:
                row.append(off)
        rows.append(''.join(row))
    return '\n'.join(rows)


def plotdct(pts, f=lambda x: x, default='.', bbox=None):
    if bbox is not None:
        x0, y0, x1, y1 = bbox
    else:
        x0 = min(x for x, y in pts)
        x1 = max(x for x, y in pts)
        y0 = min(y for x, y in pts)
        y1 = max(y for x, y in pts)

    rows = []
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            if (x, y) in pts:
                row.append(f(pts[(x, y)]))
            else:
                row.append(default)
        rows.append(''.join(row))
    return '\n'.join(rows)


def tobits(bs):
    """Build a bitmask from a sequence of bools (little-endian)."""
    return sum(1 << i for i, b in enumerate(bs) if b)


def frombits(x, bitlen=None):
    """Build a list of bools from a bitmask (little-endian).  If `bitlen` is
    set, the output list will have length `bitlen` (otherwise, it will be just
    long enough to contain every `1` bit."""
    if bitlen:
        return [bool(x & (1 << i)) for i in range(bitlen)]
    else:
        assert x >= 0
        bs = []
        while x != 0:
            bs.append(bool(x & 1))
            x >>= 1
        return bs


def bitmask(idxs):
    """Compute a bitmask with 1s at the positions listed in `idxs` (0 = LSB)."""
    return sum(1 << i for i in idxs)


def bitrev(x, bitlen):
    """Reverse the bits of `x`, treating it as a `bitlen`-length word."""
    return sum(1 << i for i in range(bitlen) if x & (1 << (bitlen - i - 1)))


def bitslice(x, lo, hi):
    """Extract bits lo .. hi of `x`."""
    return (x >> lo) & ((1 << (hi - lo)) - 1)


class Dedup:
    def __init__(self):
        self._seen = set()

    def seen(self, x):
        """Returns `False` on the first call to `self.seen(x)`, `True` on all
        later calls."""
        if isinstance(x, list):
            x = tuple(x)
        elif isinstance(x, set):
            x = tuple(sorted(x))
        elif isinstance(x, dict):
            x = tuple(sorted(x.items()))
        result = x in self._seen
        self._seen.add(x)
        return result
