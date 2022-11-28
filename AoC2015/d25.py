from aoc import *


def p1():
    last = 20151125
    x, y = 1, 1
    while True:
        y -= 1
        x += 1
        if y < 1:
            y = x
            x = 1
        last = last * 252533 % 33554393
        if y == data[0] and x == data[1]:
            return last


day = 25
if len(sys.argv) > 2:
    data = [int(i) for i in sys.argv[1:]]
else:
    data = [2978, 3083]
    print(f'Usage: {sys.argv[0]} row column; using hardcoded values of {data}')

print(f'part1: {p1()}')
