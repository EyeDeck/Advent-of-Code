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
    # print('get_rotations_for', points)
    return [get_orientation[n](*x) for x in points]


def get_all_rotations(sets):
    all_rots = []
    for i in range(24):
        this_rot = [get_orientation[i](*x) for x in sets]
        all_rots.append(this_rot)
    print(all_rots)

    # perms = list(permutations(d[0]))
    # print(perms)


def test_alignment_for(points1, points2):
    for h, (ox,oy,oz) in enumerate(points1):
        for i, p1 in enumerate(points1):
            diffs = defaultdict(int)
            for j, p2 in enumerate(points2):
                # print(p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
                diffs[(p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])] += 1
            for k,v in diffs.items():
                if v > 1:
                    print(diffs)

            # # print('aaa', i, j, p1, p2)
            # ct = 0
            # #for k, po in enumerate(points1):
            # for k, (ox, oy, oz) in enumerate(points1):
            #     # ox, oy, oz = p2[0] - po[0], p2[1] - po[1], p2[2] - po[2]
            #     print(p1[0] - ox, p1[1] - oy, p1[2] - ox)
            #     if p1[0] - ox == 0 and p1[1] - oy == 0 and p1[2] - ox == 0:
            #         ct += 1
            # if ct > 0:
            #     print(i,j, ct)


def test_rotations_for(points1, points2):
    # print('GOT p1', points1, '\n')
    # print('GOT p2', points2, '\n')
    for i in range(24):
        for j in range(24):
            test_alignment_for(get_rotations_for(i, points1), get_rotations_for(j, points2))


# def try_alignment_for(points):
#     for p in points:
#         ox, oy, oz = -p[1], -p[2], -p[3]
#         for p2 in built:
#
#
#
# def try_rotations_for(points):
#     for i in range(24):
#         try_alignment_for(get_rotations_for(i, points))


def test_alignments(pts1, pts2):
    dists = defaultdict(int)
    for p1 in pts1:
        for p2 in pts2:
            dist = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]) # vsub(p1,p2)
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
                        return i,j,h,k
    return None


def find_rel_match(abs, rel):
    for i,v in rel.items():
        if i[0] in abs:
            return v, i[0]


def p1():
    print(parsed[0])
    unfound = copy.deepcopy(parsed)
    found = {0: unfound.pop(0)}

    rel_offsets = {}
    while len(unfound):
        m = find_next_match(found, unfound)
        if m is None:
            print('no matches?', len(found), len(unfound))
        found_index, unfound_index, rotation, offset = m
        found[unfound_index] = get_rotations_for(rotation, unfound.pop(unfound_index))
        # print('just wrote to found index', unfound_index)
        # rel_offsets[(found_index, unfound_index)] = get_orientation[rotation](*offset)
        rel_offsets[(found_index, unfound_index)] = offset
        print(found_index, unfound_index, rotation, offset)

    for k,v in rel_offsets.items():
        print(k,v)

    abs_offsets = {0:(0,0,0)}
    while len(rel_offsets):
        print('aaa', rel_offsets, '\n', abs_offsets, '\n')
        r = -1
        for k,v in rel_offsets.items():
            print(k)
            l, r = k
            if l in abs_offsets:
                print('adding offsets:', abs_offsets[l], 'and',  rel_offsets[l, r])
                abs_offsets[r] = vadd(abs_offsets[l], rel_offsets[l, r])
                print('asdasdasdasdasd', abs_offsets[r])
                break
        del rel_offsets[l,r]
        # abs_offsets[m[0]] = rel_offsets[m[1]]

    print('absolute offsets:', abs_offsets)

    print(found)

    built = set()
    for k, points in found.items():
        for point in points:
            built.add( vadd(point, abs_offsets[k]) )

    print('all:', sorted(built))


    # for s1, p1 in parsed.items():
    #     for s2, p2 in parsed.items():
    #         if s1 == s2:
    #             continue
    #         print(s1, s2)
    #         # print('PASSING IN p1', p1, '\n')
    #         # print('PASSING IN p2', p2, '\n')
    #         test_rotations_for(p1, p2)

    # built = set(parsed[0])
    # while len(parsed) > 0:
    #     for k, v in parsed.items():
    #         test_rotations_for(v)
    #     break
    # return None
    return len(built)


def p2():
    return None


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

print('parsed:', parsed)
# built = set(parsed[0])

print(f'part1: {p1()}')
print(f'part2: {p2()}')
