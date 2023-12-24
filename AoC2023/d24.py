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
        p = tuple(int(n) for n in p.split(', ')[:-1])
        v = tuple(int(n) for n in v.split(', ')[:-1])
        hailstones.append((p, v))

    acc = 0
    for i, h1 in enumerate(hailstones):
        for h2 in hailstones[i + 1:]:
            # print('\nintersecting', h1, h2)

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


def p2():
    hailstones = []
    for line in data:
        p, v = line.split(' @ ')
        p = tuple(int(n) for n in p.split(', '))
        v = tuple(int(n) for n in v.split(', '))
        hailstones.append((p, v))

    hailstones = hailstones[:3]

    # ugh
    import z3
    solver = z3.Solver()
    x, y, z, vx, vy, vz = [z3.Real(v) for v in ['x', 'y', 'z', 'vx', 'vy', 'vz']]
    for i, ((cx, cy, cz), (hvx, hvy, hvz)) in enumerate(hailstones):
        t = z3.Real(f't{i}')
        solver.add(t > 0)
        solver.add(x + vx * t == cx + hvx * t)
        solver.add(y + vy * t == cy + hvy * t)
        solver.add(z + vz * t == cz + hvz * t)
    solver.check()
    m = solver.model()
    return sum(m[v].as_long() for v in [x,y,z])


setday(24)

data = parselines()

print('part1:', p1())
print('part2:', p2())
