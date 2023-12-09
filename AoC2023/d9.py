import sys

from aoc import *

def solve():
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    acc = 0
    acc_2 = 0
    for line in data:
        history = [line]
        while True:
            hs = set(history[-1])
            if len(hs) == 1 and hs.pop() == 0:
                break

            last = history[-1]
            new = []
            for i in range(len(last)-1):
                new.append(last[i+1] - last[i])
            history.append(new)
        history[-1].append(0)
        history[-1].insert(0,0)
        for i in range(len(history)-2, -1, -1):
            history[i].append(history[i+1][-1] + history[i][-1])
            history[i].insert(0, history[i][0] - history[i+1][0])
        acc += history[0][-1]
        acc_2 += history[0][0]

        if verbose:
            print('\n')
            for i, ln in enumerate(history):
                print('   ' * i, ln)
    return acc, acc_2

setday(9)

data = [[int(i) for i in line.split()] for line in parselines()]

print('part1: %s\npart2: %s' % solve())
