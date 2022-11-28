import sys
raw = open("d2.txt").read().split(',')


def intcode(p):
    ptr = 0
    for i in range(0, len(p), 4):
        op = (p[i], p[i + 1], p[i + 2], p[i + 3])
        ptr += 4

        if op[0] == 1:
            p[op[3]] = p[op[1]] + p[op[2]]
        elif op[0] == 2:
            p[op[3]] = p[op[1]] * p[op[2]]
        elif op[0] == 99:
            p.append(ptr)
            return p


p1 = [int(i) for i in raw]
p1[1] = 12
p1[2] = 2
intcode(p1)
print("p1:", p1[0])

for j in range(0, 100):
    for k in range(0, 100):
        inp = [int(i) for i in raw]
        # print(inp)
        inp[1] = j
        inp[2] = k

        pointer = 0
        for i in range(0, len(inp), 4):
            op = (inp[i], inp[i + 1], inp[i + 2], inp[i + 3])
            pointer += 4
            # print(op)
            if op[0] == 1:
                inp[op[3]] = inp[op[1]] + inp[op[2]]
            elif op[0] == 2:
                inp[op[3]] = inp[op[1]] * inp[op[2]]
            elif op[0] == 99:
                # print(pointer,j,k)
                # print(inp[0])
                if inp[0] == 19690720:
                    print("p2:", (100 * j + k), k, j)
                    sys.exit()
                break

# print("p1:", inp[0])


