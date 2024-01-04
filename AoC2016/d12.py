from aoc import *


def solve(registers):
    program = [[int(word) if word.lstrip('-').isnumeric() else word for word in line.split()] for line in data]

    ins_p = 0
    while ins_p < len(program):
        instruction = program[ins_p]
        # print(instruction, registers)
        op = instruction[0]
        if op == 'cpy':
            val, dest = instruction[1:]
            if type(val) == str:
                val = registers[val]
            registers[dest] = val
        elif op == 'inc':
            registers[instruction[1]] += 1
        elif op == 'dec':
            registers[instruction[1]] -= 1
        elif op == 'jnz':
            val, off = instruction[1:]
            if type(val) == str:
                val = registers[val]
            if val > 0:
                ins_p += off
                continue
        ins_p += 1
    return registers['a']


setday(12)

data = parselines()

print('part1:', solve(defaultdict(int)) )
print('part2:', solve(defaultdict(int) | {'c':1}) )
