import sys
from aoc import *


def p1():
    x, y = 0, 0
    heading = 90
    for line in data:
        a = line[0]
        amt = line[1]
        if a == 'N':
            y += amt
        elif a == 'S':
            y -= amt
        elif a == 'E':
            x += amt
        elif a == 'W':
            x -= amt
        elif a == 'L':
            heading -= amt
            heading %= 360
        elif a == 'R':
            heading += amt
            heading %= 360
        elif a == 'F':
            if heading == 0:
                y += amt
            elif heading == 90:
                x += amt
            elif heading == 180:
                y -= amt
            elif heading == 270:
                x -= amt
    return abs(x) + abs(y)


def p2():
    x, y = 0, 0
    w_x, w_y = 10, 1
    for line in data:
        a = line[0]
        amt = line[1]
        if a == 'N':
            w_y += amt
        elif a == 'S':
            w_y -= amt
        elif a == 'E':
            w_x += amt
        elif a == 'W':
            w_x -= amt
        elif a == 'L' or a == 'R':
            w_x, w_y = rotate_point_around_origin(w_x, w_y, 0, 0, amt, True if a == 'R' else False)
        elif a == 'F':
            x += w_x * amt
            y += w_y * amt
        else:
            die('bad op')
    return abs(x) + abs(y)


f = 'd12.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]
    data = [(line[0], int(line[1:])) for line in data]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
