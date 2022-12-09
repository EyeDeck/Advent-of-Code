from aoc import *


def p1():
    found = {}
    for (x, y), v in board.items():
        if check_vis(board, x, y):
            found[x, y] = v
    # print_2d('. ', found)
    print_2d_repl('  ', [found, {i: '/\\' for i in range(0, 10)}])

    return len(found)


def check_vis(board, x, y):
    this_tree = board[x, y]
    for xmod, ymod in DIRS:
        nx, ny = x + xmod, y + ymod
        tallest = -1
        while (nx, ny) in board:
            tallest = max(tallest, board[nx, ny])
            nx += xmod
            ny += ymod
        if tallest < this_tree:
            return True


def p2():
    return max([count_vis(board, x, y) for x, y in board.keys()])


def count_vis(board, x, y):
    this_tree = board[x, y]
    score = 1
    for xmod, ymod in DIRS:
        nx, ny = x + xmod, y + ymod
        i = 0
        while (nx, ny) in board and x >= 0 and y >= 0:
            i += 1
            if board[nx, ny] >= this_tree:
                break
            nx += xmod
            ny += ymod
        score *= i
    return score


day = 8
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

board = {}
with open(f) as file:
    for y, line in enumerate(file.readlines()):
        for x, c in enumerate(line.strip()):
            board[x, y] = int(c)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
