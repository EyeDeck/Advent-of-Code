import sys
from operator import itemgetter
from aoc import *


def getneighbors(x, y, grid, bg):
    n = []
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            n.append(grid[i, j] if (i, j) in grid else bg)
    return int(''.join(['0' if c == '.' else '1' for c in n]), 2)


def step(grid, bg):
    newgrid = {}
    points = grid.keys()
    bounds = min(points, key=itemgetter(0))[0] - 1, min(points, key=itemgetter(1))[1] - 1, \
             max(points, key=itemgetter(0))[0] + 2, max(points, key=itemgetter(1))[1] + 2
    for x in range(bounds[0], bounds[2]):
        for y in range(bounds[1], bounds[3]):
            index = getneighbors(x, y, grid, bg)
            char = algo[index]
            if char == bg:
                newgrid[x, y] = char

    return newgrid


def step_n(grid, n):
    working = grid.copy()
    first, last = algo[0], algo[511]
    for i in range(n):
        working = step(working, first if i & 1 else last)
        if '--render' in sys.argv:
            print_2d(last if i & 1 else first, working)
    return len([c for c in working.values() if c == '#'])


day = 20
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    algo, rawgrid = file.read().split('\n\n')
    grid = {}
    for y, line in enumerate(rawgrid.split('\n')):
        for x, c in enumerate(line.strip()):
            grid[x, y] = c

print(f'part1: {step_n(grid, 2)}')
print(f'part2: {step_n(grid, 50)}')
