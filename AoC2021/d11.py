from collections import *
from aoc import *


def getneighbors(c, b):
    r = []
    for d in DIAGDIRS:
        dr = (d[0] + c[0], d[1] + c[1])
        if dr in b:
            r.append(dr)
    return r


def flashtopuses(b, flashed):
    changed = False
    for coord, level in b.items():
        if level > maxstate and not flashed[coord]:
            changed = True
            flashed[coord] = True
            neighbors = getneighbors(coord, b)
            for n in neighbors:
                b[n] += 1
    for coord, f in flashed.items():
        if f:
            b[coord] = 0
    if not changed:
        return flashed
    else:
        return flashtopuses(b, flashed)


def process(b):
    p1 = 0
    p2 = 0
    i = 0
    while True:
        i += 1
        flashed = defaultdict(bool)
        b = {k: v + 1 for k, v in b.items()}
        after_flash = flashtopuses(b, flashed)
        flashed_ct = len([x for x in after_flash.values() if x])

        print(f'\n{i}')
        # print_2d('  ', b)
        # print_2d('     ', b, after_flash)
        # print_2d_repl('  ', [b, {}], [after_flash, {True: '*'}])
        print_2d_repl('  ', [b, {0:' ', 1:' ', 2:'.', 3:',', 4:'o', 5:'O', 6:'@', 7:'░', 8:'▒', 9:'▓', }], [after_flash, {True: '█'}])

        if i < 100:
            p1 += flashed_ct
        if flashed_ct == len(board):
            p2 = i
        if i >= 100 and p2:
            return p1, p2


day = 11
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

maxstate = 9
if len(sys.argv) >= 5:
    maxstate = int(sys.argv[4])

board = {}
if f == 'random':
    from random import randint
    xlen, ylen = int(sys.argv[2]), int(sys.argv[3])
    for x in range(xlen):
        for y in range(ylen):
            board[x,y] = randint(0,maxstate)
else:
    with open(f) as file:
        data = [line.strip() for line in file]

    for x, line in enumerate(data):
        for y, n in enumerate(line):
            board[(x, y)] = int(n)



solutions = process(board)
print(f'part1: {solutions[0]}')
print(f'part2: {solutions[1]}')
