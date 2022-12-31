from aoc import *


def solve(grid, all_keys, all_doors, start):
    def get_neighbors(grid, coord, keys):
        neighbors = {}
        for dir in DIRS:
            neighbor = vadd(dir, coord)
            if neighbor not in grid:
                continue

            tile = grid[neighbor]

            if tile == '#':
                continue

            if isinstance(tile, int) and tile < 0 and not -tile & keys:
                continue

            neighbors[neighbor] = tile

        return neighbors

    q = {(start, 0): 0}
    best = {}

    while True:
        if not q:
            return 0

        next_q = {}

        while q:
            first = next(iter(q))
            pos, keys = first
            steps = q.pop(first)

            for coord, tile in get_neighbors(grid, pos, keys).items():
                next_keys = keys
                if isinstance(tile, int) and tile > 0 and not tile & keys:
                    next_keys += tile

                next_steps = steps + 1
                next_key = (coord, next_keys)

                if next_key in best and best[next_key] <= next_steps:
                    continue

                if next_keys == all_keys:
                    return next_steps

                next_q[next_key] = next_steps
                best[next_key] = next_steps

            q = next_q


def p1():
    return solve(grid, KEY_SUM, DOOR_SUM, unique['@'])


def p2():
    def cut_quad(grid, keys, doors, ul, br):
        new_grid = {}
        new_keys = 0
        new_doors = 0
        top_x, top_y = ul
        bot_x, bot_y = br
        for (x, y), tile in grid.items():
            if not top_x <= x <= bot_x or not top_y <= y <= bot_y:
                continue
            new_grid[x, y] = tile
            if isinstance(tile, int):
                if tile > 0:
                    if tile & keys:
                        new_keys += tile
                else:
                    if tile & doors:
                        new_doors += tile

        for c, tile in new_grid.items():
            if isinstance(tile, int) and tile < 0 and not (-tile & new_keys):
                new_grid[c] = '.'
                new_doors -= tile

        return new_grid, new_keys, new_doors

    x, y = unique['@']
    min_x, min_y, max_x, max_y = grid_bounds(grid)

    starts = [
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1),
    ]

    quads = [
        ((min_x, min_y), (x, y)),  # top left (top left to middle)
        ((x, min_y), (max_x, y)),  # top right (top middle to right middle)
        ((min_x, y), (x, max_y)),  # bottom left (left middle to bottom middle)
        ((x, y), (max_x, max_y)),  # bottom right (middle to bottom right)
    ]

    acc = 0
    for start, quad in zip(starts, quads):
        acc += solve(*cut_quad(grid, KEY_SUM, DOOR_SUM, *quad), start)

    return acc


setday(18)

grid, inverse, unique = parsegrid()

ALL_KEYS = {k: v for k, v in unique.items() if k in string.ascii_lowercase}
ALL_DOORS = {k: v for k, v in unique.items() if k in string.ascii_uppercase}

KEY_BITMASKS = {v: 1 << k for k, (v, c) in enumerate(ALL_KEYS.items())}
DOOR_BITMASKS = {v: -1 << k for k, (v, c) in enumerate(ALL_KEYS.items()) if v.lower() in ALL_KEYS}

KEY_SUM = sum(i for i in KEY_BITMASKS.values())
DOOR_SUM = sum(i for i in DOOR_BITMASKS.values())

for key, mask in KEY_BITMASKS.items():
    grid[ALL_KEYS[key]] = mask
    if key.upper() in ALL_DOORS:
        grid[ALL_DOORS[key.upper()]] = -mask

print('part1:', p1())
print('part2:', p2())