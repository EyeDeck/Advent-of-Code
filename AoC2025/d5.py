from aoc import *


def p1():
    def is_in_range(id):
        for l, r in ranges:
            if l <= id <= r:
                return True
        return False

    acc = 0
    for id in available:
        if is_in_range(id):
            acc += 1
    return acc


def p2():
    acc = 0
    for l, r in ranges:
        acc += r-l + 1
    return acc


if __name__ == '__main__':
    setday(5)

    with open_default() as file:
        data = file.read()

    ranges_raw, available_raw = data.split('\n\n')
    ranges = [tuple(int(s) for s in line.split('-')) for line in ranges_raw.split('\n')]
    ranges = merge_ranges(ranges)
    available = [int(line) for line in available_raw.split('\n')]

    print('part1:', p1() )
    print('part2:', p2() )
