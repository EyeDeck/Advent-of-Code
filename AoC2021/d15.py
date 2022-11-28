from aoc import *


def heuristic(a, b):
    (x1, y1) = a[0], a[1]
    (x2, y2) = b[0], b[1]
    return abs(x1 - x2) + abs(y1 - y2)


def getneighbors(c):
    r = []
    for d in DIRS:
        dr = (d[0] + c[0], d[1] + c[1])
        if dr in data:
            r.append((dr, data[dr]))
    return r


def p1():
    # holy crap my existing astar function worked with zero modification
    path = astar(start, (w - 1, h - 1), getneighbors, lambda a, b: 0)  #
    if '--print' in sys.argv:
        print_2d(' ', data, {k: '.' for k in path})
    return sum([data[k] for k in path[1:]])


def p2():
    global data
    new_data = {}
    for (x, y), v in data.items():
        for a in range(5):
            for b in range(5):
                extra = a + b
                new_data[x + a * w, y + b * h] = (v + extra - 1) % 9 + 1
    data = new_data  # need to change the base data because getneighbors is hardcoded
    path = astar(start, ((w * 5) - 1, (h * 5) - 1), getneighbors, lambda a, b: 0)
    if '--print' in sys.argv:
        print_2d(' ', data, {k: '.' for k in path}, constrain=(0, 0, w * 5, h * 5))
    return sum([data[k] for k in path[1:]])


day = 15
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = {}
    for y, line in enumerate(file):
        for x, c in enumerate(line.strip()):
            data[x, y] = int(c)
    start = (0, 0)
    w, h = max(set(x[0] for x in data.keys())) + 1, max(set(y[1] for y in data.keys())) + 1

print(f'part1: {p1()}')
print(f'part2: {p2()}')
