import copy
import sys


def p1(program):
    seen = set()
    acc = 0
    p = 0
    while p < len(program):
        if p in seen:
            return False, acc
        seen.add(p)
        ins = program[p]

        if ins[0] == 'acc':
            acc += ins[1]
        elif ins[0] == 'jmp':
            p += ins[1]
            continue

        elif ins[0] == 'nop':
            pass

        p += 1
    return True, acc


def p2(program):
    for i in range(len(program)):
        prog2 = copy.deepcopy(program)
        if prog2[i][0] == 'jmp':
            prog2[i] = ('nop', prog2[i][1])
        elif prog2[i][0] == 'nop':
            prog2[i] = ('jmp', prog2[i][1])
        else:
            continue
        result = p1(prog2)
        if result[0]:
            return result[1]
    return None


f = 'd8.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip().split(' ') for line in file]
    data = [(line[0], int(line[1])) for line in data]


print(f'part1: {p1(data)[1]}')
print(f'part2: {p2(data)}')
