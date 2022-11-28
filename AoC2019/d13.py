import copy
import msvcrt
import sys
import time
from collections import defaultdict
import colorama

import numpy as np


def intcode(p, args):
    p['error'] = 0
    while True:
        ptr = p['pointer']
        rb = p['relative_base']

        op = get_op(p, ptr)
        if op is None:
            p['error'] = 1
            return None, 1
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
            return get_val(p, op[1])
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
            return None, None

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


def printboard(bd):
    print(np.array2string(np.swapaxes(bd, 0, 1), max_line_width=200, separator=' ', threshold=1000, edgeitems=1000, formatter={'str_kind': lambda x: x}), end='\r')


def renderboard(board, program, last=(), score=0):
    for i in range(0, len(program), 3):
        x, y, tile = program[i:i + 3]
        if tile == 0:
            board[x, y] = ' '
        elif tile == 1:
            board[x, y] = '#'
        elif tile == 2:
            board[x, y] = '='
        elif tile == 3:
            board[x, y] = '—'
            last = (x, last[1])
        elif tile == 4:
            board[x, y] = 'o'
            last = (last[0], x)
    print()
    x, y = board.shape
    x -= 14
    y -= 1
    for c in 'score: ' + str(score):
        board[x, y] = c
        x += 1
    printboard(board)
    print('\x1b[2;1H')
    return last


def run_until_stop(program, args, max_x=0, max_y=0):
    out = []
    board = np.full((max_x, max_y), fill_value=' ', dtype=str)
    # print(board)
    score = 0
    last_ball = 0
    last_paddle = 0
    while True:
        cur = [intcode(program, args)]
        args = []
        cur.extend([intcode(program, args), intcode(program, args)])
        # print(cur)
        if cur[0] == (None, 1):
            if program['error'] != 0:
                out.append('crash: ' + str(program['error']))
                break
        elif cur[0] == (None, None):
            print('end')
            break
        elif cur[0] == (None, 3) or cur[0] == -1 and cur[1] == 0:
            if isinstance(cur[0], tuple):
                pass
            else:
                score = cur[2]

            last_paddle, last_ball = renderboard(board, out, (last_paddle, last_ball), score)

            # move = msvcrt.getch()
            # if move == b'a':
            #     args.append(int(1))
            # elif move == b'd':
            #     args.append(int(-1))
            # elif move == b'\x1b':
            #     sys.exit()
            # else:
            #     args.append(0)
            # print(last_ball, last_paddle)

            if last_ball < last_paddle:
                args.append(-1)
                # print('l')
            elif last_ball > last_paddle:
                args.append(1)
                # print('r')
            else:
                args.append(0)
                # print('stop')
        else:
            #print(out)
            out.extend(cur)
    print('\x1b[{};1B'.format(max_y))
    return out


colorama.init()  # autoreset=True)

f = 'd13.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})
p1p = copy.deepcopy(inp)

p1out = run_until_stop(p1p, [])
# print(p1out)
print('\x1b[200B\x1b[200C\x1b[1J\x1b[1;1H')  # down 200, right 200, erase 1,1->cursor, set cursor 1,1
print('p1', len([p1out[i] for i in range(-1, len(p1out), 3) if p1out[i] == 2]))

max_x = max([p1out[i] for i in range(0, len(p1out), 3)]) + 1
max_y = max([p1out[i] for i in range(1, len(p1out), 3)]) + 1
# print(max_x, max_y)

p2_program = copy.deepcopy(inp)
p2_program[0] = 2
run_until_stop(p2_program, [0], max_x, max_y)
