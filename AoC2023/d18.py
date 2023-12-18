from aoc import *

dir_map = {
    'R': (1, 0),
    'U': (0, -1),
    'L': (-1, 0),
    'D': (0, 1),
}

def p1():
    grid = {(0,0)}

    pos = (0,0)
    for line in data:
        d, n, color = line.split(' ')
        n = int(n)

        # print(d,n, color)
        for i in range(n):
            pos = vadd(dir_map[d], pos)
            grid.add(pos)

    stack = {(1,1)}
    while stack:
        cur = stack.pop()
        grid.add(cur)
        for d in DIRS:
            nxt = vadd(cur, d)
            if nxt in grid:
                continue
            stack.add(nxt)

    # print_2d(' ', {c:'.' for c in grid}, {(0,0):'0'}, constrain=(-1000, -1000, 1000, 1000))
    return len(grid)


def shoelace(p):
    return abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(p))) // 2

def segments(p):
    return zip(p, p[1:] + [p[0]])

def p2():
    perimeter = []
    vertices = []
    pos = (0,0)
    perimeter_len = 0
    for line in data:
        _, _, ins = line.split(' ')
        d, n = int(ins[-2]), int(ins[2:-2], 16)

    # pos = (0, 0)
    # for line in data:
    #     d, n, color = line.split(' ')
    #     print(DIRS.index(dir_map[d]))
    #     d = DIRS.index(dir_map[d])
    #     n = int(n)
        perimeter_len += n

        # print(d,n)



        start_pos = pos
        end_pos = vadd(vmul((n,n), DIRS[d]), pos)
        perimeter.append((start_pos, end_pos))
        vertices.append(start_pos)
        pos = end_pos
    # print(perimeter)
    # print(vertices)

    # area = polygonArea(vertices)
    # perimeter = sum(abs(n[0]-n[1])-1 for n in vertices)
    #
    # x, y = zip(*vertices)
    # area = area_by_shoelace(x, y)

    print(vertices)
    area = shoelace(vertices)

    # print_2d('  _   ', {k:k for k in vertices})

    print(area, perimeter_len)

    return area + perimeter_len//2 + 1

setday(18)

data = parselines()
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
