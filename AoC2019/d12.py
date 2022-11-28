import copy
import math
import os
import shutil
import sys
import re
from PIL import Image, ImageDraw


def invert_srgb_companding(color):  # whatever the hell that means
    one_scale = [min(1, max(0, c/255)) for c in color]
    one_scale = [pow((c+0.055) / 1.055, 2.4) if c > 0.04045 else c / 12.92 for c in one_scale]
    return tuple([c*255 for c in one_scale])


def srgb_companding(color):
     one_scale = [min(1, max(0, c / 255)) for c in color]
     one_scale = [1.055 * pow(c, 1/2.4)-0.055 if c > 0.0031308 else c * 12.92 for c in one_scale]
     return tuple([int(c*255) for c in one_scale])


def gradient(a, b, amt):
    a = invert_srgb_companding(a)
    b = invert_srgb_companding(b)
    ret = (int(a[0] * (1 - amt) + b[0] * amt),
           int(a[1] * (1 - amt) + b[1] * amt),
           int(a[2] * (1 - amt) + b[2] * amt))
    return srgb_companding(ret)


def render_board(coords, vels, size, num):
    mid = (size[0] // 2, size[1] // 2)
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)

    # I'm certain there's some elegant one-liner for this, but I can't figure it out
    unsorted = set(range(moon_ct))
    order = []
    while unsorted:
        m = 100000000000
        mi = -1
        for i in unsorted:
            if coords[i][2] < m:
                m = coords[i][2]
                mi = i
        unsorted.remove(mi)
        order.append(mi)
    coords = [coords[i] for i in order]
    vels = [vels[i] for i in order]

    for coord, vel in zip(coords, vels):
        camera = 100
        focus = 120
        if camera-10 - coord[2] < 0:
            continue

        x,y = ((coord[0] * ((coord[2]+camera) / focus))+mid[0]), \
              ((coord[1] * ((coord[2]+camera) / focus))+mid[0])

        r = max(1, 1/(camera-coord[2] if camera-coord[2] > 0 else 1) * 1000)
        total_vel = sum([abs(v) for v in vel]) / 40

        color = gradient((0, 0, 255), (255, 128, 0), total_vel)
        if camera - coord[2] > camera:
            color = tuple([c-(camera//5) for c in color])

        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    del draw
    img.save(out_dir + '\\frame' + str(num).zfill(6) + '.png')
    return


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


def render(_p, _v, size):
    p1_pos = copy.deepcopy(_p)
    p1_vel = copy.deepcopy(_v)
    for i in range(3600//1):  #2772):
        step(p1_pos, p1_vel)
        # print(p1_pos, p1_vel)
        render_board(p1_pos, p1_vel, size, i)
        if i % 50 == 0:
            print(i, end='\r')
    p1 = 0
    for i in range(moon_ct):
        p1 += sum([abs(i) for i in p1_pos[i]]) * sum([abs(i) for i in p1_vel[i]])
    return p1


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
out_dir = f.split('.')[0]
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.mkdir(out_dir)

pattern = re.compile('[-\\d]+')
pos = [[int(j) for j in pattern.findall(i)] for i in open(f).readlines()]
vel = [[0 for _ in i] for i in pos]
moon_ct = len(pos)

render(pos, vel, (800, 800))

# print('p1:', part1(pos, vel))
# print('p2:', part2(pos, vel))
