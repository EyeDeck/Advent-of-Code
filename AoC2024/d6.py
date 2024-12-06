import copy
from aoc import *


def p1():
    dir_map = {'^': (0,-1), '>': (1,0), 'v':(0,1), '<':(-1,0)}
    dir_next = {'^':'>', '>':'v', 'v':'<', '<':'^'}
    p1_grid = copy.deepcopy(grid)
    pos = unique['^']
    heading = '^'
    p1_grid[pos] = '.'
    visited = {pos}
    while True:
        next_tile = vadd(pos, dir_map[heading])
        if next_tile not in grid:
            return len(visited)
        elif grid[next_tile] == '#':
            heading = dir_next[heading]
        else:
            pos = next_tile
            visited.add(pos)

    return None


def p2():
    dir_map = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
    dir_next = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

    acc = 0
    for grid_point, grid_thing in grid.items():
        print(grid_point, acc)
        if grid_thing != '.':
            continue

        p2_grid = copy.deepcopy(grid)
        p2_grid[grid_point] = '#'
        pos = unique['^']
        heading = '^'
        p2_grid[pos] = '.'
        visited = {(heading, pos)}

        while True:
            next_tile = vadd(pos, dir_map[heading])
            if next_tile not in p2_grid:
                break
            elif p2_grid[next_tile] == '#':
                heading = dir_next[heading]
            else:
                pos = next_tile
                to_add = (heading, pos)
                if to_add in visited:
                    print('loop!')
                    acc += 1
                    break
                visited.add(to_add)
                # print(visited)

    return acc


setday(6)


grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
