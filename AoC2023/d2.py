import math

from aoc import *

def solve():
    target = {'red': 12, 'green': 13, 'blue': 14}

    acc_1 = 0
    acc_2 = 0
    for line in data:
        minimums = defaultdict(int)

        game, sets = line.split(':')
        sets = [[x.strip() for x in s.strip().split(',')] for s in sets.split(';')]
        for cubes in sets:
            for cube in cubes:
                ct, color = cube.split()
                ct = int(ct)
                minimums[color] = max(minimums[color], ct)

        for k,v in minimums.items():
            if k not in target or v > target[k]:
                break
        else:
            acc_1 += int(game.split()[-1])

        acc_2 += math.prod(minimums[k] for k in target.keys())
    return acc_1, acc_2


setday(2)

data = parselines()

print('part1: %s\npart2: %s' % solve())
