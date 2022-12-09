import math
from aoc import *


def p1():
    board = {(0, 0): 's'}
    h_pos = (0, 0,)
    t_pos = (0, 0,)
    visited = {}
    dirs = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    for line in data:
        for step in range(line[1]):
            # print(line[0], step+1, '/', line[1])
            h_pos = vadd(h_pos, (dirs[line[0]] * line[1]))
            # print(h_pos) #, get_adj(*h_pos))
            if t_pos not in get_adj(*h_pos):
                diff = vsub(t_pos, h_pos)
                # print(diff, adjust(*diff))

                # t_pos = vadd(t_pos, (int(i//2) for i in vsub(h_pos,t_pos)))
                # t_pos = vsub(t_pos, (adjust(i) for i in diff))
                t_pos = vsub(t_pos, adjust(*diff))
            assert t_pos in get_adj(*h_pos) or t_pos == h_pos
            visited[t_pos] = '#'
            # print_2d('. ', visited, board, {h_pos:'H'}, {t_pos:'T'})
            # print_2d('. ', board, {h_pos:'H'}, {t_pos:'T'})
        # print()
        # input()
        # print_2d('. ', visited)
    return len(visited)


def get_adj(x, y):
    return [vadd(i, (x, y,)) for i in DIAGDIRS] + [(x, y)]


def adjust(x, y):
    if x == 0 or y == 0 or (abs(x) == abs(y)):
        return x // 2, y // 2
    if abs(x) > abs(y):
        return x - int(math.copysign(1, x)), y
    else:
        return x, y - int(math.copysign(1, y))


def p2():
    board = {(0, 0): 's'}
    knots = {i: (0, 0) for i in range(10)}
    visited = {}
    dirs = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    for line in data:
        for step in range(line[1]):
            # print(line[0], step+1, '/', line[1])
            knots[0] = vadd(knots[0], (dirs[line[0]] * line[1]))
            for knot, pos in knots.items():
                # print(knot)
                if knot == 0:
                    continue

                if knots[knot] not in get_adj(*knots[knot - 1]):
                    diff = vsub(knots[knot], knots[knot - 1])
                    knots[knot] = vsub(knots[knot], adjust(*diff))
                    # print('moved', knot)
                    # print_2d('. ', {v:k for k,v in reversed(knots.items())})
                visited[knots[9]] = '#'

        # print_2d('. ', visited, {v:k for k,v in knots.items()})
        # input()

    return len(visited)


day = 9
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(word) if word.isnumeric() else word for word in line.split()] for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
