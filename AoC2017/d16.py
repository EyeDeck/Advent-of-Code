from aoc import *


def tick(programs):
    for line in data:
        op, r = line[0], line[1:]
        if op == 's':
            n = int(r)
            programs[:] = programs[-n:] + programs[:-n]
        elif op == 'x':
            a, b = (int(s) for s in r.split('/'))
            programs[a], programs[b] = programs[b], programs[a]
        elif op == 'p':
            a, b = r.split('/')
            a, b = programs.index(a), programs.index(b)
            programs[a], programs[b] = programs[b], programs[a]


def to_str(l):
    return ''.join(l)


def p1():
    programs = [p for p in 'abcdefghijklmnop']
    tick(programs)
    return to_str(programs)


def p2():
    iters = 1_000_000_000
    programs = [p for p in 'abcdefghijklmnop']
    cycle_len = 0
    seen = {to_str(programs): 0}
    for i in range(iters):
        tick(programs)
        state = to_str(programs)
        if state in seen:
            cycle_len = i + 1
            break
        seen[state] = i + 1
    return [k for k, v in seen.items() if v == iters % cycle_len][0]


setday(16)

data = parselines()[0].split(',')

print('part1:', p1())
print('part2:', p2())
