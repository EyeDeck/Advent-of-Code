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

            if tile in all_doors and tile.lower() not in keys:
                continue

            neighbors[neighbor] = tile

        return neighbors

    q = {(start, start, frozenset()): 0}
    best = {}

    while True:
        if not q:
            return None

        next_q = {}

        while q:
            first = next(iter(q))
            pos, last, keys = first
            steps = q.pop(first)

            for coord, tile in get_neighbors(grid, pos, keys).items():
                if coord == last:
                    continue

                if tile in all_keys:
                    next_keys = frozenset(keys | {tile})
                    last_coord = coord
                else:
                    next_keys = keys
                    last_coord = pos

                if next_keys == all_keys:
                    return steps + 1

                next_key = (coord, last_coord, next_keys)
                next_steps = steps + 1
                if next_key in best and best[next_key] < next_steps:
                    continue

                if next_key in next_q and next_q[next_key] < next_steps:
                    continue

                next_q[next_key] = next_steps
                best[next_key] = next_steps

            q = next_q


def p1():
    return solve(grid, ALL_KEYS, ALL_DOORS, unique['@'])


def p2():
    def cut_quad(grid, keys, doors, ul, br):
        new_grid = {}
        new_keys = set()
        new_doors = set()
        top_x, top_y = ul
        bot_x, bot_y = br
        for (x, y), tile in grid.items():
            if not top_x <= x <= bot_x or not top_y <= y <= bot_y:
                continue
            new_grid[x, y] = tile
            if tile in keys:
                new_keys.add(tile)
            if tile in doors:
                new_doors.add(tile)

        for c, tile in new_grid.items():
            if tile in new_doors and tile.lower() not in new_keys:
                new_grid[c] = '.'
                new_doors.remove(tile)

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
        acc += solve(*cut_quad(grid, ALL_KEYS, ALL_DOORS, *quad), start)

    return acc


setday(18)

grid, inverse, unique = parsegrid()

ALL_KEYS = unique.keys() & set(string.ascii_lowercase)
ALL_DOORS = unique.keys() & set(string.ascii_uppercase)

print('part1:', p1())
print('part2:', p2())
