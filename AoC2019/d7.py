import copy
import itertools
import sys


# Returns a tuple:
#   When 'output' opcode 4 is hit, returns (output, instruction_pointer)
#     Program may be resumed by calling this function again with new args and the same pointer
#   When 'stop' opcode 99 is hit, returns (None, instruction_pointer)
#   If an invalid opcode is hit, returns (None, None)
def intcode(p, args, ptr=0):
    #    print('args:', args)
    arg_i = 0
    while True:
        op = get_op(p, ptr)

        if op is None:
            return None, None

        if op[0] == 1:  # add
            p[op[3][0]] = get_val(p, op[1]) + get_val(p, op[2])
        elif op[0] == 2:  # mul
            p[op[3][0]] = get_val(p, op[1]) * get_val(p, op[2])
        elif op[0] == 3:  # input
            p[op[1][0]] = args[arg_i]
            arg_i += 1
        elif op[0] == 4:  # output
            ptr += len(op)
            return get_val(p, op[1]), ptr
        elif op[0] == 5:  # jump if true
            if get_val(p, op[1]) != 0:
                ptr = get_val(p, op[2])
                continue
        elif op[0] == 6:  # jump if false
            if get_val(p, op[1]) == 0:
                ptr = get_val(p, op[2])
                continue
        elif op[0] == 7:  # less than
            p[op[3][0]] = 1 if get_val(p, op[1]) < get_val(p, op[2]) else 0
        elif op[0] == 8:  # equals
            p[op[3][0]] = 1 if get_val(p, op[1]) == get_val(p, op[2]) else 0
        # elif op[0] == 9:  # output (ascii, /g/ special)
        #    print(chr(get_val(p, op[1])), end='')
        elif op[0] == 99:
            return None, ptr
        else:
            print('unknown opcode')
        # print(p)
        ptr += len(op)


def get_op(p, ptr):
    op = [p[ptr] % 100]

    if op[0] not in opcodes:
        return None

    ln = opcodes[op[0]][1]
    modes = [int(i) for i in str(p[ptr] // 100)[::-1]]
    modes.extend([0 for _ in range(ln - len(modes) - 1)])
#    print(p[ptr], op, modes)

    for i in range(1, ln):
        op.append((p[ptr + i], modes[i - 1]))
    return op


def get_val(p, op):
    return p[op[0]] if op[1] == 0 else op[0]


# asm, args
opcodes = {
    1: ('add', 4),
    2: ('mul', 4),
    3: ('store', 2),
    4: ('get', 2),
    5: ('jmpt', 3),
    6: ('jmpf', 3),
    7: ('lt', 4),
    8: ('eq', 4),
    # 9: ('ascii', 2),  # /g/ special
    99: ('stop', 1)
}

f = 'd7.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
# print(intcode(copy.deepcopy(inp), [0, 0]))

perms = list(itertools.permutations(range(0, 5)))
p1 = 0
for p in perms:
    v = 0
    for i in range(0, 5):
        v = intcode(copy.deepcopy(inp), [p[i], v])[0]
        if v is None:
            break

    if v > p1:
        p1 = v

perms = list(itertools.permutations(range(5, 10)))
p2 = 0
last_e = 0
for p in perms:
    states = [copy.deepcopy(inp) for _ in range(0, 5)]
    ptrs = [0 for _ in range(0, 5)]
    v = 0
    first_run = True
    do_exit = False
    while not do_exit:
        for i in range(0, 5):
            to_pass = [p[i], v] if first_run else [v]
            v = intcode(states[i], to_pass, ptrs[i])
            # print(states[i])

            if v[0] is None:
                do_exit = True
                break

            ptrs[i] = v[1]
            if i == 4:
                last_e = v[0]

            v = v[0]

        if do_exit:
            break
        first_run = False
    if last_e > p2:
        p2 = last_e

print('p1: {}\np2: {}'.format(p1, p2))
