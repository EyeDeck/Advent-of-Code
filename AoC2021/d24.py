import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)
import functools  # @functools.cache
from collections import *
from math import *
from pprint import pprint

from aoc import *


def run(program, inputs):
    alu = defaultdict(int)
    alu['w'] = 0
    alu['x'] = 0
    alu['y'] = 0
    alu['z'] = 0
    i = 0
    try:
        for line in program:
            c = line.split()
            ins = c[0]
            if ins == 'inp':
                a = c[1]
                p = inputs[i]
                i += 1
                # print(a, p)
                alu[a] = p
                continue

            a, b = c[1:]
            if b[0] == '-' or b.isnumeric():
                b = int(b)
            else:
                b = alu[b]

            if ins == 'add':
                alu[a] += b
            elif ins == 'mul':
                alu[a] *= b
            elif ins == 'div':
                alu[a] //= b
            elif ins == 'mod':
                alu[a] %= b
            elif ins == 'div':
                alu[a] //= b
            elif ins == 'eql':
                alu[a] = 1 if alu[a] == b else 0

            # print(f'{line}  \t[{b}] \t\t{alu}')
    except IndexError:
        return False, alu
    return True, alu


def mult(w, a, b, z):
    x = 0 if ((z % 26) + a) == w else 1
    z = z * ((25 * x) + 1) + ((w + b) * x)
    return z


def div(w, a, b, z):
    x = 0 if ((z % 26) + a) == w else 1
    z = z // 26 * ((25 * x) + 1) + (x * (w + b))
    return z


ops = [
    (mult, 12, 7),
    (mult, 11, 15),
    (mult, 12, 2),
    (div, -3, 15),
    (mult, 10, 14),
    (div, -9, 2),
    (mult, 10, 15),
    (div, -7, 1),
    (div, -11, 15),
    (div, -4, 15),
    (mult, 14, 12),
    (mult, 11, 2),
    (div, -8, 13),
    (div, -10, 13)
]


def run_native(inp):
    z = 0
    i = 0
    try:
        for op, a, b in ops:
            z = op(inp[i], a, b, z)
            i += 1
    except IndexError:
        return False, z
    return True, z


def split(i):
    return [int(d) for d in str(i)]


def solve(a, b, c):
    possibilities = []

    for i in range(a, b, c):
        ints = [int(d) for d in str(i)]
        if 0 in ints:
            continue
        possibilities.append(i)
    while len(possibilities) > 0:
        cur = possibilities.pop()
        for i in range(a, b, c):
            nx = cur * 10 + i
            ints = split(nx)
            finished, z = run_native(ints)
            if finished:
                if z == 0:
                    return nx
            elif z < maxes_per_round[len(ints)]:
                possibilities.append(nx)


maxes_per_round = {
    1: 11881376,
    2: 456976,
    3: 17576,
    4: 676,
    5: 17576,
    6: 676,
    7: 17576,
    8: 456976,
    9: 17576,
    10: 676,
    11: 26,
    12: 676,
    13: 26,
    14: 0,
}

day = 24
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

p1 = solve(1, 10, 1)
p1_check = run(data, split(p1))[1]['z']
assert p1_check == 0

p2 = solve(9, 0, -1)
p2_check = run(data, split(p2))[1]['z']
assert p2_check == 0

print(f'part1: {p1}')
print(f'part2: {p2}')
