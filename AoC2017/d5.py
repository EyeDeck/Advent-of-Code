from aoc import *


def solve(p2):
    jumps = data.copy()
    pointer = 0
    i = 0
    while pointer < len(jumps):
        i += 1
        offset = jumps[pointer]
        jumps[pointer] += -1 if p2 and offset >= 3 else 1
        pointer += offset
    return i


setday(5)

data = [line[0] for line in parselines(get_ints)]

print('part1:', solve(False))
print('part2:', solve(True))
