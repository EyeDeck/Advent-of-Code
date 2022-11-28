# accidentally nuked original code
# oh well, it was shit anyway
import sys


def intcode(p):
    ptr = 0
    while True:
        op = get_op(p, ptr)
        # if p := ops[op[0]](p, *op[1:]):
        #     pass
        # elif p[ptr] == 99:
        #     return p

        if p[ptr] == 1:
            p[op[3]] = p[op[1]] + p[op[2]]
        elif p[ptr] == 2:
            p[op[3]] = p[op[1]] * p[op[2]]
        elif p[ptr] == 'jmp':
            ptr = p[op]
        elif p[ptr] == 99:
            return p
        ptr += len(op)


def get_op(p, index):
    op = [p[index]]
    if op[0] not in opcodes:
        return [p[index]]
    for i in range(1, opcodes[op[0]][1]):
        op.append(p[index + i])
    return op


# def mutate(prog, ptr, new):
#     prog[ptr] = new
#     return prog
# ops = {
#     1: lambda prog, verb, noun, ptr: mutate(prog, ptr, verb+noun),
#     2: lambda prog, verb, noun, ptr: mutate(prog, ptr, verb*noun),
#     99: lambda prog: prog
#     # 2: lambda prog, verb, noun, ptr: verb * noun
# }

# asm, args
opcodes = {
    1: ('add', 4),
    2: ('mul', 4),
    99: ('stop', 1)
}

inp = [int(i) for i in open('d2.txt').read().split(',')]

p1 = inp[0:]
p1[1], p1[2] = 12, 2
intcode(p1)
print("p1:", p1[0])

for i in range(99,-1,-1):
    for j in range(99,-1,-1):
        p2 = inp[0:]
        p2[1], p2[2] = i, j
        intcode(p2)
        if p2[0] == 19690720:
            print("p2:", (100 * i + j))
            sys.exit()
        # print(p2[0])
