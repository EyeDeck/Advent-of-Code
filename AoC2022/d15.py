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
    y_slices = defaultdict(list)
    x_slices = defaultdict(list)
    for sensor, coords in enumerate(data):
        print('calcing slices for sensor', sensor, end='\r')
        a, b, x, y = coords
        r = sum([abs(n) for n in vsub((a, b), (x, y))])
        # print('#', sensor, (a,b), r)

        for r_off in range(-r, r + 1):
            x_off = r - abs(r_off)
            # print(x_off, r_off)
            x_slices[a + r_off].append((b - x_off, b + x_off))
            y_slices[b + r_off].append((a - x_off, a + x_off))

    # print('\nsorting x slices...')
    # x_slices = {k:sorted(v) for k,v in x_slices.items()}
    # print('sorting y slices...')
    # y_slices = {k:sorted(v) for k,v in y_slices.items()}

            # l = y_slice
            # print(y_slice, x_thing)
            # x_diff = r - r_off
            # l = x_diff
            # print(a, r_off, l)

    # vis = {}
    # for y, ranges in y_slices.items():
    #     for x_range in ranges:
    #         # print(y, x_range)
    #         for x in range(x_range[0], x_range[1] + 1):
    #             vis[x, y] = '#'
    #     # for x in range(l[0], l[1]+1):
    #     #     vis[x,y] = '#'
    # print_2d('.', vis)
    # 
    # vis = {}
    # for x, ranges in x_slices.items():
    #     for y_range in ranges:
    #         # print(y, x_range)
    #         for y in range(y_range[0], y_range[1] + 1):
    #             vis[x, y] = '#'
    # print_2d('. ', vis, {(0,0):'0'})

    print('condensing overlaps on x axis...')
    x_slices_overlapped = {k:overlap_ranges(v) for k,v in x_slices.items()}
    print('condensing overlaps on y axis...')
    y_slices_overlapped = {k:overlap_ranges(v) for k,v in y_slices.items()}

    # vis = {}
    # for y, ranges in y_slices_overlapped.items():
    #     for x_range in ranges:
    #         # print(y, x_range)
    #         for x in range(x_range[0], x_range[1] + 1):
    #             vis[x, y] = '#'
    # print_2d('. ', vis, {(0, 0): '0'})

    print('finding gaps on x axis...')
    points = set()
    for x, ranges in x_slices_overlapped.items():
        # print(x, ':', ranges)
        for i in range(len(ranges)-1):
            l, r = ranges[i], ranges[i+1]
            ll, lr = l
            rl, rr = r
            if lr == rl-2:
                points.add((x,lr+1))
    # print(points)

    print('matching gaps on y axis...')
    for y, ranges in y_slices_overlapped.items():
        # print(x, ':', ranges)
        for i in range(len(ranges)-1):
            l, r = ranges[i], ranges[i+1]
            ll, lr = l
            rl, rr = r
            if lr == rl-2:
                if (lr+1, y) in points:
                    return (lr+1) * 4000000 + y

    # for y, ranges in y_slices_overlapped.items():
    #     print(y, ':', ranges)


    # print(y_slices)


def overlap_ranges(ranges):
    while True:
        did_work = False
        ranges = sorted(ranges)
        pos = len(ranges) - 1
        while pos > 0:
            l, r = ranges[pos-1], ranges[pos]
            # print(ranges, l, r)
            ll, lr = l
            rl, rr = r
            if lr >= rl:
                ranges[pos-1] = (ll, max(lr,rr))
                ranges.pop(pos)
                did_work = True
            pos -= 1
        if not did_work:
            return ranges
    # l, r = ranges[0]
    # for next_l, next_r in ranges:
    #     if next_l > r:
    #         print(y, next_l - 1)
    #     l = next_l


def p2x():
    # inners = set()
    # sensors = set()
    borders = defaultdict(list)
    sensors = {}
    for sensor, coords in enumerate(data):
        a, b, x, y = coords
        # sensors[a, b] = chr(65 + sensor)
        r = sum([abs(n) for n in vsub((a, b), (x, y))])
        # sensors[a, b] = '@',  # r
        print(sensor, a, r, '               ', end='\r')

        sensors[x, y] = r  # chr(97 + sensor)

        # for coord in diam(a,b, r-1):
        #     inners.add(coord)
        # for coord in diam(a, b, r):
        #     sensors.add(coord)
        for coord in diam(a, b, r + 1):
            x, y = coord
            if x < 0 or y < 0 or x > 4000000 or y > 4000000:
                continue
            borders[y].append(x)
        # for coord in diam(a, b, r - 1):
        #     if coord in sensors:
        #         pass
        #     sensors[coord] = '~'

        # sensors.update({})
        # sensors.update({k: '~' for k in diam(a, b, r - 1) if k not in sensors})

    # print_2d(' ', {k: '#' for k in borders})
    print('checking', len(borders), 'points...')
    print(borders)
    #
    # candidates = {}
    # for point in borders:
    #     for sensor, radius in sensors.items():
    #         dist = vdistm(point, sensor)
    #         print(point, sensor, radius, dist)
    #         if dist <= radius:
    #             print('nope')
    #             break
    #     else:
    #         print(point)
    #         candidates[point] = '?'

    # print_2d(' ', {k: '#' for k in borders}, candidates)
    #
    # l_bound, r_bound = min(tgt_borders)[0], max(tgt_borders)[0]
    # print(l_bound, r_bound)
    #
    # acc = 0
    # for x in range(l_bound, r_bound+1):
    #     if (x, tgt_line) not in beacons:
    #         acc += 1

    # print(sensors)

    # print_2d(' ', sensors)

    # print_2d('  ', {k:'-' for k in borders}, {k:'$' for k in inners}, {k:'#' for k in sensors})

    print('checking sensors...')

    # candidates = {}
    # for x, y in borders:
    #     # print(x,y)
    #     if (x,y) in inners:
    #         continue
    #     if (x,y) in sensors:
    #         continue
    #     if x < 0 or y < 0 or x > 4000000 or y > 4000000:
    #         # print('wat')
    #         continue
    #     r = get_neighbors(x,y, inners, sensors, borders)
    #     print(x,y,r)
    #     if r:
    #         candidates[x,y] = '@'

    # print_2d('  ', {k: '-' for k in borders}, {k: '$' for k in inners}, {k: '#' for k in sensors}, candidates)

    # if (x,y) in :
    #     continue
    # for neighbor in [(x+d[0], y+d[1]) for d in DIRS]:
    #     # print(neighbor)
    #     if neighbor not in sensors:
    #         break
    # else:
    #     return neighbor[0] * 4000000 + neighbor[1]
    # neighbors = [vadd((x, y), d) for d in DIRS]
    # for n in neighbors:
    #     if n in sensors:
    #         continue
    #     if get_neighbors(*n, sensors):
    #         # print_2d('. ', sensors, {(x, y): 'X', (0, 0): 0})
    #         return n[0] * 4000000 + n[1]
    # for x_o, y_o in DIRS:
    #     adj = (x + x_o, y + y_o)
    #     if get_neighbors(*adj, sensors):
    #         print_2d('. ', sensors, {(x, y): 'X', (0,0):0})
    #         return x, y
    # print(x,y, neighbors)

    # print_2d('. ', sensors) #, {k:'!' for k in tgt_borders})

    # diam(0,0,10)


# 10363143010544 too low
# 11542111305286 too high


def get_neighbors(x, y, inners, sensors, borders):
    # print_2d('. ', sensors)
    neighbors = [vadd((x, y), d) for d in DIRS]
    # print('wtf', x, y, neighbors, [sensors[n] for n in neighbors if n in sensors])
    for n in neighbors:
        if n not in sensors or n in inners:
            return False
        # if n not in sensors or sensors[j] != '#':
        #     return False
    # print([sensors[j] for j in neighbors])
    # print(sensors[x-2,y], sensors[x-1,y], sensors[x,y], sensors[x+1,y], sensors[x+2,y])
    return True


day = 15
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[int(i) for i in re.findall(r'[\-0-9]+', line)] for line in file]

# print('part1:', p1())
print('part2:', p2())
