from aoc import *


def solve(registers):
    program = [[int(word) if word.lstrip('-').isnumeric() else word for word in line.split()] for line in data]

    ins_p = 0
    while ins_p < len(program):
        instruction = program[ins_p]
        # print(instruction, registers, len(program), ins_p)
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
            if type(off) == str:
                off = registers[off]
            if val > 0:
                # print(ins_p, off, type(ins_p), type(off))
                ins_p += off
                continue
        elif op == 'tgl':
            off = ins_p + registers[instruction[1]]
            # print('target', tgt)
            if off < len(program):
                tgt = program[off]
                if len(tgt) == 2:
                    program[off][0] = 'dec' if tgt[0] == 'inc' else 'inc'
                elif len(tgt) == 3:
                    program[off][0] = 'cpy' if tgt[0] == 'jnz' else 'jnz'
                # print('target/', tgt, '       ', registers)
                # input()
            # print(tgt, len(program))
        ins_p += 1
        # print(instruction, registers)
        # input()
    return registers['a']


def solve_2(registers):
    program = [[int(word) if word.lstrip('-').isnumeric() else word for word in line.split()] for line in data]

    ins_p = 0
    while ins_p < len(program):
        instruction = program[ins_p]
        # print(instruction, registers, len(program), ins_p)
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
            if type(off) == str:
                off = registers[off]
            if val > 0:
                # print(ins_p, off, type(ins_p), type(off))
                ins_p += off
                continue
        elif op == 'tgl':
            off = ins_p + registers[instruction[1]]
            # print('target', tgt)
            if off < len(program):
                tgt = program[off]
                if len(tgt) == 2:
                    program[off][0] = 'dec' if tgt[0] == 'inc' else 'inc'
                elif len(tgt) == 3:
                    program[off][0] = 'cpy' if tgt[0] == 'jnz' else 'jnz'
                # print('target/', tgt, '       ', registers)
                # input()
            # print(tgt, len(program))
        ins_p += 1
        # print(ins_p, instruction, registers)
        if ins_p == 7:
            # input()
            registers['a'] = registers['b'] * registers['d']
            registers['d'] = 0
            registers['c'] = -16
        # if registers['a'] == 0:
        #     input()
        # input()
    return registers['a']


setday(23)

data = parselines()

print('part1:', solve_2(defaultdict(int) | {'a':7}) )
print('part2:', solve_2(defaultdict(int) | {'a':12}) )
