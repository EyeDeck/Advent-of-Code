import math
from aoc import *

def p1():
    def has_symbol():
        for x in range(bb[0][0], bb[1][0] + 1):
            for y in range(bb[0][1], bb[1][1] + 1):
                if (x,y) not in grid:
                    continue
                adj = grid[(x,y)]
                if adj != '.' and not adj.isnumeric():
                    return True
        return False

    acc = 0
    for k,v in grid.items():
        if v == '.':
            continue

        to_left = vadd(k, (-1,0))
        if v.isnumeric() and (to_left in grid and not grid[to_left].isnumeric()) or (to_left not in grid):
            coord = k
            num_str = ''
            while coord in grid and grid[coord].isnumeric():
                num_str += grid[coord]
                coord = vadd(coord, (1,0))

            bb = (vadd(k, (-1,-1)), vadd(coord, (0,1)))

            if has_symbol():
                acc += int(num_str)
    return acc

# this is hideous but I just don't care enough to fix it
def p2():
    acc = 0
    for k,v in grid.items():
        if v != '*':
            continue
        numeric = {}

        bb = (vadd(k, (-1,-1)), vadd(k, (1,1)))
        for x in range(bb[0][0], bb[1][0] + 1):
            for y in range(bb[0][1], bb[1][1] + 1):
                if (x,y) in grid and grid[x,y].isnumeric():
                    numeric[(x,y)] = grid[x,y]

        seen = set()
        adj_numbers = []
        for k,v in numeric.items():
            if k in seen:
                continue

            while k in grid and grid[k].isnumeric():
                k = vadd(k, (-1,0))

            num_str = ''
            k = vadd(k, (1, 0))
            while k in grid and grid[k].isnumeric():
                seen.add(k)
                num_str += grid[k]
                k = vadd(k, (1,0))

            adj_numbers.append(int(num_str))

        if len(adj_numbers) == 2:
            acc += math.prod(adj_numbers)

    return acc


setday(3)

grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
