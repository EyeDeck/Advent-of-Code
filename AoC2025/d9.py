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

    # apply coordinate compression so we can handle this with discrete tiles in a reasonable time (and not mess with ranges)
    # the entire grid fits in ~250x250 this way
    data_cmp = [compress(c) for c in data]

    # map out the entire border wall in memory, as well as a set containing inner and outer outlines of the border wall
    bounds = set()
    outset = set()
    for i in range(len(data_cmp) - 1, -1, -1):
        a, b = data_cmp[i], data_cmp[i - 1]
        segment = set(p for p in bresenham(a, b))
        bounds |= segment
        outset |= {vadd(o, point) for o in DIAGDIRS for point in segment}
    outset -= bounds

    # flood fill from an arbitrary point in 'outset'; this will randomly either find the inner or outer wall
    random_point = outset.pop()
    flood_set = {random_point}
    frontier = {random_point}
    while frontier:
        point = frontier.pop()
        n = [vadd(o, point) for o in DIRS]
        n = {p for p in n if p in outset and p not in flood_set}
        frontier |= n
        flood_set |= n
    outset -= flood_set
    # the outer wall is the longer of the two sets, and also the only one we care about
    forbidden_zone = min([outset, flood_set], key=len)

    scale = 1 if '-s' not in sys.argv else int(sys.argv[sys.argv.index('-s') + 1])

    if verbose:
        print_2d(
            '  ',
            {tuple(x // scale for x in k): '.' for k in outset},
            {tuple(x // scale for x in k): '+' for k in forbidden_zone},
            {tuple(x // scale for x in k): '#' for k in bounds},
            # {tuple(x // scale for x in k): '~' for k in search_line},
            {tuple(x // scale for x in random_point): '@'}
        )

    def get_inside(a, b):
        #  x1 y1 -> x2 y1 -> x2 y2 -> x1 y2 -> x1 y1
        corners = [a, (b[0], a[1]), b, (a[0], b[1])]
        for i in range(3, -1, -1):
            line = set(bresenham(corners[i], corners[i - 1]))
            if not line.isdisjoint(forbidden_zone):
                return False
        return True

    # perform a riffle shuffle so we test alternating points earlier (results in a ~20% speed boost on my input)
    data_cmp = [data_cmp[i // 2 + i % 2 * (len(data_cmp) // 2)] for i in range(len(data_cmp))][:-1] + data_cmp[-1:]

    # now just bruteforce every pair of points
    best = 0
    for i, a in enumerate(data_cmp):
        if verbose:
            print(i, best, end='\r')
        for b in data_cmp[i + 1:]:
            # calculate the area these two points would cover, using their decompressed coordinates
            a_real, b_real = decompress(a), decompress(b)
            w = abs(a_real[0] - b_real[0]) + 1
            h = abs(a_real[1] - b_real[1]) + 1
            area = w * h
            # if the area is smaller than the previous best, skip it early
            # otherwise, just generate all 4 line segments, and see if any point in them intersects with the ~forbidden zone~
            if area > best and get_inside(a, b):
                best = max(w * h, best)

    return best


if __name__ == '__main__':
    setday(9)

    data = parselines(get_ints)

    print('part1:', p1())
    print('part2:', p2())
