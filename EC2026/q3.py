import math

from ec import *


def p1():
    data = parse_lines(1)
    acc = 0
    for line in data:
        l, r = line.split('-')[1].split(' ')

        for i in range(4):
            acc += (int(l[i]) ** (3-i)) * (int(r[i]))

    return acc


def p2():
    data = parse_lines(2)
    acc = 0
    for line in data:
        l, r = line.split('-')[1].split(' ')
        r_len = len(r)
        l = l[::-1]*r_len
        print(l,r)

        temp = 0
        for i in range(r_len):
            d = l[-i-1]
            print(d, (r_len-i-1), r[i], (int(d) ** (r_len-i-1)) * (int(r[i])))
            temp += (int(d) ** (r_len-i-1)) * (int(r[i]))
        print(temp)
        acc += temp

    return acc


def calc_int(l,r):
    l = l[::-1] * math.ceil(len(r) / len(l))
    r = r[::-1]
    acc = 0
    for i in range(len(r)):
        acc += int(l[i]) ** i * int(r[i])
    return acc


def p2():
    data = parse_lines(2)
    acc = 0
    for line in data:
        l, r = line.split('-')[1].split(' ')
        acc += calc_int(l, r)

    return acc


def p3():
    data = parse_lines(3)
    acc = 0
    m_l, m_r = 0, 0
    for line in data:
        l, r = line.split('-')[1].split(' ')

        m_l = max(m_l, int(l))
        m_r = max(m_r, int(r))
    print(m_l, m_r)
    smallest = {}
    for x in range(m_l):
        for y in range(m_r):
            i = calc_int(str(x), str(y))
            if i not in smallest:
                smallest[i] = [x, y]
        if x % 1000 == 0:
            print(x, '...')
            print(smallest, '\n', len(smallest), '\n\n')
    return


def p3():
    data = parse_lines(3)
    acc = 0
    for line in data:
        l, r = line.split('-')[1].split(' ')
        line_int = calc_int(l, r)
        for i in range(int(r)):
            if calc_int(l, str(i)) == line_int:
                print(f'{line} invalid (ISO-{l} {i})')
                break
        else:
            print(line, 'valid')
            acc += line_int
    return acc


if __name__ == '__main__':
    setquest(3)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
