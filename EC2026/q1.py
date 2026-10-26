from ec import *
import math


def p1():
    data = parse_lines(1, get_ints)[0]
    acc = 0
    for i in data:
        nearest_sq = math.ceil(math.sqrt(i)) ** 2
        acc += nearest_sq - i
    return acc


def p2():
    data = parse_lines(2, get_ints)[0]
    acc = 0
    def border(n):
        return n*4 + 4
    b_n = 1
    b = border(b_n)
    for i in data:
        while i > b:
            b_n += 1
            b = border(b_n)

        acc += b - i
    return acc


def p3():
    data = parse_lines(3, get_ints)[0]
    acc = 0
    for i in data:
        sq = math.ceil(math.sqrt(i))
        if sq & 1 == 0:
            sq += 1
        nearest_sq = sq ** 2 - 1
        n = nearest_sq - i
        if n < 0:
            n = ((sq+2)**2 - 1) - i
        acc += n
        print(i, sq, nearest_sq, n)
    return acc


if __name__ == '__main__':
    setquest(1)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
