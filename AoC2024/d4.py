from aoc import *


def p1():
    acc = 0
    marked_grid = set()

    tgt = 'XMAS'
    for coord, char in grid.items():
        if char != 'X':
            continue

        for dir in DIAGDIRS:
            clist = {coord}
            for i, char in enumerate(tgt):
                n_c = vadd(coord, vmul(dir, i))
                if n_c not in grid:
                    break
                if grid[n_c] != char:
                    break
                clist.add(n_c)
            else:
                acc += 1

                marked_grid |= clist

    if verbose:
        print_2d('.', {(0, 0): '.', max(grid.keys()): '.'} | {k: grid[k] for k in marked_grid})
    return acc


def p2():
    acc = 0
    marked_grid = set()

    diag = DIAGDIRS[1::2]

    for coord, char in grid.items():
        if char != 'A':
            continue

        try:
            cross = {k: grid[k] for k in [vadd(coord, c) for c in diag]}
        except KeyError:
            continue

        cross_vals = [k for k in cross.values()]
        if cross_vals.count('M') == 2 and cross_vals.count('S') == 2 and cross_vals[0] != cross_vals[2]:
            acc += 1

            marked_grid |= cross.keys()
            marked_grid.add(coord)

    if verbose:
        print_2d('.', {(0, 0): '.', max(grid.keys()): '.'} | {k: grid[k] for k in marked_grid})
    return acc


setday(4)

grid, inverse, unique = parsegrid()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
