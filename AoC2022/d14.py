import copy
import sys
from operator import itemgetter
from aoc import print_2d


def p1(board):
    i = 0
    while step(board):
        i += 1
        # print_2d('.', board, constrain=(-9999, -9999, 9999, 9999))
    return i


step_order = [
    lambda x, y: (x, y + 1),
    lambda x, y: (x - 1, y + 1),
    lambda x, y: (x + 1, y + 1)
]


def step(board):
    x, y = 500, 0
    if (x, y) in board:
        return False
    while True:
        for func in step_order:
            n = func(x, y)
            if n not in board:
                x, y = n
                break
        else:
            board[x, y] = 'o'
            return True
        if y > board['abyss']:
            return False


def p2(board):
    abyss = board['abyss']
    for i in range(-abyss-1, abyss+2):
        board[500+i, (abyss + 1)] = '#'
    front = {(500, 0)}
    acc = 0
    while front:
        c = front.pop()
        board[c] = 'o'
        acc += 1
        front.update(d for d in (f(*c) for f in step_order) if d not in board)

        if acc % 50 == 0:
            print('\033[2;0H')
            print_2d('  ', board, {k: '.' for k in front}, constrain=(-9999, -9999, 9999, 9999))
    return acc


day = 14
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    board = {}
    for line in [[tuple(int(i) for i in coord.split(',')) for coord in line.strip().split(' -> ')] for line in file]:
        for i in range(len(line) - 1):
            [x1, y1], [x2, y2] = line[i], line[i + 1]
            if x1 == x2:
                y1, y2 = sorted([y1, y2])
                for y in range(y1, y2 + 1):
                    board[x1, y] = '#'
            elif y1 == y2:
                x1, x2 = sorted([x1, x2])
                for x in range(x1, x2 + 1):
                    board[x, y1] = '#'
            else:
                raise Exception('bad input?')
    board['abyss'] = max(board.keys(), key=itemgetter(1))[1] + 1

print('part1:', p1(copy.deepcopy(board)))
print('part2:', p2(copy.deepcopy(board)))
