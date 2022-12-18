import sys
from collections import deque
from operator import itemgetter


def p1():
    return sum(sum([0 if ((x + d[0], y + d[1], z + d[2]) in cubes) else 2 for d in [(0, 0, 1), (0, 1, 0), (1, 0, 0)]]) for x, y, z in cubes)


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
        q = deque([src])
        seen = set()
        while q:
            cur = q.popleft()

            empty, filled = get_air(*cur, b)
            acc += filled

            for n in empty:
                if n in seen:
                    continue
                seen.add(n)
                q.append(n)
        return acc
    return bfs((*mn,), cubes)


day = 18
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    cubes = set(tuple(int(i) for i in line.split(',')) for line in file)

    mn = [min(*cubes, key=itemgetter(i))[i] - 2 for i in range(3)]
    mx = [max(*cubes, key=itemgetter(i))[i] + 2 for i in range(3)]

print('part1:', p1())
print('part2:', p2())
