import operator
from aoc import *


def is_gradual(nums):
    if nums[0] > nums[1]:
        op = operator.gt
    else:
        op = operator.lt

    for n in range(len(nums) - 1):
        a, b = nums[n], nums[n + 1]

        if not op(a, b) or abs(a - b) > 3:
            return 0
    return 1


def is_gradual_with_dampening(nums):
    for n in range(len(nums)):
        if is_gradual(nums[:n] + nums[n + 1:]):
            return 1
    return 0


def p1():
    return sum(is_gradual(line) for line in data)


def p2():
    return sum(is_gradual_with_dampening(line) for line in data)


setday(2)

data = parselines(get_ints)

print('part1:', p1())
print('part2:', p2())
