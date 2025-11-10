from ec import *


def p1():
    data = parse_lines(1)[0]
    acc = 0
    for i in range(len(data)):
        # print(data[i])
        if data[i] != 'A':
            continue
        acc += sum(data[j] == 'a' for j in range(i, len(data)))
        # print([data[j] == 'a' for j in range(i, len(data))])
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    # print(data)

    return acc



def p2():
    data = parse_lines(2)[0]
    acc = 0
    for i in range(len(data)):
        # print(data[i])
        if data[i] not in 'ABC':
            continue
        # mentor = data[i]
        novice = data[i].lower()
        acc += sum(data[j] == novice for j in range(i, len(data)))
        # print([data[j] == 'a' for j in range(i, len(data))])
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    # print(data)

    return acc

#
# def result_with_data(data, range_l, range_r):
#
#     acc = 0
#     dlen = len(data)
#     for i in range(dlen):
#         if data[i] not in 'ABC':
#             continue
#         novice = data[i].lower()
#         acc += sum(data[j] == novice for j in range(max(0, i-1001), min(i+1001, dlen)))
#         if i % 100000 == 0:
#             print(max(i, i-1000), min(i+1000, dlen))
#
#     return acc
#
# def p3():
#     data = parse_lines(3)[0]
#     acc = 0
#
#     data = parse_lines(3)[0] * 1000


def p3():
    data = parse_lines(3)[0] * 1000
    print(len(parse_lines(3)[0]))
    print(len(parse_lines(3)[0].strip()))
    acc = 0
    dlen = len(data)
    for i in range(dlen):
        # print(data[i])
        if data[i] not in 'ABC':
            continue
        # mentor = data[i]
        novice = data[i].lower()
        acc += sum(data[j] == novice for j in range(max(0, i-1000), min(i+1001, dlen)))
        if i % 100000 == 0:
            print(max(i, i-1000), min(i+1000, dlen))
        # print([data[j] == 'a' for j in range(i, len(data))])
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    # print(data)

    return acc


setquest(6)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
