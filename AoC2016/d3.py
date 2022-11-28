from aoc import *


def p1(data):
    cum = 0
    for line in data:
        line = sorted(line)
        if line[0] + line[1] > line[2]:
            cum += 1
    return cum


def p2():
    data2 = []
    for x in range(3):
        for y in range(0, len(data), 3):
            data2.append([data[y+n][x] for n in range(3)])
    return p1(data2)


day = 3
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(n) for n in line.strip().split()] for line in file]

print(f'part1: {p1(data)}')
print(f'part2: {p2()}')
