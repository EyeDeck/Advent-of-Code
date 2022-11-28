import sys
import re
from collections import defaultdict


def check_overlap(a, b):
    (ax, ay, az), (aX, aY, aZ) = a
    (bx, by, bz), (bX, bY, bZ) = b
    return ax <= bX and aX >= bx and ay <= bY and aY >= by and az <= bZ and aZ >= bz


def get_overlap(a, b):
    mn = max(a[0][0], b[0][0]), max(a[0][1], b[0][1]), max(a[0][2], b[0][2])
    mx = min(a[1][0], b[1][0]), min(a[1][1], b[1][1]), min(a[1][2], b[1][2])
    return mn, mx


def insert_cuboid(cuboids, cuboid, state):
    ext = defaultdict(int)
    for ex, es in cuboids.items():
        if check_overlap(ex, cuboid):
            overlap = get_overlap(ex, cuboid)
            ext[overlap] += -es
    if state == 1:
        ext[cuboid] += 1
    for c, v in ext.items():
        if v == 0:
            continue
        cuboids[c] += v


def get_cuboid_area(c):
    return (c[1][0] - c[0][0] + 1) * (c[1][1] - c[0][1] + 1) * (c[1][2] - c[0][2] + 1)


def solve(p1):
    cum = 0
    ranges = defaultdict(int)
    for line in data:
        state, coords = line
        if p1 and (min(coords) < -50 or max(coords) > 50):
            continue
        state = 1 if state == 'on' else -1
        xs, ys, zs = coords[0:2], coords[2:4], coords[4:6]
        insert_cuboid(ranges, ((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))), state)

    for c, v in ranges.items():
        if v == 0:
            continue
        cum += get_cuboid_area(c) * v
        # print(c,v)
    return cum


day = 22
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

exp = re.compile('([-\d]+)')
with open(f) as file:
    data = [(line.split(' ')[0], [int(i) for i in re.findall(exp, line)]) for line in file]

print(f'part1: {solve(True)}')
print(f'part2: {solve(False)}')
