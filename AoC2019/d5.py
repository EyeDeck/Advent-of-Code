import sys

def intcode(p):
    ptr = 0
    while True:
        op = get_op(p, ptr)

        if op[0] == 1:  # add
            p[op[3][0]] = get_val(p, op[1]) + get_val(p, op[2])
        elif op[0] == 2:  # mul
            p[op[3][0]] = get_val(p, op[1]) * get_val(p, op[2])
        elif op[0] == 3:  # input
            p[op[1][0]] = int(input("Input: "))
        elif op[0] == 4:  # output
            print(get_val(p, op[1]))
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
        elif op[0] == 9:  # output (ascii, /g/ special)
            print(chr(get_val(p, op[1])), end='')
        elif op[0] == 99:
            return p
        # print(p)
        ptr += len(op)


def get_op(p, ptr):
    op = [p[ptr] % 100]
    ln = opcodes[op[0]][1]
    modes = str(p[ptr] // 100)[::-1]
    modes += '0' * (ln - len(modes) - 1)
    # print(op, modes, p[ptr])
    if op[0] not in opcodes:
        print('invalid opcode', op, modes)
        sys.exit()
    for i in range(1, ln):
        op.append((p[ptr + i], int(modes[i - 1])))
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
    9: ('ascii', 2),  # /g/ special
    99: ('stop', 1)
}


f = 'd5.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
intcode(inp)

# inpt = '3,9,8,9,10,9,4,9,99,-1,8'
# inpt = '3,9,7,9,10,9,4,9,99,-1,8'
# inpt = '3,3,1108,-1,8,3,4,3,99'
# inpt = '3,3,1107,-1,8,3,4,3,99'
# inpt = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
# inpt = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
# inp = [int(i) for i in inpt.split(',')]
