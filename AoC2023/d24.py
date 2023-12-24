import numpy as np
from aoc import *


def intersect(a, b):
    '''https://stackoverflow.com/a/74266064'''
    c1 = np.array([*a[0]]).T
    v1 = np.array([*a[1]]).T

    c2 = np.array([*b[0]]).T
    v2 = np.array([*b[1]]).T

    x, err, rank = np.linalg.lstsq(np.array([v1, -v2]).T, c2 - c1, rcond=None)[:3]
    if rank == 2:
        return v1 * x[0] + c1
    else:
        return None

def p1():
    hailstones = []
    for line in data:
        p, v = line.split(' @ ')
        # px, py, pz = [int(n) for n in p.split(', ')]
        # vx, vy, vz = [int(n) for n in v.split(', ')]
        # print(px, py, pz, vx, vy, vz, slope)
        # hailstones.append((px, py, pz, vx, vy, vz, slope))
        p = tuple(int(n) for n in p.split(', ')[:-1])
        v = tuple(int(n) for n in v.split(', ')[:-1])
        hailstones.append((p,v))


    acc = 0
    for i, h1 in enumerate(hailstones):
        for h2 in hailstones[i+1:]:
            # print('\nintersecting', h1, h2)
            # a, b = h1[0], h2[0]
            # print(vdistm(a,b), end='')
            # for i in range(5):
            #     a, b = vadd(a, h1[1]), vadd(b, h2[1])
            #     print(' ', vdistm(a,b), end='')

            # start_dist = vdist2(h1[0], h2[0])
            # after_tick = vdist2(vadd(*h1), h2[0])
            # print(start_dist, after_tick, vadd(*h1), vadd(*h2), vdist2(vadd(vadd(*h1), h1[1]), vadd(vadd(*h2), h2[1])))
            # if start_dist < after_tick:
            #     print('crossed in past? ignoring')
            #     continue

            intersection = intersect(h1, h2)
            if intersection is None:
                # print('no cross')
                continue

            h1_dist_before_tick = vdist2(h1[0], intersection)
            h1_dist_after_tick = vdist2(vadd(*h1), intersection)
            h2_dist_before_tick = vdist2(h2[0], intersection)
            h2_dist_after_tick = vdist2(vadd(*h2), intersection)
            # print(f'{h1_dist_before_tick} then {h1_dist_after_tick}; {h2_dist_before_tick} then {h2_dist_after_tick}')
            if h1_dist_before_tick < h1_dist_after_tick or h2_dist_before_tick < h2_dist_after_tick:
                # print('crossed in past? ignoring')
                continue

            # least, most = 7, 27
            least, most = 200000000000000, 400000000000000
            if least <= intersection[0] <= most and least <= intersection[1] <= most:
                # print('crossed inside! at', intersection)
                acc += 1
            else:
                # print('crossed outside! at', intersection)
                pass

    return acc

    # 16053 wrong


def p2():

    return None


setday(24)

data = parselines()
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )
