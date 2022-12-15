from collections import *
from aoc import *

corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]]


def diam(x, y, r):
    points = set()
    for x_mod, y_mod in corners:
        n = 0
        for i in range(r, -1, -1):
            # print(i,n, (x_mod*i), (y_mod*n))
            points.add((x + (x_mod * i), y + (y_mod * n)))
            n += 1
            # print_2d('.', points)
    return points


def p1():
    tgt_line = 2000000
    sensors = {}
    tgt_borders = set()
    beacons = {}
    for sensor, coords in enumerate(data):
        a, b, x, y = coords
        # sensors[a, b] = chr(65 + sensor)
        beacons[x, y] = chr(97 + sensor)
        r = sum([abs(n) for n in vsub((a, b), (x, y))])
        sensors[a, b] = r
        print(sensor, a, b, x, y, r, '               ', end='\r')

        range_diamond = diam(a, b, r)
        tgt_borders.update(coord for coord in range_diamond if coord[1] == tgt_line)
        sensors.update({k: '#' for k in range_diamond})

    l_bound, r_bound = min(tgt_borders)[0], max(tgt_borders)[0]
    print(l_bound, r_bound)

    acc = 0
    for x in range(l_bound, r_bound + 1):
        if (x, tgt_line) not in beacons:
            acc += 1

    # print_2d('. ', sensors, {k:'!' for k in tgt_borders})

    # diam(0,0,10)
    return acc


def p2():
    x_slices = defaultdict(list)
    for sensor, coords in enumerate(data):
        print('calcing slices for sensor', sensor, end='\r')
        a, b, x, y = coords
        r = sum([abs(n) for n in vsub((a, b), (x, y))])

        for r_off in range(-r, r + 1):
            x_off = r - abs(r_off)
            x_slices[a + r_off].append((b - x_off, b + x_off))

    print('condensing overlaps on x axis...')
    x_slices_overlapped = {k: overlap_ranges(v) for k, v in x_slices.items()}

    print('finding gaps on x axis...')
    points = set()
    for x, ranges in x_slices_overlapped.items():
        # print(x, ':', ranges)
        for i in range(len(ranges) - 1):
            l, r = ranges[i], ranges[i + 1]
            ll, lr = l
            rl, rr = r
            if lr == rl - 2:
                points.add((x, lr + 1))
    del x_slices

    y_slices = defaultdict(list)
    for sensor, coords in enumerate(data):
        print('calcing slices for sensor', sensor, end='\r')
        a, b, x, y = coords
        r = sum([abs(n) for n in vsub((a, b), (x, y))])

        for r_off in range(-r, r + 1):
            x_off = r - abs(r_off)
            y_slices[b + r_off].append((a - x_off, a + x_off))

    print('condensing overlaps on y axis...')
    y_slices_overlapped = {k: overlap_ranges(v) for k, v in y_slices.items()}

    print('matching gaps on y axis...')
    for y, ranges in y_slices_overlapped.items():
        # print(x, ':', ranges)
        for i in range(len(ranges) - 1):
            l, r = ranges[i], ranges[i + 1]
            ll, lr = l
            rl, rr = r
            if lr == rl - 2:
                if (lr + 1, y) in points:
                    return (lr + 1) * 4000000 + y


def overlap_ranges(ranges):
    ranges = sorted(ranges, key=itemgetter(1))
    pos = len(ranges) - 1
    while pos > 0:
        l, r = ranges[pos - 1], ranges[pos]
        ll, lr = l
        rl, rr = r
        if lr >= rl:
            ranges[pos - 1] = (ll, max(lr, rr))
            ranges.pop(pos)
        pos -= 1
    return ranges


day = 15
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) for i in re.findall(r'[\-0-9]+', line)] for line in file]

# print('part1:', p1())
print('part2:', p2())
