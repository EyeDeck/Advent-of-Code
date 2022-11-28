import copy
import sys
from collections import defaultdict


# this function is ugly
from operator import itemgetter


def tick(this_board):
    new = [[0 for _ in range(5)] for _ in range(5)]
    this_mask = 0
    ct = 0
    for y, line in enumerate(this_board):
        for x, c in enumerate(line):
            uldr = (this_board[y][x - 1] if x > 0 else 0,
                    this_board[y - 1][x] if y > 0 else 0,
                    this_board[y][x + 1] if x < board_size[0] - 1 else 0,
                    this_board[y + 1][x] if y < board_size[1] - 1 else 0)
            neighbors = sum(uldr)
            if c == 1 and neighbors != 1:
                next_c = 0
            elif c == 0 and (neighbors == 1 or neighbors == 2):
                next_c = 1
            else:
                next_c = c

            new[y][x] = next_c

            this_mask += next_c << ct
            ct += 1
    return new, this_mask


f = 'd24.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

parsed = [[1 if z == '#' else 0 for z in x.strip()] for x in open(f).readlines()]

board_size = 5, 5

p1_board = copy.deepcopy(parsed)
seen = set()
while True:
    p1_board, mask = tick(p1_board)
    if mask in seen:
        print(f'p1: {mask}')
        break
    seen.add(mask)

p2_board = defaultdict(int)
for y, line in enumerate(parsed):
    for x, c in enumerate(line):
        if c == 1:
            p2_board[x, y, 0] = c


def get_adj(board, x, y, lvl):
    neighbors = {(x - 1, y, lvl), (x, y - 1, lvl), (x + 1, y, lvl), (x, y + 1, lvl)}

    to_add = set()
    for n_x, n_y, _ in neighbors:
        if n_x < 0:
            to_add.add((1, 2, lvl + 1))
        elif n_y < 0:
            to_add.add((2, 1, lvl + 1))
        elif n_x > 4:
            to_add.add((3, 2, lvl + 1))
        elif n_y > 4:
            to_add.add((2, 3, lvl + 1))
        # technically also ought to pop the neighbor from the list here, but fuck it

    neighbors.update(to_add)
    if (2, 2, lvl) in neighbors:
        # add the row or column
        neighbors.remove((2, 2, lvl))
        if (x, y) == (1, 2):
            for axis_n in range(5):
                neighbors.add((0, axis_n, lvl - 1))
        elif (x, y) == (2, 1):
            for axis_n in range(5):
                neighbors.add((axis_n, 0, lvl - 1))
        elif (x, y) == (3, 2):
            for axis_n in range(5):
                neighbors.add((4, axis_n, lvl - 1))
        elif (x, y) == (2, 3):
            for axis_n in range(5):
                neighbors.add((axis_n, 4, lvl - 1))
    total = 0
    # print(f'x {x}, y {y}, lvl {lvl}, neighbors {neighbors}')
    for n in neighbors:
        if board[n] == 1:
            total += 1
    return total


level_min, level_max = 0, 0
for i in range(200):
    p2_new = defaultdict(int)
    for lvl in range(level_min - 1, level_max + 2):
        for x in range(5):
            for y in range(5):
                if (x, y) == (2, 2):
                    continue

                c = p2_board[x, y, lvl]

                neighbors = get_adj(p2_board, x, y, lvl)
                if c == 1 and neighbors != 1:
                    next_c = 0
                elif c == 0 and (neighbors == 1 or neighbors == 2):
                    next_c = 1
                else:
                    next_c = c

                p2_new[x, y, lvl] = next_c

    # level_min = min(p2_new, key=itemgetter(2))[2] - 1
    # level_max = max(p2_new, key=itemgetter(2))[2] + 1
    level_min -= 1
    level_max += 1
    p2_board = p2_new

alive = 0
for cell in p2_board.values():
    if cell == 1:
        alive += 1
print(f'p2: {alive}')
