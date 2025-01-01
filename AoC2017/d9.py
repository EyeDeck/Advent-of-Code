from aoc import *


def solve():
    stack = 0
    garbage = False
    cancel = False
    score = 0
    count = 0
    for c in data:
        if garbage:
            if cancel:
                cancel = False
            elif c == '!':
                cancel = True
            elif c == '>':
                garbage = False
            else:
                count += 1
        elif c == '<':
            garbage = True
        elif c == '{':
            stack += 1
        elif c == '}':
            score += stack
            stack -= 1
    return score, count


setday(9)

data = parselines()[0]

print('part1: %d\npart2: %d' % solve())
