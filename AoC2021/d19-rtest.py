import math


def rotate(points, x, y, z):
    cosa = math.cos(z)
    sina = math.sin(z)

    cosb = math.cos(x)
    sinb = math.sin(x)

    cosc = math.cos(y)
    sinc = math.sin(y)

    Axx = cosa * cosb
    Axy = cosa * sinb * sinc - sina * cosc
    Axz = cosa * sinb * cosc + sina * sinc

    Ayx = sina * cosb
    Ayy = sina * sinb * sinc + cosa * cosc
    Ayz = sina * sinb * cosc - cosa * sinc

    Azx = -sinb
    Azy = cosb * sinc
    Azz = cosb * cosc

    r = []
    for p in points:
        px, py, pz = p
        raw = (Axx * px + Axy * py + Axz * pz, Ayx * px + Ayy * py + Ayz * pz, Azx * px + Azy * py + Azz * pz)
        r.append(tuple(round(n) for n in raw))
    return r


all = set()
for x in range(0, 4):
    for y in range(0, 4):
        for z in range(0, 4):
            all.add(rotate([(1, 2, 3)], math.radians(90 * x), math.radians(90 * y), math.radians(90 * z)).pop())

lines = []
for x in str(all)[2:-2].replace('1', 'x').replace('2', 'y').replace('3', 'z').split('), ('):
    lines.append(f'lambda x,y,z: ({x}), ')

indexed_rotations = eval('[' + ''.join(lines) + ']')

for i in range(24):
    print(indexed_rotations[i](*[1, 2, 3]))