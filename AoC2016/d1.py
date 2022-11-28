from aoc import *


def p1():
    heading = 3
    x, y = 0, 0
    for d, n in data:
        if d == 'R':
            heading += 1
        elif d == 'L':
            heading -= 1
        heading %= 4
        x += DIRS[heading][0] * n
        y += DIRS[heading][1] * n
    return abs(x) + abs(y)


def p2():
    visited = {(0, 0)}
    heading = 3
    x, y = 0, 0
    for d, n in data:
        if d == 'R':
            heading += 1
        elif d == 'L':
            heading -= 1
        heading %= 4
        for i in range(n):
            x += DIRS[heading][0]
            y += DIRS[heading][1]
            if (x, y) in visited:
                return abs(x) + abs(y)
            visited.add((x, y))


day = 1
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [x.strip() for x in file.read().split(',')]
data = [(x[0], int(x[1:])) for x in data]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
