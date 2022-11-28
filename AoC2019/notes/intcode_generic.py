import copy
import sys
from collections import defaultdict


def intcode(p, args):
    # p['error'] = 0
    while True:
        ptr = p['pointer']
        rb = p['relative_base']

        op = get_op(p, ptr)
        if op is None:
            # p['error'] = 1
            return None, -1
        # print(opcodes[op[0]][0], op)

        if op[0] == 1:  # add
            write_val(p, op[3], get_val(p, op[1]) + get_val(p, op[2]))
        elif op[0] == 2:  # mul
            write_val(p, op[3], get_val(p, op[1]) * get_val(p, op[2]))
        elif op[0] == 3:  # input
            if len(args):
                v = args.pop(0)
            else:
                # v = int(input('Input:'))
                return None, 3
            write_val(p, op[1], v)
        elif op[0] == 4:  # output
            p['pointer'] = ptr + len(op)
            return get_val(p, op[1]), 4
        elif op[0] == 5:  # jump if true
            if get_val(p, op[1]) != 0:
                p['pointer'] = get_val(p, op[2])
                continue
        elif op[0] == 6:  # jump if false
            if get_val(p, op[1]) == 0:
                p['pointer'] = get_val(p, op[2])
                continue
        elif op[0] == 7:  # less than
            write_val(p, op[3], 1 if get_val(p, op[1]) < get_val(p, op[2]) else 0)
        elif op[0] == 8:  # equals
            write_val(p, op[3], 1 if get_val(p, op[1]) == get_val(p, op[2]) else 0)
        elif op[0] == 9:
            p['relative_base'] = rb + get_val(p, op[1])
        elif op[0] == 99:
            return None, 99

        p['pointer'] = ptr + len(op)


def get_op(p, ptr):
    op = [p[ptr] % 100]

    if op[0] not in opcodes:
        return None

    ln = opcodes[op[0]][1]
    modes = [int(i) for i in str(p[ptr] // 100)[::-1]]
    modes.extend([0 for _ in range(ln - len(modes) - 1)])

    for i in range(1, ln):
        op.append((p[ptr + i], modes[i - 1]))
    return op


def get_val(program, pointer):
    if pointer[1] == 0:
        return program[pointer[0]]
    elif pointer[1] == 1:
        return pointer[0]
    else:
        return program[program['relative_base'] + pointer[0]]


def write_val(program, pointer, val):
    if pointer[1] == 0:
        program[pointer[0]] = val
    # elif pointer[1] == 1:  # explicitly not supported according to day...5?
    #    program[0] = val
    else:
        program[program['relative_base'] + pointer[0]] = val


opcodes = {
    1: ('add         ', 4),
    2: ('mul         ', 4),
    3: ('input       ', 2),
    4: ('output      ', 2),
    5: ('jmp_if_true ', 3),
    6: ('jmp_if_false', 3),
    7: ('less_than   ', 4),
    8: ('equals      ', 4),
    9: ('mod_rel_base', 2),
    99: ('stop        ', 1)
}


def run_until_stop(program, args):
    out = []
    while True:
        output, reason_for_stop = intcode(program, args)
        # print(output, reason_for_stop)
        if reason_for_stop == -1:
            print('crash')
            return
        elif reason_for_stop == 3:
            print(out)
            args = [int(input('input:'))]
            continue
        elif reason_for_stop == 4:
            out.append(output)
        elif reason_for_stop == 99:
            print(out)
            print('end')
            return out

    return out


f = 'd15.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})
p1p = copy.deepcopy(inp)

run_until_stop(p1p, [])

# erase board
# print('\x1b[200B\x1b[200C\x1b[1J\x1b[1;1H')  # down 200, right 200, erase 1,1->cursor, set cursor 1,1

# cursor up
# print('\x1b[{};1B'.format(up))
