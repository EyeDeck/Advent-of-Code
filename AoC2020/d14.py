import sys
from collections import *


def p1():
    memory = defaultdict(int)
    bitmask = ''.join(['X' for _ in range(36)])
    for line in data:
        ins = line[0]
        if ins == 'mem':
            addr = line[1]
            num = int(line[2])
            bits = [c for c in bin(num)][2:]
            out = ['0' for _ in range(36)]
            for i, bit in enumerate(reversed(bits)):
                out[-i - 1] = bit

            for i, bit in enumerate(bitmask):
                if bit != 'X':
                    out[i] = bit
            memory[int(addr)] = int(''.join(out), 2)
        elif ins == 'mask':
            bitmask = line[1]
    return sum(memory.values())


def p2():
    def fork_write(a, v):
        for i, c in enumerate(a):
            if c == 'X':
                a[i] = '0'
                fork_write(a.copy(), v)
                a[i] = '1'
                fork_write(a.copy(), v)
                return
        else:
            memory[''.join(a)] = v

    memory = defaultdict(int)
    bitmask = ''.join(['X' for _ in range(36)])
    for line in data:
        ins = line[0]
        if ins == 'mem':
            addr = ['0' for _ in range(36)]
            addr_raw = [c for c in bin(int(line[1]))][2:]
            for i, bit in enumerate(reversed(addr_raw)):
                addr[-i - 1] = bit

            num = int(line[2])
            for i, bit in enumerate(bitmask):
                if bit == '0':
                    pass
                else:
                    addr[i] = bit
            fork_write(addr, num)

        elif ins == 'mask':
            bitmask = line[1]
    return sum(memory.values())


f = 'dx.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[p.strip() for p in line.strip().split('=')] for line in file]

for i, line in enumerate(data):
    if line[0][:3] == 'mem':
        data[i] = ['mem', line[0][4:-1], line[1]]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
