import sys
from collections import deque


dirs = [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (0, 0, -1),
    (0, -1, 0),
    (-1, 0, 0)
]


def get_neighbors(x, y, z, b):
    n = 0
    for xo, yo, zo in dirs:
        if (x + xo, y + yo, z + zo) in b:
            n += 0
        else:
            n += 1
    return n


def p1():
    cubes = set()
    for x, y, z in data:
        cubes.add((x, y, z))
    acc = 0
    for x, y, z in cubes:
        acc += get_neighbors(x, y, z, cubes)
    # print(cubes)
    return acc


def get_air(c, b):
    x, y, z = c
    empty = set()
    filled = set()
    for xo, yo, zo in dirs:
        nx, ny, nz = (x + xo, y + yo, z + zo)
        if nx < -2 or ny < -2 or nz < -2 or nx > 22 or ny > 22 or nz > 22:
            continue
        n = (nx, ny, nz)
        if n in b:
            filled.add(n)
        else:
            empty.add(n)
    return empty, filled


def bfs(src, b):
    acc = 0
    step = 0

    q = deque([src])

    seen = set()

    while q:
        step += 1
        cur = q.popleft()

        empty, filled = get_air(cur, b)

        for n in empty:
            d = (cur, n)
            if d in seen:
                continue
            seen.add(d)
            q.append(n)

        for n in filled:
            d = (cur, n)
            if d not in seen:
                seen.add(d)
                acc += 1

    return acc

# def flood_fill(src, cubes):
#     q = deque([src])
#     seen = set()
#     while q:
#         cur = q.popleft()
#         x,y,z = cur
#         if x < -2 or y < -2 or z < -2 or x > 22 or y > 22 or z > 22:
#             continue
#
#         air = []
#         filled = []
#
#         for xo, yo, zo in dirs:
#


def p2():
    cubes = set()
    for x, y, z in data:
        cubes.add((x, y, z))

    return bfs((-1, -1, -1), cubes)


day = 18
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) for i in line.split(',')] for line in file]

print('part1:', p1())
print('part2:', p2())
