import copy
import itertools
import re
import sys


def fast_proc(data):
    class Addr:
        def __init__(self, base, mask):
            self.x = int(mask.replace("1", "0").replace("X", "1"), base=2)
            self.val = base
            self.val &= ~self.x
            self.val |= int(mask.replace("X", "0"), base=2)

        def sub(self, other):
            same_bits = ~(self.x | other.x)
            if (self.val & same_bits) != (other.val & same_bits):
                # No overlap in this case.
                return [self]

            res = []
            split_bits = self.x & ~other.x
            for idx in range(36):
                bit = 2 ** idx
                if split_bits & bit:
                    self.x &= ~bit
                    if not (other.val & bit):
                        self.val |= bit
                    adr = copy.copy(self)
                    res.append(adr)
                    self.val ^= bit
            return res

        def loc_count(self):
            return 2 ** bin(self.x).count("1")

    writes = []
    prog = data.strip().splitlines()
    for line in prog:
        if m := re.match(r"mask = (.*)", line):
            mask = m.group(1)
        elif m := re.match(r"mem\[(\d+)\] = (\d+)", line):
            adr = int(m.group(1))
            val = int(m.group(2))
            adr = Addr(adr, mask)
            writes = ([(sub_adr, val2) for sub_adr in adr2.sub(adr)] for adr2, val2 in writes)
            writes = list(itertools.chain(*writes))
            writes.append((adr, val))

    print(sum(w[0].loc_count() for w in writes if w[0]))
    print(sum(w[1] * w[0].loc_count() for w in writes if w[0]))


def p2_exp():
    data_l = [[p.strip() for p in line.strip().split('=')] for line in data.split('\n')]
    for i, line in enumerate(data_l):
        if line[0][:3] == 'mem':
            data_l[i] = ['mem', line[0][4:-1], line[1]]

    memory = []
    bitmask = ''.join(['X' for _ in range(36)])
    for line in data_l:
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
            # memory.append((''.join(addr), num))
            memory.append((addr, num))

        elif ins == 'mask':
            bitmask = line[1]
    # print(memory)

    sum = 0
    seen_x = set()
    for addr, val in reversed(memory):
        # print(addr, val)
        # print(seen_x)
        perms = 1
        for i, c in enumerate(addr):
            if i in seen_x:
                continue
            perms += 1
            if c == 'X':
                seen_x.add(i)
        sum += val * (2**perms)
    return sum
    # return sum(memory.values())


f = 'dx.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read()

fast_proc(data)
print(p2_exp())