import sys
from aoc import *


def step(board, bounds=None):
    to_tick = set()
    for tile, state in board.items():
        for d in DIAGDIRS:
            n = vadd(tile, d)
            if not bounds or (bounds[0] <= n[0] <= bounds[2] and bounds[1] <= n[1] <= bounds[3]):
                to_tick.add(n)
            to_tick.add(tile)
    nxt = {}
    # print_2d('.', board)
    # print_2d('.', board, {k:'@' for k in to_tick})
    for tile in to_tick:
        ct = 0
        for d in DIAGDIRS:
            if vadd(tile, d) in board:
                ct += 1
        if tile in board:
            if ct == 2 or ct == 3:
                nxt[tile] = '#'
        else:
            if ct == 3:
                nxt[tile] = '#'
    return nxt


def p1():
    bounds = [0, 0, max(x[0] for x in data), max(y[1] for y in data)]
    board = data.copy()
    for i in range(100):
        board = step(board, bounds)
    return len(board)


def activate_corners(board, bounds):
    board[0, 0] = '#'
    board[bounds[2], 0] = '#'
    board[0, bounds[3]] = '#'
    board[bounds[2], bounds[3]] = '#'


def p2():
    bounds = [0, 0, max(x[0] for x in data), max(y[1] for y in data)]
    board = data.copy()
    activate_corners(board, bounds)

    for i in range(100):
        board = step(board, bounds)
        activate_corners(board, bounds)

    return len(board)


day = 18
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

data = {}
with open(f) as file:
    for y, line in enumerate(file):
        for x, c in enumerate(line):
            if c == '#':
                data[x, y] = c
# print_2d('.', data)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
