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
    bounds = set()
    for i in range(len(data) - 1, -1, -1):
        a, b = data[i], data[i - 1]
        bounds |= set(p for p in bresenham(a, b))
    # print(bounds)
    # print_2d(' ', {k:'#' for k in bounds})
    # print({(x//20 for x in k):'#' for k in bounds})
    bottom_right = max(data, key=lambda x: x[0] * x[1])
    search_line = bresenham((0, 0), bottom_right)

    SCALE = 1

    outside_point = None
    for i in range(len(search_line)):
        if search_line[i] in bounds:
            outside_point = search_line[i - 1]
            break

    expanded = set()
    for point in bounds:
        expanded |= {vadd(o, point) for o in DIAGDIRS}



    outline = {outside_point}
    frontier = {outside_point}
    while frontier:
        point = frontier.pop()
        n = [vadd(o, point) for o in DIAGDIRS]
        n = {p for p in n if p in expanded and p not in outline and p not in bounds}
        frontier |= n
        outline |= n

    print_2d(
        '  ',
        {tuple(x // SCALE for x in k): '.' for k in expanded},
        {tuple(x // SCALE for x in k): '+' for k in outline},
        {tuple(x // SCALE for x in k): '#' for k in bounds},
        # {tuple(x // SCALE for x in k): '~' for k in search_line},
        {tuple(x // SCALE for x in outside_point): '@'}
    )

    def get_inside(a, b):
        #  x1 y1 -> x2 y1 -> x2 y2 -> x1 y2
        corners = [a, (b[0], a[1]), b, (a[0], b[1])]
        # print(corners)
        # lines = set()
        for i in range(3, -1, -1):
            line = set(x for x in bresenham(corners[i], corners[i - 1]))
            if not line.isdisjoint(outline):
                return False
            # lines |= line
            # print('\t', line)
        # print_2d(' ', {tuple(x // SCALE for x in k): '#' for k in lines})
        return True

    best = 0
    for i, a in enumerate(data):
        for j, b in enumerate(data[i + 1:]):
            print(i, best, end='\r')
            if not get_inside(a, b):
                continue
            w = abs(a[0] - b[0]) + 1
            h = abs(a[1] - b[1]) + 1
            best = max(w * h, best)

    # print(len(bounds))
    return best


if __name__ == '__main__':
    setday(9)

    data = parselines(lambda x: tuple(get_ints(x)))

    print('part1:', p1())
    print('part2:', p2())
