import copy
import itertools
import random
import re
import sys
from collections import defaultdict
from operator import itemgetter


def intcode(p, args, ct=0):
    # p['error'] = 0
    while True:
        ptr = p['pointer']
        ct += 1

        op = get_op(p, ptr)
        if op is None:
            # p['error'] = 1
            return None, -1, ct
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
                return None, 3, ct
            write_val(p, op[1], v)
        elif op[0] == 4:  # output
            p['pointer'] = ptr + len(op)
            return get_val(p, op[1]), 4, ct
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
            p['relative_base'] = p['relative_base'] + get_val(p, op[1])
        elif op[0] == 99:
            return None, 99, ct

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


# def run_until_stop(program, args):
#     out = []
#     while True:
#         output, reason_for_stop = intcode(program, args)
#         # print(output, reason_for_stop)
#         if reason_for_stop == -1:
#             print('crash')
#             return
#         elif reason_for_stop == 3:
#             print(out)
#             args = [int(input('input:'))]
#             continue
#         elif reason_for_stop == 4:
#             out.append(output)
#         elif reason_for_stop == 99:
#             # print(out)
#             # print('end')
#             return out
#
#     return out


def run_until_stop(program, args, stop_on_1010=False):
    out = []
    ignore_first_x = 2
    last_output = 0
    ct = 0
    while True:
        output, reason_for_stop, ct = intcode(program, args, ct)
        # print(output, reason_for_stop)
        if reason_for_stop == -1:
            print('crash')
            return 0
        elif reason_for_stop == 3:
            print(out)
            args = [int(input('input:'))]
            continue
        elif reason_for_stop == 4:
            if output > 127:
                # print(output)
                # print(last_args)
                return output
            else:
               #  print(chr(output), end='')
                pass

        elif reason_for_stop == 99:
            # print(out)
            # print(ct)
            # print(last_output)
            # print('end')
            return 0

    return out


f = 'd21.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})

# Registers (W):
#   T = temp
#   J = Jump (if true)

# Registers (RO):
#   A = 1 tile hole
#   B = 2 tile
#   C = 3 tile
#   D = 4 tile

# Instructions:
#   AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
#   OR  X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
#   NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.

# if A empty, set J
# if C empty, set T
# if A or C empty, set J
# if A or C empty, and D solid, set J
rules = '''OR A T
AND C T
NOT T J
AND D J
WALK
'''

print(f'p1: { run_until_stop(inp.copy(), [ord(c) for c in rules]) }')

# if A empty, set T
# if A and B empty, set T
# if A and B and C empty, set T
# invert T and store in J
# if D solid, set J
# ~~~ T = !ABC ; J = T & D
# if E solid, or ABC empty, set T
# if H solid, or (ABC empty or E solid), set T
# J = (H, or (!ABC or E)), and D)
rules = '''OR A T
AND B T
AND C T
NOT T J
AND D J
OR E T
OR H T
AND T J
RUN
'''

print(f'p2: { run_until_stop(inp.copy(), [ord(c) for c in rules]) }')


# below is some experimentation in bruteforcing
# part 1 is easy to bruteforce;
# part 2 is really only bruteforcible if you start with certain programs for part 1, then work out what extra to add

# p1_solutions = open('d21p1.txt').read().split('WALK')[:-1]
# print(p1_solutions)
# print(p1_solutions[0])

# all_perms = list(itertools.product(['AND', 'OR', 'NOT'], ['A', 'B', 'C', 'D', 'T', 'J'], ['T', 'J']))
# line_perms = list(itertools.product(all_perms,all_perms,all_perms))
# tried = set()
# found = False
# while not found:
#     print(len(tried), end='\r')
#     # lines = [random.choice(p1_solutions)]
#     lines = []
#     # this_range = random.randint(5,6)
#     for i in range(2):
#         things = list(random.choice(all_perms))
#         lines.append(f'{things[0]} {things[1]} {things[2]}\n')
#     things = list(random.choice(all_perms))
#     lines.append(f'{things[0]} {things[1]} J\n')
#     lines.append('WALK\n')
#     last_args = ''.join(lines)
#     # print(last_args)
#     # input()
#     if last_args in tried:
#         continue
#     else:
#         tried.add(last_args)
#     found = run_until_stop(inp.copy(), [ord(c) for c in last_args])
# print('lol')

# rules = '''OR A T
# AND B T
# AND C T
# NOT T J
# AND D J
# '''
# # rules = '''NOT A J
# # NOT C T
# # OR T J
# # AND D T
# # OR J J
# # AND D J
# # NOT D T
# # OR A T
# # '''
# all_perms = list(itertools.product(['AND', 'OR', 'NOT'], ['E', 'F', 'G', 'H', 'T', 'J'], ['T', 'J']))
# tried = set()
# found = 0
# while found == 0:
#     print(len(tried), end='\r')
#     # lines = [random.choice(p1_solutions)]
#     lines = []
#     # this_range = random.randint(4,5)
#     for i in range(2):
#         things = list(random.choice(all_perms))
#         lines.append(f'{things[0]} {things[1]} {things[2]}\n')
#     things = list(random.choice(all_perms))
#     lines.append(f'{things[0]} {things[1]} J\n')
#     lines.append('RUN\n')
#     last_args = rules + ''.join(lines)
#     # print(last_args)
#     # input()
#     if last_args in tried:
#         continue
#     else:
#         tried.add(last_args)
#     found = run_until_stop(inp.copy(), [ord(c) for c in last_args])
#     if found:
#         print(last_args)
#         print(f'p2: {found} (took {len(tried)} perms)')
# print('lol')