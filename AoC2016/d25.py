from aoc import *


def solve(registers):
    program = [[int(word) if word.lstrip('-').isnumeric() else word for word in line.split()] for line in data]

    ins_p = 0
    while ins_p < len(program):
        instruction = program[ins_p]

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
                ins_p += off
                continue
        elif op == 'tgl':
            off = ins_p + registers[instruction[1]]
            if off < len(program):
                tgt = program[off]
                if len(tgt) == 2:
                    program[off][0] = 'dec' if tgt[0] == 'inc' else 'inc'
                elif len(tgt) == 3:
                    program[off][0] = 'cpy' if tgt[0] == 'jnz' else 'jnz'
        elif op == 'out':
            val = instruction[1]
            if type(val) == str:
                val = registers[val]
            yield val
        ins_p += 1
    return registers['a']

def p1():
    for i in range(1_000_000):
        print(i, '...', end='\r')
        n = 0
        s = iter(solve(defaultdict(int) | {'a': i}))
        for j in range(1_000):
            if next(s) != n:
                break
            n ^= 1
        else:
            return i


setday(25)

data = parselines()

print('part1:', p1() )