import itertools
import operator

from aoc import *


def test_ops(target, numbers, operators):
    op_combs = [operators for _ in range(len(numbers) - 1)]

    for ops in itertools.product(*op_combs):
        acc = numbers[0]
        for n, op in zip(numbers[1:], ops):
            acc = op(acc, n)
        if acc == target:
            return target
    return 0


def solve(ops):
    acc = 0
    for line in data:
        target, numbers = line[0], line[1:]
        acc += test_ops(target, numbers, ops)
    return acc


setday(7)

data = parselines(get_ints)

print('part1:', solve([operator.add, operator.mul]))
print('part2:', solve([operator.add, operator.mul, lambda a, b: int(str(a) + str(b))]))
