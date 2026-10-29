import math

from ec import *


def calc_int(l,r):
    l = l[::-1] * math.ceil(len(r) / len(l))
    r = r[::-1]
    acc = 0
    for i in range(len(r)):
        acc += int(l[i]) ** i * int(r[i])
    return acc


def solve(part, validate):
    if verbose:
        print()

    data = parse_lines(part)
    acc = 0
    for line in data:
        l, r = line.split('-')[1].split(' ')
        line_int = calc_int(l, r)

        if not validate:
            acc += line_int

            if verbose:
                print(f'{line} = {line_int}')
        else:
            # doing `for i in range(int(r)-1, -1, -1):` instead is significantly faster,
            # but doesn't produce the 'valid' ISO2 standard number when --verbose is on
            for i in range(int(r)):
                if calc_int(l, str(i)) == line_int:
                    if verbose:
                        print(f'{line} invalid (ISO2-{l} {i}) = {line_int}')
                    break
            else:
                acc += line_int

                if verbose:
                    print(f'{line} valid = {line_int}')
    return acc


if __name__ == '__main__':
    setquest(3)

    print('part1:', solve(1, False))
    print('part2:', solve(2, False))
    print('part3:', solve(3, True))
