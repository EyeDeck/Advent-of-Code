from aoc import *


def solve():
    neighbors = {0: '-', 1: '|', 2: '-', 3: '|'}

    pos = min(inverse['|'], key=lambda x: x[1])
    collected = []
    heading = 3
    i = 0
    while True:
        i += 1
        c = grid[pos]
        if c.isalpha():
            collected.append(c)
        elif c == '+':
            for h, tile in neighbors.items():
                if h == (heading + 2) % 4:
                    continue
                adj_pos = vadd(pos, DIRS[h])
                if adj_pos not in grid:
                    continue
                grid_c = grid[adj_pos]
                if grid_c == tile or grid_c.isalpha():
                    heading = h
                    break
        pos = vadd(pos, DIRS[heading])

        if pos not in grid:
            break

        if verbose:
            d_x, d_y = 24, 12  # draw_area
            print_2d(' ', grid, {pos: '@'}, constrain=(vsub(pos, (d_x, d_y)) + vadd(pos, (d_x, d_y) * 2)))

            print(i, collected)
            input()

    return ''.join(collected), i


setday(19)

grid, inverse, unique = parsegrid()
grid = {k: v for k, v in grid.items() if v != ' '}

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1: %s\npart2: %d' % solve())
