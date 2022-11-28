import sys
import re
from collections import deque
from math import *


class Node:
    def __init__(self, d=None, next=None, prev=None):
        self.d = d
        self.next = next
        self.prev = prev


def parse_line(line):
    line = line.strip()
    p = [[None, None]]
    for c in line:
        n = Node(None)
        p.append(n)
        if c.isnumeric():
            n.d = int(c)
            n.prev = p[0][1]
            if p[0][0] is None:
                p[0][0] = n
            if p[0][1] is not None:
                p[0][1].next = n
            p[0][1] = n
        else:
            n.d = c
    # print(as_str(p[1:]))
    return p


def as_str(line):
    return ''.join([str(n.d) for n in line])


def add(a, b):
    b[0][0].prev, a[0][1].next = a[0][1], b[0][0]
    return [[a[0][0], b[0][1]], Node('[')] + a[1:] + [Node(',')] + b[1:] + [Node(']')]


def try_explode(line):
    depth = 0
    for i, node in enumerate(line[1:]):
        c = node.d
        depth += 1 if c == '[' else -1 if c == ']' else 0
        # print(depth)
        if depth == 5:
            to_explode = line[depth:depth+5]
            repl = Node(0)
            print(as_str(line[1:]))
            print('expl', as_str(to_explode), '\n')
            # input()
            l, r = to_explode[1], to_explode[3]
            ll, rr = l.prev, r.next
            if ll is not None:
                ll.d += l.d
            if rr is not None:
                rr.d += r.d
            full = line[:depth] + [repl] + line[depth+5:]
            return full, True
    return line, False


def try_split(line):
    for i, n in enumerate(line[1:]):
        c = n.d
        if not isinstance(c,int):
            continue
        if c > 9:
            ll, rr = n.prev, n.next
            l, r = Node(c//2), Node(ceil(c/2))
            l.prev, l.next, r.prev, r.next = ll, r, l, rr
            ins = [Node('['), l, Node(','), r, Node(']')]
            line[i:i+1] = [ins]
            if ll is None:
                line[0][0] = l
            if rr is None:
                line[0][1] = r
            return line, True
    return line, False


def tick_once(fish):
    fish, exploded = try_explode(fish)
    # print('fish', fish, '\nsplit', exploded, '\n')
    if exploded:
        return fish, True
    fish, split = try_split(fish)

    if split:
        return fish, True
    return fish, False


def reduce(fish):
    while True:
        fish, ticked = tick_once(fish)
        if not ticked:
            return fish


def r_mag(d):
    a,b = d
    if isinstance(a, list):
        a = r_mag(a)
    if isinstance(b, list):
        b = r_mag(b)
    return a*3 + b*2


def p1():
    # r, x= try_explode(parse_line('[[[[[9,8],1],2],3],4]'))
    # print(r)
    # print('\n')
    # print(as_str(r[1:]))
    # return
    a = parsed[0]
    for line in parsed[1:]:
        a = add(a, line)
        a = reduce(a)
    return r_mag(eval(a))


def p2():
    return None


day = 18
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

parsed = []
with open(f) as file:
    for line in file:
        parsed.append(parse_line(line))

print(f'part1: {p1()}')
print(f'part2: {p2()}')
