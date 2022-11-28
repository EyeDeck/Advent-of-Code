import copy
import sys
from collections import defaultdict


# Returns a tuple:
#   When 'output' opcode 4 is hit, returns (output, instruction_pointer)
#     Program may be resumed by calling this function again with new args and the same pointer
#   When 'stop' opcode 99 is hit, returns (None, instruction_pointer)
#   If an invalid opcode is hit, returns (None, None)
def intcode(p, args, ptr=0, rb=0):
    arg_i = 0
    while True:
        op = get_op(p, ptr)
        if op is None:
            return None, None, None

        if op[0] == 1:  # add
            write_val(p, op[3], rb, get_val(p, op[1], rb) + get_val(p, op[2], rb))
        elif op[0] == 2:  # mul
            write_val(p, op[3], rb, get_val(p, op[1], rb) * get_val(p, op[2], rb))
        elif op[0] == 3:  # input
            write_val(p, op[1], rb, args[arg_i])
            arg_i += 1
        elif op[0] == 4:  # output
            ptr += len(op)
            return get_val(p, op[1], rb), ptr, rb
        elif op[0] == 5:  # jump if true
            if get_val(p, op[1], rb) != 0:
                ptr = get_val(p, op[2], rb)
                continue
        elif op[0] == 6:  # jump if false
            if get_val(p, op[1], rb) == 0:
                ptr = get_val(p, op[2], rb)
                continue
        elif op[0] == 7:  # less than
            write_val(p, op[3], rb, 1 if get_val(p, op[1], rb) < get_val(p, op[2], rb) else 0)
        elif op[0] == 8:  # equals
            write_val(p, op[3], rb, 1 if get_val(p, op[1], rb) == get_val(p, op[2], rb) else 0)
        elif op[0] == 9:
            rb += get_val(p, op[1], rb)
        elif op[0] == 99:
            return None, ptr, rb
        else:
            print('unknown opcode')
            return None, None, None
        ptr += len(op)


def get_op(p, ptr):
    op = [p[ptr] % 100]

    if op[0] not in opcodes:
        return None

    ln = opcodes[op[0]][1]
    modes = [int(i) for i in str(p[ptr] // 100)[::-1]]
    modes.extend([0 for _ in range(ln - len(modes) - 1)])
    # print(p[ptr], op, modes)

    for i in range(1, ln):
        op.append((p[ptr + i], modes[i - 1]))
    return op


def get_val(p, op, rb):
    if op[1] == 0:
        return p[op[0]]
    elif op[1] == 1:
        return op[0]
    else:
        return p[rb + op[0]]


def write_val(p, op, rb, val):
    if op[1] == 0:
        p[op[0]] = val
    elif op[1] == 1:
        p[0] = val
    else:
        p[rb + op[0]] = val


def run_until_stop(p, args):
    out = []
    ptr = 0
    rb = 0
    while True:
        o, ptr, rb = intcode(p, args, ptr, rb)
        if o is None:
            break
        out.append(o)
    return out


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
    9: ('rb', 2),
    99: ('stop', 1)
}

f = 'd9.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})

print(run_until_stop(copy.deepcopy(inp), [1]))
print(run_until_stop(copy.deepcopy(inp), [2]))
