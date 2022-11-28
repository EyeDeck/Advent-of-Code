import copy
from collections import *
from aoc import *

get_orientation = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (y, z, x),
]


def get_rotations_for(n, points):
    return [get_orientation[n](*x) for x in points]


def test_alignments(pts1, pts2):
    dists = defaultdict(int)
    for p1 in pts1:
        for p2 in pts2:
            dist = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
            dists[dist] += 1
    return dists


def find_next_match(found, unfound):
    for i, pts in found.items():
        for j, fpts in unfound.items():
            for h in range(24):
                this_rotation = get_rotations_for(h, fpts)
                out = test_alignments(pts, this_rotation)
                for k, v in out.items():
                    if v >= 12:
                        return i, j, h, k
    return None


def solve():
    unfound = copy.deepcopy(parsed)
    mn, mx = 1, len(unfound)-1
    found = {0: unfound.pop(0)}

    rel_offsets = {}
    while len(unfound):
        m = find_next_match(found, unfound)

        found_index, unfound_index, rotation, offset = m
        found[unfound_index] = get_rotations_for(rotation, unfound.pop(unfound_index))

        rel_offsets[(found_index, unfound_index)] = offset
        ps = lambda s, bg, ct: (ct - len(str(s))) * bg + str(s)
        p = lambda s: ps(s, ' ', 2)
        print(f'({p(mn)}/{p(mx)}) {p(unfound_index)} connects to {p(found_index)} with rotation index {p(rotation)} and offset',
            ','.join(ps(n, ' ', 6) for n in offset))
        mn += 1

    abs_offsets = {0: (0, 0, 0)}
    while len(rel_offsets):
        r = -1
        for k, v in rel_offsets.items():
            l, r = k
            if l in abs_offsets:
                abs_offsets[r] = vadd(abs_offsets[l], rel_offsets[l, r])
                break
        del rel_offsets[l, r]

    built = set()
    for k, points in found.items():
        for point in points:
            built.add(vadd(point, abs_offsets[k]))

    mx = 0
    for k, v in abs_offsets.items():
        for k2, v2 in abs_offsets.items():
            mx = max(mx, vmagm(vsub(v, v2)))

    return len(built), mx


day = 19
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file.read().split('\n\n')]

parsed = {}
for thing in data:
    lines = thing.split('\n')
    n = re.findall('scanner (\d+)', lines[0])[0]
    parsed[int(n)] = [tuple(int(i) for i in x.split(',')) for x in lines[1:]]

p1, p2 = solve()
print(f'part1: {p1}')
print(f'part2: {p2}')
