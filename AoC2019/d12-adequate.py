import copy
import math
import sys
import re


def step(_p, _v):
    for i in range(moon_ct):
        for j in range(moon_ct):
            for k in range(0,3):
                if _p[i][k] < _p[j][k]:
                    _v[i][k] += 1
                elif _p[i][k] > _p[j][k]:
                    _v[i][k] -= 1
    for i in range(moon_ct):
        for j in range(0, 3):
            _p[i][j] += _v[i][j]


def lcm(*args):
    ret = args[0]
    for arg in args[1:]:
        ret = (ret * arg) // math.gcd(ret, arg)
    return ret


def part1(_p, _v):
    p1_pos = copy.deepcopy(_p)
    p1_vel = copy.deepcopy(_v)
    for i in range(1000):
        step(p1_pos, p1_vel)
    p1 = 0
    for i in range(moon_ct):
        p1 += sum([abs(i) for i in p1_pos[i]]) * sum([abs(i) for i in p1_vel[i]])
    return p1


def part2(_p, _v):
    p2_pos = copy.deepcopy(_p)
    p2_vel = copy.deepcopy(_v)

    unfound = set(range(0, 3))
    cycles = []
    loops = 1

    while unfound:
        step(p2_pos, p2_vel)
        for axis in unfound:
            good = True
            for moon in range(moon_ct):
                if p2_pos[moon][axis] != _p[moon][axis] or p2_vel[moon][axis] != _v[moon][axis]:
                    good = False
                    break
            if good:
                unfound.remove(axis)
                cycles.append(loops)
                print(cycles, '...', end='\r')
                break
        loops += 1

    #print(' '*100, end='\r')
    print('')
    return lcm(*cycles)


f = 'd12.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

pattern = re.compile('[-\\d]+')
pos = [[int(j) for j in pattern.findall(i)] for i in open(f).readlines()]
vel = [[0 for _ in i] for i in pos]
moon_ct = len(pos)

print('p1:', part1(pos, vel))
print('p2:', part2(pos, vel))
