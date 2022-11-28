from collections import defaultdict
from aoc import *


dirmap = {
    'e': HEXDIRS[0],
    'se': HEXDIRS[1],
    'sw': HEXDIRS[2],
    'w': HEXDIRS[3],
    'nw': HEXDIRS[4],
    'ne': HEXDIRS[5],
}


def p1():
    global tiles
    tiles = set()
    for line in data:
        steps = re.findall('(e|se|sw|w|nw|ne)', line)
        coords = (0, 0, 0)
        for step in steps:
            coords = vadd(coords, dirmap[step])
        if coords in tiles:
            tiles.remove(coords)
        else:
            tiles.add(coords)

    return len(tiles)


def get_neighbors(tile, bd, get_all=False):
    neighbors = set()
    for x in HEXDIRS:
        c = vadd(tile, x)
        if get_all or c in bd:
            neighbors.add(c)
    return neighbors


def step(bd):
    new_board = bd.copy()
    to_tick = set()
    for cell in bd:
        for c2 in get_neighbors(cell, bd, True):
            to_tick.update(get_neighbors(c2, bd, True))
    for cell in to_tick:
        n_ct = len(get_neighbors(cell, bd))
        if cell in bd:
            if n_ct == 0 or n_ct > 2:
                new_board.remove(cell)
        else:
            if n_ct == 2:
                new_board.add(cell)
    return new_board


def p2():
    running = tiles

    for i in range(0, 100):
        running = step(running)

    return len(running)


tiles = None

f = 'dx.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
