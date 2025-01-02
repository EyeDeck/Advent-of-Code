import functools

from aoc import *


def rounds(lengths, ct):
    x = [i for i in range(LENGTH)]
    skip = 0
    pos = 0
    for _ in range(ct):
        for n in lengths:
            for i in range(n // 2):
                a = (pos + i) % LENGTH
                b = (pos + n - i - 1) % LENGTH
                x[a], x[b] = x[b], x[a]
                # print(f'\t swapped {a} and {b} producing {x}')
            pos = (pos + n + skip) % LENGTH
            skip += 1
    return x


def p1():
    lengths = get_ints(data)
    x = rounds(lengths, 1)
    return x[0] * x[1]


def p2():
    lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]
    x = rounds(lengths, 64)
    dense = [functools.reduce(lambda a, b: a ^ b, x[n:n + 16]) for n in range(0, 256, 16)]
    hex_str = ''.join(f'{n:02x}' for n in dense)
    assert len(hex_str) == 32
    return hex_str


setday(10)

with open_default() as file:
    data = file.read()

LENGTH = 256

print('part1:', p1())
print('part2:', p2())
