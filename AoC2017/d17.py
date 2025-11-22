from aoc import *


def p1():
    steps = data[0]
    pos = 0
    buffer = [0]
    for i in range(1, 2017+1):
        pos = (pos + steps + 1) % i
        buffer.insert(pos, i)

    return buffer[pos+1]


def p2():
    steps = data[0]
    pos = 0
    leftmost = 0
    for i in range(1, 50000000+1):
        pos = (pos + steps + 1) % i
        if pos == 0:
            leftmost = i

    return leftmost


setday(17)

data = parselines(get_ints)[0]

print('part1:', p1() )
print('part2:', p2() )
