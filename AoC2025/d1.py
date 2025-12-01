from aoc import *


def solve():
    pointer = 50
    acc_p1 = 0
    acc_p2 = 0
    for line in data:
        extra = 0 if pointer == 0 else 1

        pointer += int(line[1:]) * (1 if line[0] == 'R' else -1)

        if pointer <= 0:
            acc_p2 += (abs(pointer) // 100) + extra
        elif pointer >= 100:
            acc_p2 += pointer // 100

        pointer %= 100

        if pointer == 0:
            acc_p1 += 1

    return acc_p1, acc_p2


if __name__ == '__main__':
    setday(1)

    data = parselines()

    print('part1: %d\npart2: %d' % solve())
