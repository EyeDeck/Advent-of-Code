import sys
from collections import deque


def p1():
    dirs = [
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
    ]

    def get_neighbors(x, y, z, b):
        n = 0
        for xo, yo, zo in dirs:
            if (x + xo, y + yo, z + zo) in b:
                n += 0
            else:
                # interestingly we can simply double-count positive directions, because for every
                # double-counted face, there's exactly 1 opposite uncounted face, and it evens out
                n += 2
        return n

    return sum(get_neighbors(*c, cubes) for c in cubes)


def p2():
    dirs = [
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (0, 0, -1),
        (0, -1, 0),
        (-1, 0, 0),
    ]

    def get_air(x,y,z, b):
        empty = set()
        filled = 0
        for xo, yo, zo in dirs:
            nx, ny, nz = (x + xo, y + yo, z + zo)
            if nx < mn[0] or ny < mn[1] or nz < mn[2] or nx > mx[0] or ny > mx[1] or nz > mx[2]:
                continue
            n = (nx, ny, nz)
            if n in b:
                filled += 1
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

            empty, filled = get_air(*cur, b)
            acc += filled

            for n in empty:
                if n in seen:
                    continue
                seen.add(n)
                q.append(n)
        return acc
    return bfs((-1, -1, -1), cubes)


day = 18
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) for i in line.split(',')] for line in file]

    cubes = set()
    mn, mx, = [2**32, 2**32, 2**32], [0, 0, 0]
    for x, y, z in data:
        mn, mx = [min(mn[0], x), min(mn[1], y), min(mn[2], z)], [max(mx[0], x), max(mx[1], y), max(mx[2], z)]
        cubes.add((x, y, z))
    mn, mx = [i-2 for i in mn], [i+2 for i in mx]

print('part1:', p1())
print('part2:', p2())
