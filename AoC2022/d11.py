import copy
import math
import sys
import re
from collections import deque


def solve(monkeys, steps, worry_op):
    for turn in range(steps):
        for monkey in monkeys:
            while monkey['items']:
                worry = monkey['items'].popleft()
                worry = monkey['op'](worry)
                worry = worry_op(worry)
                monkeys[monkey[worry % monkey['test'] == 0]]['items'].append(worry)
                monkey['ct'] += 1
    inspections = sorted([m['ct'] for m in monkeys])
    return inspections[-1] * inspections[-2]


def parse_monkey(m):
    return {
        # 'id': int(re.findall('[0-9]', m[0])[0]),
        'items': deque(int(i) for i in re.findall('[0-9]+', m[1])),
        'op': eval('lambda old:' + m[2].split('=')[-1]),  # >:)
        'test': int(m[3].split()[-1]),
        True: int(m[4].split()[-1]),
        False: int(m[5].split()[-1]),
        'ct': 0
    }


day = 11
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    monkeys_raw = [line.strip() for line in file.read().split('\n\n')]
    monkeys = [parse_monkey(m.split("\n")) for m in monkeys_raw]

print('part1:', solve(copy.deepcopy(monkeys), 20, lambda x: x // 3))
magic = math.lcm(*(m["test"] for m in monkeys))
print('part2:', solve(copy.deepcopy(monkeys), 10000, lambda x: x % magic))
