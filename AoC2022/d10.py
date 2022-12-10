import time

from aoc import *


def p1():
    cycles = {20, 60, 100, 140, 180, 220}
    x = 1
    cycle = 1
    acc = 0
    for line in data:
        if cycle in cycles:
            acc += x * cycle

        if line[0] == 'noop':
            pass
        elif line[0] == 'addx':
            cycle += 1

            if cycle in cycles:
                acc += x * cycle

            x += line[1]
        cycle += 1
    return acc


def p2():
    screen = {(0, 0): '<', (39, 5): '>'}
    x = 1
    cycle = 1
    for line in data:
        process(screen, cycle, x)

        if line[0] == 'noop':
            pass
        elif line[0] == 'addx':
            cycle += 1

            process(screen, cycle, x)
            x += line[1]
        cycle += 1

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

animate = '-a' or '--animate' in sys.argv
if animate:
    print('\033c \033[0;0H', end='')  # clear screen and set cursor to 0,0

with open(f) as file:
    data = [[int(word) if word.lstrip("-").isnumeric() else word for word in line.strip().split()] for line in file]

print(f'part1: {p1()}')
print('part2:')
p2()
