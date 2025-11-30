import math
from aoc import *


def p1():
    registers = {chr(i): 0 for i in range(ord('a'), ord('h') + 1)}
    pointer = 0

    program = [[int(s) if (s.isnumeric() or s[0] == '-') else s for s in line.split()] for line in data]
    # print(program)

    acc = 0
    while True:
        if pointer >= len(program):
            return acc
        instruction = program[pointer]
        opcode = instruction[0]
        args = instruction[1:]
        # print(opcode, args, registers)

        args_v = [a if isinstance(a, int) else registers[a] for a in instruction[1:]]
        if opcode == 'jnz':
            if args_v[0] != 0:
                pointer += args_v[1]
            else:
                pointer += 1
        else:
            x = args[0]
            y = args_v[1]

            if opcode == 'set':
                registers[x] = y
            elif opcode == 'sub':
                registers[x] -= y
            elif opcode == 'mul':
                acc += 1
                registers[x] *= y

            pointer += 1


"""
set b 99
set c b
jnz a 2---------->
jnz 1 5------->  |
mul b 100-----|--<
sub b -100000 |
set c b       |
sub c -17000  |
set f 1-------<--<
set d 2          |
set e 2--------< |
set g d-----<  | |
mul g e     |  | |
sub g b     |  | |
jnz g 2-->  |  | |
set f 0  |  |  | |
sub e -1-<  |  | |
set g e     |  | |
sub g b     |  | |
jnz g -8---->  | |
sub d -1       | |
set g d        | |
sub g b        | |
jnz g -13------> |
jnz f 2--->      |
sub h -1  |      |
set g b---<      |
sub g c          |
jnz g 2------->  |
jnz 1 3 --->  |  |
sub b -17--|--<  |
jnz 1 -23 ------->
           |
           V
"""


def p2():
    registers = {chr(i): 0 for i in range(ord('a'), ord('h') + 1)}
    registers['a'] = 1
    last_sound = INF
    pointer = 0

    program = [[int(s) if (s.isnumeric() or s[0] == '-') else s for s in line.split()] for line in data]

    i = 0
    while True:
        i += 1
        if pointer >= len(program):
            return registers['h']

        # if pointer == 9:
        #     registers['e'] = registers['b'] - 1
        #     registers['d'] = registers['b'] - 1

        instruction = program[pointer]
        opcode = instruction[0]
        args = instruction[1:]
        # if i % 10000000 == 0:
        if True:
            out = f'[{i}] [p:{pointer}] = {opcode}, {args}'
            out += ((33 - len(out)) * ' ') + f'| {registers}'
            print(out)
            inp = ''
            inp = input()
            if len(inp):
                spl = inp.split(' ')
                if len(spl) > 1 and spl[0] in 'abcdefgh' and spl[1].isnumeric():
                    registers[spl[0]] = int(spl[1])
                    print('modified registers:', registers)

            # print(len(inp))

        args_v = [a if isinstance(a, int) else registers[a] for a in instruction[1:]]
        if opcode == 'jnz':
            if args_v[0] != 0:
                pointer += args_v[1]
            else:
                pointer += 1
        else:
            x = args[0]
            y = args_v[1]

            if opcode == 'set':
                registers[x] = y

                # if pointer == 8:
                #     registers['f'] = 0
                # if pointer == 9:
                #     registers['d'] = registers['b']-1
                # if pointer == 10:
                #     if registers['f'] == 1:
                #         # print('thing a')
                #         registers['e'] = registers['b'] // registers['d']
                #     # else:
                #     #     registers['e'] = registers['b']
                #
                # if pointer == 11 and registers['f'] == 0:
                #     # print('thing b')
                #     registers['e'] = registers['b'] - 1


            elif opcode == 'sub':
                registers[x] -= y
            elif opcode == 'mul':
                registers[x] *= y

            pointer += 1


def rewrite():
    a = 1                             # 0
    b = 99                            # 1
    c = b                             # 2
    d = 0
    e = 0
    flag = 0
    g = 0
    h = 0

    # skip p1 jump                    # 3

    b *= 100                          # 5
    b -= -100000                      # 6
    c = b                             # 7
    c -= -17000                       # 8
    print(a, b, c, d, e, flag, g, h)
    while True:                       # <-- 32
        print('<-32', a, b, c, d, e, flag, g, h)
        flag = True                      # 9
        d = 2                         # 10
        while True:                   # <-- 24
            print('<-24', a, b, c, d, e, flag, g, h)
            e = 2                     # 11
            while True:               # <-- 20
                print('<-20', a, b, c, d, e, flag, g, h)
                g = d                 # 12
                g *= e                # 13
                g -= b                # 14
                if g == 0:            # 15
                    flag = False      # 16
                e -= -1                # 17
                g = e                 # 18
                g -= b                # 19
                if g == 0:            # 20 -->
                    break
            d -= -1                   # 21
            g = d                     # 22
            g -= b                    # 23
            if g == 0:                # 24 -->
                break
        if not flag:              # 25
            h -= 1                # 26
        g = b                     # 27
        g -= c                    # 28
        if g != 0:                # 29
            return h                  # 30
        b -= 17               # 31
        break              # 32 -->



def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def optimized():
    b = 99                            # 1
    b *= 100                          # 5
    b -= -100000                      # 6
    c = b                             # 7
    c -= -17000                       # 8
    h = 0
    for i in range(b, c+17, 17):
        h += 0 if is_prime(i) else 1
    return h


setday(23)

data = parselines()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
# print('part2:', p2())
print('part3:', optimized())
