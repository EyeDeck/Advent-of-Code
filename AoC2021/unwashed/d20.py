import sys

from aoc import *


def getneighbors(x,y,grid,bg):
    n = []
    for j in range(y-1,y+2):
        for i in range(x-1,x+2):
            point = grid[i,j] if (i,j) in grid else bg
            # print(i,j, point)
            n.append(point)
    return toint(n)


def toint(n):
    return int(''.join(['0' if c == '.' else '1' for c in n]), 2)


def step(grid,bg):
    newgrid = {}
    points = grid.keys()
    # minx, miny, maxx, maxy
    # bounds = min(points, key=itemgetter(0))[0], min(points, key=itemgetter(1))[1], max(points, key=itemgetter(0))[0], max(points, key=itemgetter(1))[1]
    to_tick = set()
    for key in points:
        for x in range(-2,3):
            for y in range(-2,3):
                to_tick.add((key[0]+x, key[1]+y))
    # print(bounds)
    # for x in range(bounds[0]-5,bounds[2]+5):
    #     for y in range(bounds[1]-5,bounds[3]+5):
    #         index = getneighbors(x, y, grid)
    #         newgrid[x, y] = algo[index]
    for x,y in to_tick:
        index = getneighbors(x, y, grid, bg)
        newgrid[x, y] = algo[index]

    # for (x,y), c in grid.items():

        # print(index)

    return newgrid

def p1():
    #for line in data:
    #    print(line)
    working = grid.copy()
    # print_2d(' ', grid)
    for i in range(2):
        bg = '.' if i % 2 == 0 else '#'
        # bg = '#' if i % 2 == 0 else '.'
        working = step(working, bg)
        print_2d(' ', working)
    return len([c for c in working.values() if c == '#'])


def p2():
    # for line in data:
    #    print(line)
    working = grid.copy()
    # print_2d(' ', grid)
    for i in range(50):
        bg = '.' if i % 2 == 0 else '#'
        # bg = '#' if i % 2 == 0 else '.'
        working = step(working, bg)
        print_2d(' ', working)
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
            grid[x,y] = c
    # lookup = []
    # print(algo, grid)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
