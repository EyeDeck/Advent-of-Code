import sys
from collections import *


def stepgrow(polymer):
    cur = polymer[0]
    while True:
        nxt = cur.next
        if nxt is None:
            return
        pair = ''.join((cur.d, nxt.d))
        if pair not in rules:
            continue
        insert = Node(rules[pair])
        insert.prev = cur
        insert.next = nxt
        cur.next = insert
        nxt.prev = insert
        cur = nxt
        # print(pair)


def p1():
    polymer = [Node(template[0])]
    for e in template[1:]:
        p = Node(e)
        prev = polymer[-1]
        p.prev = prev
        prev.next = p
        polymer.append(p)
    # print(ply)
    for i in range(10):
        stepgrow(polymer)
    quantities = defaultdict(int)
    cur = polymer[0]
    while True:
        quantities[cur.d] += 1
        cur = cur.next
        if cur is None:
            break
    return max(quantities.values()) - min(quantities.values())


def stepgrowbetter(polymer):
    new_polymer = defaultdict(int)
    for k, v in polymer.items():
        if k not in rules:
            pass  # ??
        m = rules[k]
        l = k[0] + m
        r = m + k[1]
        new_polymer[l] += v
        new_polymer[r] += v
    return new_polymer


def p2():
    polymer = defaultdict(int)
    for i in range(len(template) - 1):
        polymer[''.join((template[i], template[i + 1]))] += 1
    print(polymer)
    for i in range(40):
        polymer = stepgrowbetter(polymer)
        print(polymer)
        print('...')
    fug = defaultdict(int)
    for k,v in polymer.items():
        fug[k[0]] += v
    print(fug)
    print(polymer)
    fug[template[-1]] += 1  # lol idk
    return max(fug.values()) - min(fug.values())


class Node:
    def __init__(self, d=None):
        self.d = d
        self.next = None
        self.prev = None


day = 14
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    template, rules = file.read().split('\n\n')

template = [c for c in template]
rules = [line.strip().split(' -> ') for line in rules.split('\n')]
rules = {line[0]: line[1] for line in rules}

print(f'part1: {p1()}')
print(f'part2: {p2()}')
