import collections
import functools

from aoc import *


def knot_hash(s):
    LENGTH = 256

    def rounds(lengths, ct):
        x = [i for i in range(LENGTH)]
        skip = 0
        pos = 0
        for _ in range(ct):
            for n in lengths:
                for i in range(n // 2):
                    a = (pos + i) % LENGTH
                    b = (pos + n - i - 1) % LENGTH
                    x[a], x[b] = x[b], x[a]
                pos = (pos + n + skip) % LENGTH
                skip += 1
        return x

    lengths = [ord(c) for c in s] + [17, 31, 73, 47, 23]
    x = rounds(lengths, 64)
    dense = [functools.reduce(lambda a, b: a ^ b, x[n:n + 16]) for n in range(0, 256, 16)]
    hex_str = ''.join(f'{n:02x}' for n in dense)
    assert len(hex_str) == 32
    return hex_str


def p1():
    return sum(collections.Counter(f"{int(knot_hash(f'{data}-{i}'), 16):0128b}")['1'] for i in range(128))


def p2():
    grid = set()
    for y in range(128):
        for x, c in enumerate(f"{int(knot_hash(f'{data}-{y}'), 16):0128b}"):
            if c == '1':
                grid.add((x, y))
    if verbose:
        print_2d('.', {k: '#' for k in grid})
    r_count = 0
    while grid:
        r_count += 1
        frontier = {grid.pop()}
        while frontier:
            cur = frontier.pop()
            for d in DIRS:
                n = vadd(cur, d)
                if n in grid:
                    frontier.add(n)
                    grid.remove(n)
    return r_count


setday(14)

with open_default() as file:
    data = file.read().strip()


verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
