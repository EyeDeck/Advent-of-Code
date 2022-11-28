from aoc import *

def run(m):
    i = 0
    while i < len(data):
        op = data[i].split()
        # print(m, i, op)

        ins = op[0]
        reg = op[1].strip(',')
        # print(ins, reg)

        if ins == 'jmp':
            i += int(reg)
            continue
        elif ins == 'jie':
            i += int(op[2].strip('+')) if m[reg] & 1 == 0 else 1
            continue
        elif ins == 'jio':
            i += int(op[2].strip('+')) if m[reg] == 1 else 1
            continue

        i += 1

        if ins == 'hlf':
            m[reg] //= 2
        elif ins == 'tpl':
            m[reg] *= 3
        elif ins == 'inc':
            m[reg] += 1
        else:
            die('Unknown opcode')

    # print(m, i, op)
    return m["b"]


def p2():
    return None


day = 23
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {run({"a":0, "b":0})}')
print(f'part2: {run({"a":1, "b":0})}')
