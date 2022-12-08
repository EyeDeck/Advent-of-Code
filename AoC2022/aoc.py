import string
from collections import deque
import heapq
from functools import lru_cache
import re
import sys
from operator import itemgetter

# 193354 posted his library one time
# I don't think he minds if I borrow it

# INF = 999999999
# mkmat(sx, sy, val=0)
# fw(m)
# get0(scrub=re)
# get1(cvt=str, scrub=re)
# get2(cvt=str, scrub=re, maxsplit=-1)
# @memo
# splat(f)
# bfs(src, tgt, {n1: [n2, n3, n4]})
# wbfs(src, tgt, edge_func)
# astar(src, tgt, edge_func, heur_func)
# ccs(srcs, neigh_func, filt_func?)
# Dedup().seen(x)
# mkcls('Name', f1=v1, f2=v2, ...)

INF = sys.maxsize

def heurparse(f, try_grid=True):
    with open(f) as file:
        return rheurparse(file.read(), try_grid)

def rheurparse(raw, try_grid):
    # print(raw)
    if isinstance(raw, str):
        if raw.isdigit():
            return int(raw)

        if len(raw) == 1:
            return raw
        # print('RAW:', raw, '\n')

        # if there's a double newline, that should almost always be split on
        if raw.count('\n\n'):
            # print('found \\n\\n')

            # chunks = [rheurparse(line, try_grid) for line in raw.split('\n\n')] # raw.split('\n\n')
            chunks = [line.split('\n') for line in raw.split('\n\n')]
            # chunks = raw.split('\n\n')
            # print('chunks:', chunks)
            # input()
            try:
                if (type(chunks[0][0]) != type(chunks[0][1]) and isinstance(chunks[0][0], str)) \
                        or (re.match(r'\w', chunks[0][0]) and not re.match(r'\w', chunks[0][1])):
                    # print('asdafasfdasd')
                    return {v[0].strip('.:,- '): rheurparse('\n'.join(v[1:]), try_grid) for v in chunks}
            except:
                # print('damn')
                pass

            return chunks # [rheurparse(line) for line in chunks]

        raw_set = set(raw)
        # if it's all . and # it's probably a grid
        if '\n' in raw_set:
            # print(raw_set)
            if try_grid == 'force' or (try_grid and raw_set <= set(' ([{<>}])#.v^\n') or len(re.findall(r'\.|#', raw)) > len(raw) * 0.8):
                # print('gridding, n', raw.strip().count("\n"), '\n#############')
                grid = {}
                for y, line in enumerate(raw.split('\n')):
                    for x, c in enumerate(line):
                        # grids tend to be 1-indexed in descriptions
                        grid[x+1, y+1] = rheurparse(c, try_grid)
                return grid
            return [rheurparse(line, try_grid) for line in raw.split('\n')]

        if ',' in raw_set:
            return [rheurparse(line, try_grid) for line in raw.split(',')]

        # if re.match(re.match(r"^(?:\w+ +\w*)+$", raw.strip()):
        if ' ' in raw_set and raw_set <= set(string.ascii_lowercase + string.digits + '_ '):
            # print(f'space split "{raw}"')
            return [rheurparse(line, try_grid) for line in re.sub(' +', ' ', raw.strip()).split(' ')]
        # print(f'fell through "{raw}"')

    return raw


def print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
    print_2d_repl(padding, *([v, {}] for v in dicts), constrain=constrain)


def print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):
    points = []
    for d in dicts:
        points.extend([k for k, v in d[0].items() if isinstance(k, tuple)])
    from operator import itemgetter
    bounds = max(constrain[0], min(points, key=itemgetter(0))[0]), max(constrain[1], min(points, key=itemgetter(1))[1]), \
             min(constrain[2], max(points, key=itemgetter(0))[0]), min(constrain[2], max(points, key=itemgetter(1))[1])
    for y in range(bounds[1], bounds[3]+1):
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


def mkmat(sx, sy, val=0):
    return [[val for _ in range(sx)] for _ in range(sy)]


def fw(m):
    for k in range(len(m)):
        for i in range(len(m)):
            for j in range(len(m)):
                m[i][j] = min(m[i][j], m[i][k] + m[k][j])


def do_scrub(scrub, s):
    """Remove characters designated by `scrub` from `s`."""
    # If it starts with '[' then it's probably a regex character class.
    # Otherwise, assume it's a normal list of characters.
    if scrub.startswith('['):
        s = re.sub(scrub, ' ', s)
    else:
        for c in scrub:
            s = s.replace(c, ' ')
    return s


def oneof(*cvts):
    def oneof_cvt(s):
        for cvt in cvts:
            try:
                return cvt(s)
            except:
                pass
        raise ValueError('failed to parse %s with %s' % (s, cvts))

    return oneof_cvt


def parse(s, cvt=str, scrub=None, spliton=None, maxsplit=-1):
    if scrub:
        s = do_scrub(scrub, s)
    s = s.strip()
    if isinstance(cvt, (list, tuple, dict)):
        maxsplit = len(cvt) - 1
    return parselist(s.split(spliton, maxsplit), cvt=cvt)


def parselist(ss, cvt=str):
    if isinstance(cvt, (list, tuple)):
        parsed = []
        for i in range(len(cvt)):
            if i < len(ss):
                parsed.append(cvt[i](ss[i]))
            else:
                parsed.append(None)
        return parsed
    elif isinstance(cvt, dict):
        parsed = {}
        for i, k in enumerate(cvt.keys()):
            if i < len(ss):
                parsed[k] = cvt[k](ss[i])
            else:
                parsed[k] = None
        return parsed
    else:
        return [cvt(x) for x in ss]


_PROBLEM = None


def setproblem(n):
    global _PROBLEM
    assert isinstance(n, int), 'problem number must be int, not %s' % (type(n),)
    assert _PROBLEM is None, 'setproblem() multiple times'
    _PROBLEM = n


def inpfile():
    assert _PROBLEM is not None, 'called inpfile() before setproblem()'
    if len(sys.argv) > 1:
        suffix = sys.argv[1]
    else:
        suffix = ''
    return open('in%d%s.txt' % (_PROBLEM, suffix))


def get0(scrub=None):
    """Get the entire input from stdin.  Input is scrubbed using
    `do_scrub(scrub, _)`."""
    s = inpfile().read().strip()
    if scrub is not None:
        s = do_scrub(scrub, s)
    return s


def get1(cvt=str, scrub=None):
    """
    scrubbed, stripped, and converted using `cvt`."""
    clean_lines = []
    for line in inpfile():
        if scrub:
            line = do_scrub(scrub, line)
        line = line.strip()
        clean_lines.append(line)
    return parselist(clean_lines, cvt=cvt)


def get2(cvt=str, scrub=None, maxsplit=-1):
    """Get 2-dimensional input from stdin.  `cvt` and `scrub` work as in
    `get1`."""
    lines = get1()
    return [parse(line, cvt=cvt, scrub=scrub, maxsplit=maxsplit)
            for line in lines]


DEFAULT_SCRUB = '[^a-zA-Z0-9]'


# Same as get0/1/2, but with an automatic default for `scrub`.
def get0s(scrub=DEFAULT_SCRUB):
    return get0(scrub=scrub)


def get1s(cvt=str, scrub=DEFAULT_SCRUB):
    return get1(cvt=cvt, scrub=scrub)


def get2s(cvt=str, maxsplit=-1, scrub=DEFAULT_SCRUB):
    return get2(cvt=cvt, scrub=scrub, maxsplit=maxsplit)


def get0sd(scrub='[^0-9-]'):
    return get0(scrub=scrub)


def get1sd(cvt=int, scrub='[^0-9-]'):
    return get1(cvt=cvt, scrub=scrub)


def get2sd(cvt=int, maxsplit=-1, scrub='[^0-9-]'):
    return get2(cvt=cvt, scrub=scrub, maxsplit=maxsplit)


class dictobj:
    def __init__(self, *args, **kwargs):
        object.__setattr__(self, '_d', dict(*args, **kwargs))

    def __getattr__(self, k):
        return self._d[k]

    def __setattr__(self, k, v):
        self._d[k] = v

    def __delattr__(self, k):
        del self._d[k]

    def __repr__(self):
        return 'dictobj(%r)' % (self._d,)

    def __str__(self):
        return 'dictobj(%s)' % (self._d,)


def mkcls(name, *args, **kwargs):
    fields = dict(*args, **kwargs)

    def init(self, *args, **kwargs):
        for k, v in fields.items():
            setattr(self, k, v)
        for k, v in zip(fields.keys(), args):
            setattr(self, k, v)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def rep(self):
        return '%s(%r)' % (name,
                           dict((k, getattr(self, k)) for k in fields.keys()))

    return type(name, (object,), dict(
        __slots__=tuple(fields.keys()),
        __init__=init,
        __repr__=rep,
        __str__=rep,
    ))


fst = lambda x: x[0]
snd = lambda x: x[1]
nth = lambda n: lambda x: x[n]

memo = lru_cache(maxsize=None)
memo1m = lru_cache(maxsize=2 ** 20)


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
