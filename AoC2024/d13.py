import z3

from aoc import *


def z3_this_nonsense(a_x, a_y, b_x, b_y, prize_x, prize_y, offset=0):
    optimizer = z3.Optimize()

    x, y = z3.Ints('x y')

    eq1 = a_x * x + b_x * y == prize_x + offset
    eq2 = a_y * x + b_y * y == prize_y + offset

    optimizer.add(eq1, eq2)

    optimizer.minimize(y)

    if optimizer.check() == z3.sat:
        solution = optimizer.model()
        return solution[x].as_long() * 3 + solution[y].as_long()
    else:
        return 0


def solve(offset):
    return sum(z3_this_nonsense(*line, offset=offset) for line in data)


setday(13)


with open_default() as file:
    data = [get_ints(line) for line in file.read().split('\n\n')]

print('part1:', solve(0) )
print('part2:', solve(10000000000000) )
