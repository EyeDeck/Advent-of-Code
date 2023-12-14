import copy

from aoc import *

def rock(grid, width, height):
    for n in range(height):
        for x in range(width + 1):
            for y in range(1, height + 1):
                if grid[x, y] == 'O' and grid[x, y - 1] == '.':
                    grid[x, y] = '.'
                    grid[x, y - 1] = 'O'
    return grid

def p1():
    g = copy.deepcopy(grid)

    _, _, width, height = grid_bounds(grid)
    g = rock(g, width, height)

    acc = 0
    for k,v in g.items():
        if v == 'O':
            acc += height-k[1]+1

    print_2d(' ', g)
    return acc

def spin(grid, width, height):
    for _ in range(4):
        grid = rock(grid, width, height)
        grid = rotate_2d(grid, 90, True, width, height)
    return grid


def p2():
    g = copy.deepcopy(grid)

    _, _, width, height = grid_bounds(g)

    seen = {}
    for i in range(1000000000):
        print('\n', i)
        g = spin(g, width, height)
        print_2d(' ', g)
        hashable = str(g)
        if hashable in seen.keys():
            last, weight = seen[hashable]
            cycle_len = i - last
            print('at cycle', i, 'last seen', last, 'cycle len', cycle_len)
            print(1000000000 % cycle_len)
            print(seen.values())
            ans = [x for x in seen.values()][((1000000000 - last) % cycle_len) + last -1]
            return ans

        acc = 0
        for k, v in g.items():
            if v == 'O':
                acc += height - k[1] + 1

        seen[hashable] = (i, acc)
    print(seen)

# not 102837
# not 102851
# 102829!

setday(14)

grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
