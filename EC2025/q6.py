from ec import *


def p1():
    data = parse_lines(1)[0]
    acc = 0
    for i in range(len(data)):
        if data[i] != 'A':
            continue
        acc += sum(data[j] == 'a' for j in range(i, len(data)))
    return acc


def p2():
    data = parse_lines(2)[0]
    acc = 0
    for i in range(len(data)):
        if data[i] not in 'ABC':
            continue
        novice = data[i].lower()
        acc += sum(data[j] == novice for j in range(i, len(data)))

    return acc


def p3():
    def result_with_data(data, range_l, range_r):
        acc = 0
        dlen = len(data)

        for i in range(range_l, range_r):
            if data[i] not in 'ABC':
                continue
            novice = data[i].lower()
            acc += sum(data[j] == novice for j in range(max(0, i - DIST), min(i + DIST + 1, dlen)))

        return acc

    data = parse_lines(3)[0]
    dlen = len(data)
    duped_data = data * 3

    DUPE = 1000
    DIST = 1000

    acc = result_with_data(duped_data, 0, dlen)
    acc += result_with_data(duped_data, dlen, dlen*2) * (DUPE-2)
    acc += result_with_data(duped_data, dlen*2, dlen*3)

    return acc


setquest(6)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
