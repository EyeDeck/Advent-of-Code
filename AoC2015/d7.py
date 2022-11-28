import sys
from collections import *


def process(data):
    states = {}
    commands = deque(data)
    while commands:
        nxt = deque()
        while len(commands) and (command := commands.popleft()):
            # print(command)
            dest = command[-1]

            r = command[-3]
            if r.isnumeric():
                r = int(r)
            elif r in states:
                r = states[r]
            else:
                nxt.append(command)
                continue

            if len(command) == 3:
                states[dest] = r
                continue

            op = command[-4]

            if op == 'NOT':
                states[dest] = ~ r
                continue

            l = command[-5]
            if l.isnumeric():
                l = int(l)
            elif l in states:
                l = states[l]
            else:
                nxt.append(command)
                continue

            if op == 'LSHIFT':
                states[dest] = l << r
            elif op == 'RSHIFT':
                states[dest] = l >> r
            elif op == 'OR':
                states[dest] = l | r
            elif op == 'AND':
                states[dest] = l & r
        commands = nxt
    return states['a']


day = 7
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip().split() for line in file]

p1a = process(data)
for i, cmd in enumerate(data):
    if cmd[-1] == 'b':
        data[i][-3] = str(p1a)
p2a = process(data)

print(f'part1: {p1a}')
print(f'part2: {p2a}')
