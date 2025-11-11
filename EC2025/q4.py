import math

from ec import *


def p1():
    data = [l[0] for l in parse_lines(1, get_ints)]
    macc = 1
    for i in range(len(data)-1):
        a,b = data[i], data[i+1]
        macc *= a / b
        print(a/b, macc)

    print(data)
    return math.floor(macc * 2025)


def p2():
    data = [l[0] for l in parse_lines(2, get_ints)]
    macc = 1
    for i in range(len(data)-1):
        a,b = data[i], data[i+1]
        macc *= a / b
        print(a/b, macc)

    print(data)
    return math.ceil(10000000000000 / macc)


def p3():
    data = [l for l in parse_lines(3, get_ints)]
    data[0].append(data[0][0])
    data[-1].append(data[-1][0])
    macc = 1
    for i in range(len(data)-1):
        a,b = data[i][1], data[i+1][0]
        macc *= a / b
        print(a/b, macc)
    print(data)

    return math.floor(macc * 100)


setquest(4)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
