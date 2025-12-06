from aoc import *


def p1():
    data = parselines(lambda x: x.split())

    acc = 0
    w, h = len(data[0]), len(data)
    for y in range(w):
        col = [data[x][y] for x in range(h)]
        op = col[-1]
        ns = [int(s) for s in col[:-1]]
        if op == '*':
            acc += math.prod(ns)
        else:
            acc += sum(ns)

    return acc


def p2():
    grid, inverse, unique = parsegrid()

    bounds = grid_bounds(grid)

    print_2d(' ', grid)

    print(bounds)

    acc = 0

    op = None
    numbers = []
    for x in range(bounds[2], -1, -1):
        digits = []
        clear_flag = False
        for y in range(bounds[3]+1):
            pos = (x,y)
            if pos not in grid:
                continue
            c = grid[pos]
            print('c:', c)
            if c.isnumeric():
                digits.append(c)
            if c in {'+', '*'}:
                if c == '+':
                    op = sum
                else:
                    op = math.prod
                clear_flag = True
            print(digits)

        if digits:
            numbers.append(int(''.join(digits)))
            digits.clear()

        print(numbers)

        if clear_flag:
            acc += op(numbers)
            numbers.clear()

        print(x)

    return acc


if __name__ == '__main__':
    setday(6)

    print('part1:', p1() )
    print('part2:', p2() )
