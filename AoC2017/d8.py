import operator

from aoc import *


def solve():
    registers = defaultdict(int)
    p2 = 0
    for ins in instructions:
        if ins[4](registers[ins[3]], ins[5]):
            temp = ins[1](registers[ins[0]], ins[2])
            p2 = max(p2, temp)
            registers[ins[0]] = temp
    return max(registers.values()), p2


setday(8)

data = parselines(str.split)

op_map = {
    'dec': operator.sub, 'inc': operator.add,
    '==': operator.eq,   '!=': operator.ne,
    '<': operator.lt,    '<=': operator.le,
    '>': operator.gt,    '>=': operator.ge
}

instructions = [[ins[0], op_map[ins[1]], int(ins[2]), ins[4], op_map[ins[5]], int(ins[6])] for ins in data]

print('part1: %d\npart2: %d' % solve())
