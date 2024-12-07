import itertools
import operator

from aoc import *

def test_ops(target, numbers, operators):
    op_ct = len(numbers) - 1
    op_combs = [operators for _ in range(op_ct)]

    for ops in itertools.product(*op_combs):
        acc = numbers[0]
        for n, op in zip(numbers[1:], ops):
            acc = op(acc, n)
        if acc == target:
            return target
    return 0

def p1():
    acc = 0
    for line in data:
        target, numbers = line[0], line[1:]
        acc += test_ops(target, numbers, [operator.add, operator.mul, lambda a, b: int(str(a) + str(b))])
    return acc


def p2():
    return None


setday(7)

data = parselines(get_ints)

print('part1:', p1() )
print('part2:', p2() )