from aoc import *

sys.setrecursionlimit(10000)

mirrors = {
    '/': {0: (1,), 1: (0,), 2: (3,), 3: (2,)},
    '\\': {0: (3,), 1: (2,), 2: (1,), 3: (0,)},
    '|': {0: (1, 3), 2: (1, 3)},
    '-': {1: (0, 2), 3: (0, 2)}
}

r_beam_dp = {}
def r_beam(coord, heading, seen):
    # print(coord, heading)
    if (coord, heading) in r_beam_dp:
        return r_beam_dp[(coord, heading)]

    if (coord, heading) in seen:
        return {(coord, heading)}

    tile = grid[coord]

    next_seen = seen.union({(coord, heading)})

    next_beams = []
    if tile in mirrors and heading in mirrors[tile]:
        for new_heading in mirrors[tile][heading]:
            next_beams.append((vadd(coord, DIRS[new_heading]), new_heading))
    else:
        next_beams.append((vadd(coord, DIRS[heading]), heading))

    next_history = {(coord, heading)}
    for next_coord, next_heading in next_beams:
        if next_coord in grid:
            next_history.update(r_beam(next_coord, next_heading, next_seen))

    r_beam_dp[(coord, heading)] = next_history
    # print(r_beam_dp)
    return next_history


def p1(start=None):
    if start is None:
        start = ((0, 0), 0)

    # print('aaa')
    previous = set()
    history = r_beam(*start, previous)
    # print(history)

    flattened = set(k[0] for k in history)
    # print(flattened)
    # print_2d('.', grid, {k:'#' for k in flattened})
    return len(flattened)


def p2():
    highest = (0, 0)
    bounds = grid_bounds(grid)

    edges = [((x,bounds[1]),3) for x in range(bounds[0], bounds[2]+1)] + \
            [((x,bounds[3]),1) for x in range(bounds[0], bounds[2]+1)] + \
            [((bounds[0],y),0) for y in range(bounds[1], bounds[3]+1)] + \
            [((bounds[2],y),2) for y in range(bounds[1], bounds[3]+1)]

    for start in edges:
        result = p1(start)
        if result > highest[0]:
            highest = (result, start)

    return highest[0]


setday(16)

grid, inverse, unique = parsegrid()

dirs = ['>', '^', '<', 'v']


print('part1:', p1())
print('part2:', p2() )
