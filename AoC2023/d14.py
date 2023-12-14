import copy

from aoc import *

def rock(r, w):
    for x, y in sorted(r):
        y2 = y
        while y2 > 0 and (x,y2-1) not in r and (x,y2-1) not in w:
            y2 -= 1
        r.remove((x,y))
        r.add((x,y2))
        # print(x,y,'->',x,y2)
    return r

def p1():
    r = copy.deepcopy(rocks)
    # print_2d('.', {k:'#' for k in walls}, {k:'O' for k in r})
    r = rock(r, walls)

    acc = 0
    for k in r:
        acc += height-k[1]+1

    # print_2d('.', {k:'#' for k in walls}, {k:'O' for k in r})
    return acc

def p2():
    r = copy.deepcopy(rocks)
    w = copy.deepcopy(walls)

    seen = {}
    for i in range(1000000000):
        for _ in range(4):
            r = rock(r, w)
            # print('\n', i, _)
            # print_2d('.', {k: '#' for k in w}, {k: 'O' for k in r})
            r = rotate_2d(r, 90, True, width, height)
            w = rotate_2d(w, 90, True, width, height)

        hashable = (frozenset(r), frozenset(w))

        if hashable in seen.keys():
            last, weight = seen[hashable]
            cycle_len = i - last
            ans = [v for v in seen.values()][((1000000000 - last) % cycle_len) + last -1]
            return ans[1]

        acc = 0
        for k in r:
            acc += height - k[1] + 1

        seen[hashable] = (i, acc)

setday(14)

grid, inverse, unique = parsegrid()
_, _, width, height = grid_bounds(grid)
walls = set()
rocks = set()
for k, v in grid.items():
    if v == '#':
        walls.add(k)
    elif v == 'O':
        rocks.add(k)


print('part1:', p1() )
print('part2:', p2() )
