from aoc import *


def solve():
    screen = {}
    for x in range(50):
        for y in range(6):
            screen[x,y] = False
    for line in data:

        ins = line.strip().split()
        if ins[0] == 'rect':
            w,h = [int(n) for n in ins[1].split('x')]
            for x in range(w):
                for y in range(h):
                    screen[(x,y)] = True
        if ins[0] == 'rotate':
            _,n = ins[2].split('=')
            index = int(n)
            ct = int(ins[-1])
            if ins[1] == 'row':
                to_update = {((k[0]+ct)%50, k[1]):v for k,v in screen.items() if k[1] == index}
            else:
                to_update = {(k[0], (k[1]+ct)%6):v for k,v in screen.items() if k[0] == index}
            screen.update(to_update)

    return screen


def p2():
    return None


setday(8)

data = parselines()

answer = solve()
print('part1:', len([v for v in answer.values() if v == True]) )
print('part2:',)
print_2d('  ', {k:'#' if v == True else ' ' for k,v in answer.items()})