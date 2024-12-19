from aoc import *


def p1():
    return sum(int(data[i]) for i in range(len(data)-1, -2, -1) if data[i] == data[i-1])


def p2():
    return sum(int(data[i]) for i in range(len(data)-1, -2, -1) if data[i] == data[i-len(data)//2])


setday(1)

data = list(parselines()[0])

print('part1:', p1())
print('part2:', p2())
