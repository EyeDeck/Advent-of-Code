import math
from aoc import *


def simulate(sim_grid, extra, pos, heading):
    old = {}
    for k, v in extra.items():
        old[k] = sim_grid[k]
        sim_grid[k] = v

    visited_states = {(heading, pos)}
    visited_tiles = {pos}

    while True:
        next_tile = vadd(pos, dir_map[heading])
        if next_tile not in sim_grid:
            sim_grid.update(old)
            return len(visited_tiles), visited_tiles
        elif sim_grid[next_tile] == '#':
            heading = dir_next[heading]
        else:
            pos = next_tile
            to_add = (heading, pos)
            if to_add in visited_states:
                sim_grid.update(old)
                return math.inf, visited_tiles
            visited_states.add(to_add)
            visited_tiles.add(pos)


def p1():
    return simulate(grid, {unique['^']: '.'}, unique['^'], '^')


def p2():
    acc = 0
    total_points = len(p1_visited)
    for i, grid_point in enumerate(p1_visited):
        if i % 10 == 0:
            print(f'part2: {acc} ({(i / total_points) * 100:.2f}%)', end='\r')
        r, _ = simulate(grid, {unique['^']: '.', grid_point: '#'}, unique['^'], '^')
        if r == math.inf:
            acc += 1
    sys.stdout.write('\x1b[2K')  # ANSI erase line
    return acc


setday(6)

grid, inverse, unique = parsegrid()

dir_map = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
dir_next = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

p1_result, p1_visited = p1()
p1_visited.remove(unique['^'])

print('part1:', p1_result)
print('part2:', p2())
