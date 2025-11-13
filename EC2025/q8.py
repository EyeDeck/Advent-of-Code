import math

from ec import *


def p1():
    data = parse_lines(1, get_ints)[0]

    pin_ct = 32

    acc = 0
    for i in range(len(data) - 1):
        l, r = sorted([data[i], data[i + 1]])
        if l + pin_ct//2 == r:
            acc += 1

    return acc


def intersects(s0, s1):
    """
    Copied from https://stackoverflow.com/a/62625458
    Calculates whether two line segments intersect
    :param s0:  one line segment
    :param s1:  the other line segment
    :return:    boolean value whether the segments intersect
    """
    dx0 = s0[1][0] - s0[0][0]
    dx1 = s1[1][0] - s1[0][0]
    dy0 = s0[1][1] - s0[0][1]
    dy1 = s1[1][1] - s1[0][1]
    p0 = dy1 * (s1[1][0] - s0[0][0]) - dx1 * (s1[1][1] - s0[0][1])
    p1 = dy1 * (s1[1][0] - s0[1][0]) - dx1 * (s1[1][1] - s0[1][1])
    p2 = dy0 * (s0[1][0] - s1[0][0]) - dx0 * (s0[1][1] - s1[0][1])
    p3 = dy0 * (s0[1][0] - s1[1][0]) - dx0 * (s0[1][1] - s1[1][1])
    return (p0 * p1 < 0) & (p2 * p3 < 0)


def get_spaced_point_on_circle(n, pin_ct, r):
    """
    :param n:   which numbered point to calculate
    :param ct:  how many total points the circle should have
    :param r:   circle radius
    :return:    tuple of (x,y) coords
    """
    theta = (math.pi * 2) / pin_ct
    angle = theta * n

    return r * math.cos(angle), r * math.sin(angle)


def p2():
    data = parse_lines(2, get_ints)[0]

    pin_ct = 256

    point_coords = {}
    for i in range(pin_ct):
        point_coords[i + 1] = get_spaced_point_on_circle(i, pin_ct, pin_ct)

    acc = 0
    line_segments = []
    for i in range(len(data) - 1):
        l, r = sorted([data[i], data[i + 1]])
        segment = (point_coords[l], point_coords[r])

        for other_segment in line_segments:
            if intersects(segment, other_segment):
                acc += 1

        line_segments.append(segment)

    return acc


def p3():
    data = parse_lines(3, get_ints)[0]

    pin_ct = 256

    point_coords = {}
    for i in range(pin_ct):
        point_coords[i + 1] = get_spaced_point_on_circle(i, pin_ct, pin_ct)

    line_segments = []
    for i in range(len(data) - 1):
        l, r = sorted([data[i], data[i + 1]])
        segment = (point_coords[l], point_coords[r])
        line_segments.append(segment)

    best = 0
    for i in range(pin_ct):
        for j in range(i + 1, pin_ct):
            cut_segment = (point_coords[i + 1], point_coords[j + 1])

            acc = 0
            for other_segment in line_segments:
                if intersects(cut_segment, other_segment):
                    acc += 1

            best = max(best, acc)

    return best


setquest(8)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
