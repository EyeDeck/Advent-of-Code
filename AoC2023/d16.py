from aoc import *

def p1(beams=None):
    if beams is None:
        beams = [(0, 0, 0)]

    history = set()
    dirs = ['>', '^', '<', 'v']

    mirrors = {
        '/':  {0: (1,  ), 1: (0,  ), 2: (3,  ), 3: (2,  )},
        '\\': {0: (3,  ), 1: (2,  ), 2: (1,  ), 3: (0,  )},
        '|':  {0: (1, 3), 2: (1, 3)},
        '-':  {1: (0, 2), 3: (0, 2)}
    }

    while beams:
        new_beams = []
        for beam in beams:
            if beam in history:
                continue
            history.add(beam)

            coord = beam[:2]
            heading = beam[-1]
            tile = grid[coord]

            next_coords = []
            if tile in mirrors and heading in mirrors[tile]:
                for new_heading in mirrors[tile][heading]:
                    next_coords.append(vadd(coord, DIRS[new_heading]) + (new_heading,))
            else:
                next_coords.append(vadd(coord,DIRS[heading]) + (heading,))

            for c in next_coords:
                if c[:2] in grid:
                    new_beams.append(c)

        beams = new_beams

    flattened = set(k[:2] for k in history)
    # print_2d('.', grid, {k[:2]:'#' for k in flattened})
    return len(flattened)


def p2():
    highest = 0
    bounds = grid_bounds(grid)

    edges = [(x,bounds[1],3) for x in range(bounds[0], bounds[2]+1)] + \
            [(x,bounds[3],1) for x in range(bounds[0], bounds[2]+1)] + \
            [(bounds[0],y,0) for y in range(bounds[1], bounds[3]+1)] + \
            [(bounds[2],y,2) for y in range(bounds[1], bounds[3]+1)]

    for start in edges:
        highest = max(highest, p1([start]))

    return highest


setday(16)

grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
