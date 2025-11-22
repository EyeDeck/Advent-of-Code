from aoc import *


def p1():
    registers = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}  # why didn't I just defaultdict?
    last_sound = INF
    pointer = 0

    while True:
        sp = [int(s) if (s.isnumeric() or s[0] == '-') else s for s in data[pointer].split()]
        ins = sp[0]
        args = sp[1:]

        args_v = [a if isinstance(a, int) else registers[a] for a in sp[1:]]
        if ins == 'jgz':
            if args_v[0] > 0:
                pointer += args_v[1]
                continue
        elif ins == 'rcv':
            if args[0] != 0:
                return last_sound
        elif ins == 'snd':
            last_sound = args_v[0]
        else:
            x = args[0]
            y = args_v[1]

            if ins == 'set':
                registers[x] = y
            elif ins == 'add':
                registers[x] += y
            elif ins == 'mul':
                registers[x] *= y
            elif ins == 'mod':
                registers[x] %= y

        pointer += 1

    return None


def p2():
    p_0 = defaultdict(int, {'queue':deque()})
    p_1 = defaultdict(int, {'queue':deque(), 'p':1})

    def tick(program_0, program_1, which):
        registers = program_1 if which else program_0

        sp = [int(s) if (s.isnumeric() or s[0] == '-') else s for s in data[registers['pointer']].split()]
        ins = sp[0]
        args = sp[1:]

        args_v = [a if isinstance(a, int) else registers[a] for a in sp[1:]]
        if ins == 'jgz':
            if args_v[0] > 0:
                registers['pointer'] += args_v[1]
                return 0
        elif ins == 'rcv':
            if not registers['queue']:
                return -1
            else:
                registers[args[0]] = registers['queue'].popleft()
        elif ins == 'snd':
            other = program_0 if which else program_1
            other['queue'].append(args_v[0])
            registers['pointer'] += 1
            if which:
                return 1
            else:
                return 0
        else:
            x = args[0]
            y = args_v[1]

            if ins == 'set':
                registers[x] = y
            elif ins == 'add':
                registers[x] += y
            elif ins == 'mul':
                registers[x] *= y
            elif ins == 'mod':
                registers[x] %= y

        registers['pointer'] += 1
        return 0

    acc = 0
    while True:
        r_0 = tick(p_0, p_1, False)
        r_1 = tick(p_0, p_1, True)

        if r_1 > 0:
            acc += 1
        elif r_0 + r_1 == -2:
            return acc


setday(18)

data = parselines()

print('part1:', p1())
print('part2:', p2())
