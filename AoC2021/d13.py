import sys
from aoc import *


def do_fold(points, axis, n):
    folded = {}
    for (x, y), v in points.items():
        if axis == 'x':
            if x < n:
                folded[(x, y)] = v
            else:
                folded[-x + n * 2, y] = v
        else:
            if y < n:
                folded[(x, y)] = v
            else:
                folded[x, -y + n * 2] = v
    return folded


def p1():
    return len(do_fold(paper, *folds[0]))


def p2():
    render = '--renderall' in sys.argv
    p = paper
    for fold in folds:
        if render:
            print_2d(' ', p)
            print('-------')
        p = do_fold(p, *fold)
    print_2d(' ', p)


day = 13
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    dots, folds = file.read().split('\n\n')

paper = {tuple(int(i) for i in line.strip().split(',')): '#' for line in dots.strip().split('\n')}
folds = [line.strip().split()[-1].split('=') for line in folds.strip().split('\n')]
folds = [[line[0], int(line[1])] for line in folds]

print(f'part1: {p1()}')
print(f'part2:')
p2()
