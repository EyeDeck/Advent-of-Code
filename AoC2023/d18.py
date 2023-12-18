from aoc import *


def get_vertices(instructions):
    pos = (0,0)
    perimeter_len = 0
    vertices = []
    for d, n in instructions:
        vertices.append(pos)
        pos = vadd(vmul((n,n), DIRS[d]), pos)
        perimeter_len += n
    return vertices, perimeter_len


def get_area(v, p):
    # formula copied from https://stackoverflow.com/a/451482
    return abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in zip(v, v[1:] + [v[0]]))) // 2  + p//2 + 1


def solve(p2):
    instructions = []
    for line in data:
        if p2:
            _, _, ins = line.split(' ')
            d = int(ins[-2])
            n = int(ins[2:-2], 16)
        else:
            d, n, _ = line.split(' ')
            d = 'RDLU'.index(d)
            n = int(n)
        instructions.append((d,n))
    return get_area(*get_vertices(instructions))

setday(18)

data = parselines()

print('part1:', solve(False) )
print('part2:', solve(True) )
