import copy
import re
import sys
from collections import defaultdict
from operator import itemgetter
import colorama

import numpy as np


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


def get_dict_bounds(d):
    k = d.keys()
    return ((min(k, key=itemgetter(0))[0], min(k, key=itemgetter(1))[1]),
            (max(k, key=itemgetter(0))[0], max(k, key=itemgetter(1))[1]))


def render_array(bd):
    as_str = np.array2string(np.swapaxes(bd,0,1), max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
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
        board[k[0]+offset[0], k[1]+offset[1]] = v
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
            x_off = x+1
        else:
            render[x-x_off, y] = char
    #print(render)
    return dict_to_array(render)


def run_until_stop(program, args, stop_on_1010=False):
    out = []
    ignore_first_x = 2
    last_output = 0
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
            # print(chr(output), end='')
            last_output = output
            out.append(output)
            if stop_on_1010 and out[-1] == 10 and out[-2] == 10:
                if ignore_first_x > 0:
                    ignore_first_x -= 1
                    out = []
                    continue
                render_array(prog_out_to_array(out))

                if True not in [(ord(c) in out) for c in '<>^v']:
                    print(last_output)
                    print('he ded')
                    # return out

                out = []
                # input()

        elif reason_for_stop == 99:
            # print(out)
            print(last_output)
            print('end')
            return out

    return out


colorama.init()

f = 'd17.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})
p1p = copy.deepcopy(inp)

prog_out = run_until_stop(p1p, [])
board = prog_out_to_array(prog_out)
render_array(board)

bounds = [0, 0, board.shape[0], board.shape[1]]
# print(bounds)
alignment = 0
for x,line in enumerate(board):
    for y,char in enumerate(line):
        if char != '#':
            continue
        if x-1 < bounds[0] or x+2 > bounds[2]:
            continue
        if y-1 < bounds[1] or y+2 > bounds[3]:
            continue
        if board[x-1,y] == '#' and board[x+1,y] == '#' and board[x,y-1] == '#' and board[x,y+1] == '#':
            alignment += x*y
            board[x,y] = 'O'
print()
render_array(board)
print(alignment)

p2p = copy.deepcopy(inp)
p2p[0] = 2

# L,12,L,8,R,10,R,10,L,6,L,4,
# L,12,L,12,L,8,R,10,R,10,L,6,L,4
# L,12,R,10,L,8,L,4,R,10,L,6,L,4
# L,12,L12,L,8,R,10,R,10,R,10,L,8
# L,4,R,10,L,6,L,4,L,12,R,10,L,8,L,4,R,10
rules = '''A,B,A,B,C,B,A,C,B,C
L,12,L,8,R,10,R,10
L,6,L,4,L,12
R,10,L,8,L,4,R,10
n
'''
for line in rules.split('\n'):
    # print([ord(c) for c in line])
    assert len(line) <= 20

args = [ord(c) for c in rules]
# print(args)

print('\x1b[200B\x1b[200C\x1b[1J\x1b[1;1H')

prog_out = run_until_stop(p2p, args, True)
# print(prog_out[-1])

# print(prog_ascii

# erase board
# print('\x1b[200B\x1b[200C\x1b[1J\x1b[1;1H')  # down 200, right 200, erase 1,1->cursor, set cursor 1,1

# cursor up
# print('\x1b[{};1B'.format(up))
