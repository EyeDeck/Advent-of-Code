import sys
from collections import *
from functools import reduce


def factors(n):
    return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))


def p1():
    i = 0
    while True:
        i += 1
        n = sum(n*10 for n in factors(i))
        if n >= data:
            return i
        # if i % 1000 == 0:
        #     print(i, '=', n)


def p2():
    i = 0
    elves = defaultdict(int)
    while True:
        i += 1
        f = [n for n in factors(i) if elves[n] < 50]
        for n in f:
            elves[n] += 1
        n = sum(n * 11 for n in f)
        if n >= data:
            return i
        # if i % 1000 == 0:
        #     print(i, '=', n)


day = 20
if len(sys.argv) <= 1 or sys.argv[1][-4:] == '.txt':
    if len(sys.argv) <= 1:
        f = f'd{day}.txt'
    else:
        f = sys.argv[1]
    with open(f) as file:
        data = int(file.read())
else:
    data = int(sys.argv[1])


print(f'part1: {p1()}')
print(f'part2: {p2()}')
