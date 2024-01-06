from aoc import *


def solve(l):
    t = str.maketrans('01', '10')
    a = data

    while len(a) < l:
        a = f'{a}0{a[::-1].translate(t)}'
    checksum = [*a[:l]]

    while len(checksum) & 1 == 0:
        checksum = ['1' if a==b else '0' for a,b in zip(checksum[::2], checksum[1::2])]

    return ''.join(checksum)

setday(16)

data = parselines()[0]

print('part1:', solve(272) )
print('part2:', solve(35651584) )
