from aoc import *


def p1():
    return len(bfs(source, destination, neighbors)) - 1


def p2():
    srcs = [k for k, v in board.items() if v == 'a' and ('b' in [board[n] for n in neighbors[k]])]
    # print_2d('.', {k: 'a' for k in srcs})
    return min([len(bfs(s, destination, neighbors)) - 1 for s in srcs])


def get_neighbors(c):
    x, y = c
    adjacent = []
    for xm, ym in DIRS:
        adj = (x + xm, y + ym)
        if adj not in board:
            continue
        if ord(board[c]) + 1 >= ord(board[adj]):
            adjacent.append(adj)
    return adjacent


day = 12
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

board = {}
with open(f) as file:
    for y, line in enumerate(file.readlines()):
        for x, c in enumerate(line.strip()):
            board[x, y] = c
            if c == 'S':
                board[x, y] = 'a'
                source = (x, y)
            elif c == 'E':
                board[x, y] = 'z'
                destination = (x, y)

neighbors = {c: get_neighbors(c) for c in board}

print(f'part1: {p1()}')
print(f'part2: {p2()}')
