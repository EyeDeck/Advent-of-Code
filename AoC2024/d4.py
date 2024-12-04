from aoc import *


def p1():
    acc = 0
    print_2d(' ', grid)
    tgt = 'XMAS'
    for coord, char in grid.items():
        if char != 'X':
            continue

        for dir in DIAGDIRS:
            for i, char in enumerate(tgt):
                n_c = vadd(coord, vmul(dir, i))
                # print(coord, dir, i, n_c)
                if n_c not in grid:
                    break
                # print(grid[n_c])
                if grid[n_c] != char:
                    break
            else:
                # print('yes')
                acc += 1

            # print(dir)
    return acc


def p2():
    acc = 0
    marked_grid = {}

    orth = DIAGDIRS[::2]
    diag = DIAGDIRS[1::2]

    for coord, char in grid.items():
        if char != 'A':
            continue

        try:
            crosses = [{k: grid[k] for k in [vadd(coord, c) for c in coordset]} for coordset in [diag]]
            print(crosses)
        except KeyError:
            continue

        for cross in crosses:
            cross_vals = [k for k in cross.values()]
            if cross_vals.count('M') == 2 and cross_vals.count('S') == 2 and cross_vals[0] != cross_vals[2]:
                acc += 1

                marked_grid |= cross
                marked_grid[coord] = 'A'

        # print(orth_chars, diag_chars)
    print_2d('.', marked_grid)
    return acc


setday(4)

grid, inverse, unique = parsegrid()

print('part1:', p1())
print('part2:', p2())
