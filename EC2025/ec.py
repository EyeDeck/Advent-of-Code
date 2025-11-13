import re
import sys
from operator import itemgetter

INF = sys.maxsize

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


def parse_lines(n, func=None):
    with open_default(n) as file:
        if func:
            return [func(line.strip()) for line in file]
        else:
            return [line.strip() for line in file]


def parse_double_break(n):
    with open_default(n) as file:
        return file.read().split('\n\n')


def get_ints(s):
    return [int(i) for i in re.findall(r'-?[0-9]+', s)]


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


def grid_bounds(d):
    return min(d, key=itemgetter(0))[0], min(d, key=itemgetter(1))[1], \
           max(d, key=itemgetter(0))[0], max(d, key=itemgetter(1))[1]
