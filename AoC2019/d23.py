import copy
import re
import sys
from collections import defaultdict
from operator import itemgetter
# import colorama

import numpy as np


def intcode_tick(p, args):
    ptr = p['pointer']
    rb = p['relative_base']

    op = get_op(p, ptr)
    if op is None:
        # p['error'] = 1
        return -1, None
    # print(opcodes[op[0]][0], op, args)

    if op[0] == 1:  # add
        write_val(p, op[3], get_val(p, op[1]) + get_val(p, op[2]))
    elif op[0] == 2:  # mul
        write_val(p, op[3], get_val(p, op[1]) * get_val(p, op[2]))
    elif op[0] == 3:  # input
        write_val(p, op[1], args.pop(0))
        p['pointer'] = ptr + len(op)
        return 3, None
    elif op[0] == 4:  # output
        p['pointer'] = ptr + len(op)
        return 4, get_val(p, op[1])
    elif op[0] == 5:  # jump if true
        if get_val(p, op[1]) != 0:
            p['pointer'] = get_val(p, op[2])
            return 0, None
    elif op[0] == 6:  # jump if false
        if get_val(p, op[1]) == 0:
            p['pointer'] = get_val(p, op[2])
            return 0, None
    elif op[0] == 7:  # less than
        write_val(p, op[3], 1 if get_val(p, op[1]) < get_val(p, op[2]) else 0)
    elif op[0] == 8:  # equals
        write_val(p, op[3], 1 if get_val(p, op[1]) == get_val(p, op[2]) else 0)
    elif op[0] == 9:
        p['relative_base'] = rb + get_val(p, op[1])
    elif op[0] == 99:
        return 99, None

    p['pointer'] = ptr + len(op)
    return 0, None


def intcode(p, args):
    while True:
        tick, val = intcode_tick(p, args)
        if tick != 0:
            return val


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


def get_dict_bounds(d):
    k = d.keys()
    return ((min(k, key=itemgetter(0))[0], min(k, key=itemgetter(1))[1]),
            (max(k, key=itemgetter(0))[0], max(k, key=itemgetter(1))[1]))


def render_array(bd):
    as_str = np.array2string(np.swapaxes(bd, 0, 1), max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
                             formatter={'str_kind': lambda x: x})
    print('\x1b[1;1H\r', re.sub('[\[\]]', '', as_str), end='\n')


def dict_to_array(to_render):
    # drone = to_render.pop('drone')

    layer_bounds = get_dict_bounds(to_render)
    offset = (abs(min(layer_bounds[0][0], 0)), abs(min(layer_bounds[0][1], 0)))
    adjusted_bounds = layer_bounds[1][0] + offset[0] + 1, layer_bounds[1][1] + offset[1] + 1
    # print(adjusted_bounds)
    # print(to_render, layer_bounds, offset)
    board = np.full((adjusted_bounds), fill_value=' ', dtype=str)
    for k, v in to_render.items():
        if not isinstance(k, tuple):
            continue
        board[k[0] + offset[0], k[1] + offset[1]] = v
    # board[board[drone[0]+offset[0], drone[1]+offset[1]]] = 'D'
    # print('\x1b[{}A'.format(adjusted_bounds[0]+1))
    # print('\x1b[200B\x1b[200C\x1b[1J\x1b[1;1H')

    return board


def prog_out_to_array(prog_output):
    prog_ascii = [chr(c) for c in prog_output]
    y = 0
    x_off = 0
    render = {}
    for x, char in enumerate(prog_ascii):
        if char == '\n':
            y += 1
            x_off = x + 1
        else:
            render[x - x_off, y] = char
    # print(render)
    return dict_to_array(render)


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
            # args = [int(input('input:'))]
            continue
        elif reason_for_stop == 4:
            print(out)
            input()
            # print(chr(output), end='')
            out.append(output)

        elif reason_for_stop == 99:
            # print(out)
            return out

    return out


# colorama.init()

f = 'd23.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})

computers = [inp.copy() for _ in range(50)]
c_args = [[i, -1] for i in range(50)]
c_queues = [[] for _ in range(50)]
c_consecutive_reads = [0 for _ in range(50)]
queue = []
NAT = None
all_idle = False
last_y_sent = 0
p1 = None
while True:
    # print(c_consecutive_reads)
    all_idle = True
    for a in c_args:
        if a[0] != -1:
            all_idle = False
            break
    for ct in c_consecutive_reads:
        if ct == 0:
            all_idle = False
            break

    if all_idle and (NAT is not None):
        c_args[0] = NAT.copy()

        if NAT[1] == last_y_sent:
            p2 = last_y_sent
            break

        last_y_sent = NAT[1]
        NAT = None

        print(f'p2: {last_y_sent}...', end='\r')
        # input(f'we idle bois {NAT}')
        # print(f'idle again {NAT}')

    for i, c in enumerate(computers):
        r_reason, r_val = intcode_tick(c, c_args[i])

        if r_reason == 0:
            continue
        if r_reason == 3:
            c_consecutive_reads[i] += 1
            # print(f'computer {i} ate an arg, remaining: {c_args[i]}')

            if len(c_args[i]) == 0:
                c_args[i].append(-1)
        if r_reason == 4:
            c_consecutive_reads[i] = 0
            # print(f'computer {i} got an output: {r_val}')
            c_queues[i].append(r_val)

            if len(c_queues[i]) == 3:
                c_addr, x, y = c_queues[i]
                if c_addr != 255:
                    c_args[c_addr].extend([x, y])
                    if c_args[c_addr][0] == -1:
                        c_args[c_addr].pop(0)
                    if p1 is None:
                        p1 = y
                        print(f'p1: {p1}')
                else:
                    NAT = [x, y]
                    # print(f'stored NAT {NAT}')
                c_queues[i] = []

print(f'p2: {p2}   ')
