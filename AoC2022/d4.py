from aoc import *


def p1():
    total = 0
    for line in data:
        line = sorted(line, key=itemgetter(0))
        # print(line)
        # if line[0][0] <= line[1][0] and line[0][1] >= line[1][1]:
        if (line[0][0] <= line[1][0] and line[0][1] >= line[1][1]) or (line[1][0] <= line[0][0] and line[1][1] >= line[0][1]):
            print(line)
            total += 1
    return total


def p2():
    total = 0
    for line in data:
        if len( set(i for i in range(line[0][0], line[0][1]+1)) & set(i for i in range(line[1][0], line[1][1]+1))):
            total += 1
    return total


day = 4
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[[int(i) for i in l.split('-')] for l in line.strip().split(',')] for line in file]
# data = heurparse(f)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
