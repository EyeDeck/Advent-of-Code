import sys


def p1():
    length = len(data[0])
    cmn = [[0 for _ in range(length)], [0 for _ in range(length)]]
    for line in data:
        for i, c in enumerate(line):
            cmn[int(c)][i] += 1
    print(cmn)
    gamma, epsilon = '', ''
    for i in range(len(cmn[0])):
        if cmn[0][i] > cmn[1][i]:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'

    return int(gamma, 2) * int(epsilon, 2)


def p2():
    length = len(data[0])

    oxygen = data.copy()
    for i in range(length):
        cmn = [0, 0]
        for line in oxygen:
            cmn[int(line[i])] += 1
        tgt = '1' if cmn[1] >= cmn[0] else '0'
        oxygen = [c for c in oxygen if c[i] == tgt]
        if len(oxygen) == 1:
            break

    co2 = data.copy()
    for i in range(length):
        cmn = [0, 0]
        for line in co2:
            cmn[int(line[i])] += 1
        tgt = '1' if cmn[1] < cmn[0] else '0'
        co2 = [c for c in co2 if c[i] == tgt]
        if len(co2) == 1:
            break

    return int(oxygen[0], 2) * int(co2[0], 2)


day = 3
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

print(f'part1: {p1()}')
print(f'part2: {p2()}')
