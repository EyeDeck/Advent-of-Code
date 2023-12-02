import math

from aoc import *

def is_valid(sets):
    target = {'red': 12, 'green': 13, 'blue': 14}
    for cubes in sets:
        for cube in cubes:
            ct, color = cube.split()
            ct = int(ct)
            # print(color, ct)
            if color not in target:
                return False
            if ct > target[color]:
                return False
    return True


def p1():
    acc = 0

    for line in data:
        game, sets = line.split(':')
        sets = [[x.strip() for x in s.strip().split(',')] for s in sets.split(';')]
        # print(game)
        if is_valid(sets):
            acc += int(game.split()[-1])
        # l = [word.strip().strip(',') for word in line.split()]
        # print(l)
    return acc


def p2():
    acc = 0
    for line in data:
        minimums = defaultdict(int)
        game, sets = line.split(':')
        sets = [[x.strip() for x in s.strip().split(',')] for s in sets.split(';')]
        for cubes in sets:
            for cube in cubes:
                ct, color = cube.split()
                ct = int(ct)
                minimums[color] = max(minimums[color], ct)
        print(minimums)
        acc += math.prod(minimums.values())
    return acc


setday(2)

data = parselines()

print('part1:', p1() )
print('part2:', p2() )
