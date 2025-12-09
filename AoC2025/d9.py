from aoc import *


def p1():
    best = 0
    for i, a in enumerate(data):
        for j, b in enumerate(data[i + 1:]):
            w = abs(a[0] - b[0]) + 1
            h = abs(a[1] - b[1]) + 1
            best = max(w * h, best)
    return best


def p2():
    x_to_cmp = {k: v for v, k in enumerate(sorted({c[0] for c in data}))}
    y_to_cmp = {k: v for v, k in enumerate(sorted({c[1] for c in data}))}

    def compress(c):
        return x_to_cmp[c[0]], y_to_cmp[c[1]]

    cmp_to_x = {k: v for v, k in x_to_cmp.items()}
    cmp_to_y = {k: v for v, k in y_to_cmp.items()}

    def decompress(c):
        return cmp_to_x[c[0]], cmp_to_y[c[1]]

    data_cmp = [compress(c) for c in data]

    bounds = set()
    for i in range(len(data_cmp) - 1, -1, -1):
        a, b = data_cmp[i], data_cmp[i - 1]
        bounds |= set(p for p in bresenham(a, b))

    bottom_right = max(data_cmp, key=lambda x: x[0] * x[1])
    search_line = bresenham((-1, -1), bottom_right)

    outside_point = None
    for i in range(len(search_line)):
        if search_line[i] in bounds:
            outside_point = search_line[i - 1]
            break

    expanded = set()
    for point in bounds:
        expanded |= {vadd(o, point) for o in DIAGDIRS}

    forbidden_zone = {outside_point}
    frontier = {outside_point}
    while frontier:
        point = frontier.pop()
        n = [vadd(o, point) for o in DIAGDIRS]
        n = {p for p in n if p in expanded and p not in forbidden_zone and p not in bounds}
        frontier |= n
        forbidden_zone |= n

    scale = 1 if '-s' not in sys.argv else int(sys.argv[sys.argv.index('-s') + 1])

    if verbose:
        print_2d(
            '  ',
            {tuple(x // scale for x in k): '.' for k in expanded},
            {tuple(x // scale for x in k): '+' for k in forbidden_zone},
            {tuple(x // scale for x in k): '#' for k in bounds},
            # {tuple(x // scale for x in k): '~' for k in search_line},
            {tuple(x // scale for x in outside_point): '@'}
        )

    def get_inside(a, b):
        #  x1 y1 -> x2 y1 -> x2 y2 -> x1 y2 -> x1 y1
        corners = [a, (b[0], a[1]), b, (a[0], b[1])]
        for i in range(3, -1, -1):
            line = set(x for x in bresenham(corners[i], corners[i - 1]))
            if not line.isdisjoint(forbidden_zone):
                return False
        return True

    best = 0
    for i, a in enumerate(data_cmp):
        if verbose:
            print(i, best, end='\r')
        for j, b in enumerate(data_cmp[i + 1:]):
            if not get_inside(a, b):
                continue
            a_real, b_real = decompress(a), decompress(b)
            w = abs(a_real[0] - b_real[0]) + 1
            h = abs(a_real[1] - b_real[1]) + 1
            best = max(w * h, best)

    return best


if __name__ == '__main__':
    setday(9)

    data = parselines(lambda x: tuple(get_ints(x)))

    print('part1:', p1())
    print('part2:', p2())
