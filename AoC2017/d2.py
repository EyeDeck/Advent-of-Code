from aoc import *


def p1():
    return sum(abs(min(line) - max(line)) for line in data)


def p2():
    def find_divisible(numbers):
        for a in numbers:
            for b in numbers:
                if a != b and a % b == 0:
                    return a // b

    return sum(find_divisible(line) for line in data)


setday(2)

data = parselines(get_ints)

print('part1:', p1() )
print('part2:', p2() )
