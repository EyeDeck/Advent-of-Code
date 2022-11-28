from aoc import *


def simpath(keypad):
    x, y = 1, 1
    code = []
    for line in data:
        for c in line:
            nx = x + dir[c][0]
            ny = y + dir[c][1]
            if (nx,ny) in keypad:
                x, y = nx, ny
        code.append(keypad[x, y])
    return ''.join([str(c) for c in code])


def p1():
    return simpath(keypad_p1)


def p2():
    return simpath(keypad_p2)


day = 2
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

keypad_p1 = {(0, 0): 1, (1, 0): 2, (2, 0): 3, (0, 1): 4, (1, 1): 5, (2, 1): 6, (0, 2): 7, (1, 2): 8, (2, 2): 9}
keypad_p2 = {(2, 0): 1, (1,1): 2, (2,1): 3, (3,1): 4, (0,2): 5, (1,2): 6, (2,2): 7, (3, 2): 8, (4,2): 9, (1,3):'A', (2,3):'B', (3,3):'C', (2,4):'D'}
dir = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
