import copy
import sys
from operator import itemgetter


def solve(board, p2):
    i = 0
    if p2:
        for i in range(-2000, 2000):
            board[i, board['abyss'] + 1] = '#'
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

print('part1:', solve(copy.deepcopy(board), False))
print('part2:', solve(copy.deepcopy(board), True))
