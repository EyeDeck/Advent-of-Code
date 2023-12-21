from aoc import *

def solve():
    _, _, w, h = grid_bounds(grid)
    w += 1
    h += 1

    cycle_len = 26501365 // w

    tiles = {unique['S']}
    visited, visited_alt = set(), set()

    steps = []

    step = 1
    while len(steps) < 3:
        new_tiles = set()
        while tiles:
            tile = tiles.pop()
            for dir in DIRS:
                neighbor = vadd(tile, dir)
                if neighbor in visited:
                    continue
                if grid[(neighbor[0] % w, neighbor[1] % h)] != '#':
                    new_tiles.add(neighbor)
                    visited.add(neighbor)
        tiles = new_tiles

        if step == 64:
            p1 = len(visited)

        if (step % w) == 65:
            steps.append(len(visited))
            print(step)
            # print(steps)

        visited, visited_alt = visited_alt, visited
        step += 1

        # print_2d(' ', grid, {k:'~' for k in visited}, {k:'@' for k in tiles}, constrain=(-1000, -1000, 1000, 1000))
        # input()

    # I still only have an extremely vague idea why this works
    diff0 = steps[0]
    diff1 = steps[1] - steps[0]
    diff2 = steps[2] - steps[1]
    return p1, diff0 + diff1 * cycle_len + (cycle_len * (cycle_len - 1) // 2) * (diff2 - diff1)

setday(21)

grid, inverse, unique = parsegrid()

print('part1: %s\npart2: %s' % solve())
