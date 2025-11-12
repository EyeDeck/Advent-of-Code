import math

from ec import *


def p1():
    data = parse_lines(1, get_ints)[0]

    acc = 0
    for i in range(len(data)-1):
        l,r = sorted([data[i], data[i+1]])
        if l+16==r:
            acc += 1
    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    return acc
#31


# copied from https://stackoverflow.com/a/62625458
def intersects(s0, s1):
    dx0 = s0[1][0] - s0[0][0]
    dx1 = s1[1][0] - s1[0][0]
    dy0 = s0[1][1] - s0[0][1]
    dy1 = s1[1][1] - s1[0][1]
    p0 = dy1 * (s1[1][0] - s0[0][0]) - dx1 * (s1[1][1] - s0[0][1])
    p1 = dy1 * (s1[1][0] - s0[1][0]) - dx1 * (s1[1][1] - s0[1][1])
    p2 = dy0 * (s0[1][0] - s1[0][0]) - dx0 * (s0[1][1] - s1[0][1])
    p3 = dy0 * (s0[1][0] - s1[1][0]) - dx0 * (s0[1][1] - s1[1][1])
    return (p0 * p1 < 0) & (p2 * p3 < 0)


def p2():
    data = parse_lines(2, get_ints)[0]

    point_coords = {}
    pin_ct = 256
    for i in range(pin_ct):
        theta = (math.pi * 2) / pin_ct
        angle = theta * i

        point_coords[i+1] = (pin_ct * math.cos(angle), pin_ct * math.sin(angle))

    # print(point_coords)

    acc = 0
    line_segments = []
    for i in range(len(data)-1):
        l,r = sorted([data[i], data[i+1]])
        segment = (point_coords[l],point_coords[r])

        for other_segment in line_segments:
            if intersects(segment, other_segment):
                acc += 1

        line_segments.append(segment)



    # data = parse_lines(2, get_ints)
    # data = parse_double_break(2)

    return acc
    # 2990991

def p3():
    data = parse_lines(3, get_ints)[0]

    point_coords = {}
    pin_ct = 256
    for i in range(pin_ct):
        theta = (math.pi * 2) / pin_ct
        angle = theta * i

        point_coords[i+1] = (pin_ct * math.cos(angle), pin_ct * math.sin(angle))

    # print(point_coords)

    line_segments = []
    for i in range(len(data)-1):
        l,r = sorted([data[i], data[i+1]])
        segment = (point_coords[l],point_coords[r])
        line_segments.append(segment)


    best = 0
    for i in range(pin_ct):
        for j in range(i+1, pin_ct):
            cut_segment = (point_coords[i+1],point_coords[j+1])

            acc = 0
            for other_segment in line_segments:
                if intersects(cut_segment, other_segment):
                    acc += 1

            best = max(best, acc)


    # data = parse_lines(2, get_ints)
    # data = parse_double_break(2)

    return best


setquest(8)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
