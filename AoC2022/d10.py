import time

from aoc import *


def p1():
    cycles = {20, 60, 100, 140, 180, 220}
    x = 1
    acc = 0
    for cycle, op in enumerate(data, start=1):
        if cycle in cycles:
            acc += x * cycle

        if op[0] == 'noop':
            pass
        elif op[0] == 'addx':
            x += op[1]
    return acc


def p2():
    screen = {(0, 0): '<', (39, 5): '>'}
    x = 1
    for cycle, op in enumerate(data, start=1):
        process(screen, cycle, x)

        if op[0] == 'noop':
            pass
        elif op[0] == 'addx':
            x += op[1]

    print_2d('.', screen)


def process(screen, cycle, x):
    cycle -= 1

    scan_x, scan_y = cycle % 40, cycle // 40
    nx = '#' if scan_x in range(x - 1, x + 2) else '.'
    screen[scan_x, scan_y] = nx
    if animate:
        print_2d('.', screen, {(x - 1, scan_y): '-', (x, scan_y): '=', (x + 1, scan_y): '-',
                               (scan_x, scan_y): '+' if nx == '#' else '|'}, constrain=(0, 0, 39, 6))
        print('\033[2;0H')  # reset cursor to 2,0 (y,x for some reason)
        time.sleep(0.066)


day = 10
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

animate = ('-a' or '--animate') in sys.argv
if animate:
    print('\033c \033[0;0H', end='')  # clear screen and set cursor to 0,0

with open(f) as file:
    data = file.read().replace('addx', 'noop\naddx').split('\n')
    data = [[int(word) if word.lstrip("-").isnumeric() else word for word in line.strip().split()] for line in data]

print(f'part1: {p1()}')
print('part2:')
p2()
