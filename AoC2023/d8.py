import math
from aoc import *


def p1():
    step = 0
    curr = 'AAA'
    i = 0
    while True:
        # print(step, curr, i)
        step += 1
        if i >= len(dirs):
            i = 0
        curr = nodes[curr][0 if dirs[i] == 'L' else 1]
        if curr == 'ZZZ':
            return step
        i += 1
        # print(curr)


def p2():
    step = 0
    curr = [n for n in nodes.keys() if n[-1] == 'A']
    cycles = [-1 for i in range(len(curr))]
    cycles_seen = [set() for i in range(len(curr))]

    i = 0
    while True:
        for j in range(len(curr)):
            c = curr[j]
            curr[j] = nodes[c][0 if dirs[i] == 'L' else 1]

            if c[-1] == 'Z':
                if c in cycles_seen[j]:
                    if cycles[j] == -1:
                        cycles[j] = step

                        if -1 not in cycles:
                            return math.lcm(*[i // 2 for i in cycles])
                else:
                    cycles_seen[j].add(c)
        # print(cycles, cycles_seen)

        step += 1
        i += 1

        if i >= len(dirs):
            i = 0


setday(8)

with open_default() as file:
    dirs, nodes = file.read().split('\n\n')
    nodes = {line[0:3]: (line[7:10], line[-4:-1]) for line in nodes.split('\n')}

print('part1:', p1() )
print('part2:', p2() )
