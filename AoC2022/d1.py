from aoc import *


def p1():
    return sorted([sum(n) for n in data])[-1]


def p2():
    return sum(sorted([sum(n) for n in data])[-3:])


day = 1
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) for i in n.split('\n')] for n in file.read().split('\n\n')]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
