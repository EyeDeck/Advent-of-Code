import sys
from aoc import *


def step(board):
    next_board = board.copy()
    # print_2d(' ', next_board)
    for (x, y), c in board.items():
        if c != '>':
            continue
        n = (x + 1, y)
        if n not in board:
            n = (0, y)
        if board[n] == '.':
            next_board[n] = c
            next_board[x, y] = '.'

    board = next_board
    # print_2d(' ', board)

    next_board = board.copy()
    for (x, y), c in board.items():
        if c != 'v':
            continue

        n = (x, y + 1)
        if n not in board:
            n = (x, 0)
        if board[n] == '.':
            next_board[n] = c
            next_board[x, y] = '.'
    return next_board


def p1():
    seen = set()
    board = data.copy()
    i = 0
    #print_2d(' ', board)
    while True:
        # print(' ')
        i += 1
        board = step(board)
        #print_2d(' ', board)
        as_str = str(sorted(board.items()))
        # print(as_str)
        if as_str in seen:
            return i
        seen.add(as_str)


def p2():
    return None


day = 25
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = {}
    for y, line in enumerate(file.read().strip().split('\n')):
        for x, c in enumerate(line):
            data[x, y] = c
    # print(data)
    # data = [line.strip() for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
