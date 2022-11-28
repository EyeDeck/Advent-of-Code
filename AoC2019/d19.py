import copy
import re
import sys
from collections import defaultdict
from operator import itemgetter

# import numpy as np
#
#
# def get_dict_bounds(d):
#     k = d.keys()
#     return ((min(k, key=itemgetter(0))[0], min(k, key=itemgetter(1))[1]),
#             (start_coords(k, key=itemgetter(0))[0], start_coords(k, key=itemgetter(1))[1]))
#
#
# def render_array(bd):
#     as_str = np.array2string(np.swapaxes(bd,0,1), max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
#                           formatter={'str_kind': lambda x: x})
#     print('\x1b[1;1H\r', re.sub('[\[\]]', '', as_str), end='\n')
#
#
# def dict_to_array(to_render):
#     layer_bounds = get_dict_bounds(to_render)
#     offset = (abs(min(layer_bounds[0][0], 0)), abs(min(layer_bounds[0][1], 0)))
#     adjusted_bounds = layer_bounds[1][0] + offset[0] + 1, layer_bounds[1][1] + offset[1] + 1
#     board = np.full((adjusted_bounds), fill_value=' ', dtype=str)
#     for k, v in to_render.items():
#         if not isinstance(k, tuple):
#             continue
#         board[k[0]+offset[0], k[1]+offset[1]] = v
#
#     return board
#
#
# def prog_out_to_array(prog_output):
#     prog_ascii = [chr(c) for c in prog_output]
#     y = 0
#     x_off = 0
#     render = {}
#     for x, char in enumerate(prog_ascii):
#         if char == '\n':
#             y += 1
#             x_off = x+1
#         else:
#             render[x-x_off, y] = char
#     return dict_to_array(render)

# usage:
#  pass a dict where keys are (x,y) tuples to dict_to_array
#  the max bounds will be calculated, and then overlaid in a numpy 2d array


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
            # print(out)
            # print('end')
            return out

    return out


tried = {}
def try_coords(x,y):
    if (x,y) in tried:
        return tried[x,y]
    else:
        prog = inp.copy()
        out = run_until_stop(prog, [x, y])[0]
        tried[x,y] = out
        return out


def check_corners(x,y):
    return try_coords(x+99, y), try_coords(x, y+99)


def get_starting_range(mn, mx, res):
    for x in range(mn, mx, res):
        for y in range(mn, mx, res):
            # print(check_corners(x,y), x, y)
            if check_corners(x,y) == (1, 1):
                return x,y


# Why was today so ridiculously easy?
f = 'd19p2.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})

print('running part 1...', end='\r')
p1 = 0
for x in range(0,50):
    for y in range(0,50):
        p1 += try_coords(x,y)
print(f'p1: {p1}          \nfinding starting range...', end='\r')

res = 64
start_coords = get_starting_range(0, 5000, 200)
best = 0
while True:
    good = set()
    for x in range(start_coords[0] - (10 * res), start_coords[0] + 1, res):
        for y in range(start_coords[1] - (10 * res), start_coords[1] + 1, res):
            these_coords = check_corners(x,y)
            if these_coords == (1,1):
                good.add((x,y))

    minim = 1000000
    best = 0
    for coords in good:
        dist = coords[0] + coords[1]
        if dist < minim:
            minim = dist
            best = coords

    if best == start_coords and res == 1:
        break
    else:
        print(f'refining test... current: {best}, resolution: {res}    ', end='\r')
        start_coords = best
        res = max(1, res // 2)
print(f'p2: {best[0] * 10000 + best[1]}' + 50 * ' ')
