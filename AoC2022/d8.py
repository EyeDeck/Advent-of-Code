from aoc import *


def p1():
    found = {}

    for (x,y), v in board.items():

        if check_vis(board, x, y):
            found[x,y] = v

    # print_2d('. ', found)

    return len(found)


def check_vis(board, x, y):
    this_tree = board[x,y]
    for dir in DIRS:
        xmod = dir[0]
        ymod = dir[1]
        nx, ny = x+xmod, y+ymod
        tallest = -1
        while (nx, ny) in board and x >= 0 and y >= 0:
            # print(board[x, y])
            tallest = max(tallest, board[nx,ny])
            nx += xmod
            ny += ymod
        if tallest < this_tree:
            return True


def p2():
    return max( [count_vis(board, x, y) for x,y in board.keys()]  )


def count_vis(board, x, y):
    # print(x,y)
    this_tree = board[x,y]
    score = 1
    for dir in DIRS:
        xmod = dir[0]
        ymod = dir[1]
        nx, ny = x+xmod, y+ymod
        i = 0
        while (nx, ny) in board and x >= 0 and y >= 0:
            i += 1
            if board[nx,ny] < this_tree:
                nx += xmod
                ny += ymod
            else:
                break
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
            board[x,y] = int(c)

w, h = max(board.keys(), key=itemgetter(0))[0],  max(board.keys(), key=itemgetter(1))[1]

# print_2d('.', board)


print(f'part1: {p1()}')
print(f'part2: {p2()}')
