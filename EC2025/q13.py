from collections import deque

from ec import *


def fast(n, turns, p1=False):
    if p1:
        data = [(line[0], line[0]) for line in parse_lines(n, get_ints)]
    else:
        data = [tuple(int(s) for s in line.split('-')) for line in parse_lines(n)]

    ranges_sorted = deque([(1, (1, 1))])
    toggle = True
    total_len = 1
    start_pos = 0

    for l, r in data:
        ln = r - l + 1
        total_len += ln
        if toggle:
            ranges_sorted.append((ln, (l, r)))
        else:
            ranges_sorted.appendleft((ln, (r, l)))
            start_pos += ln

        toggle = not toggle
    end_pos = (start_pos + turns) % total_len

    acc = 0
    for ln, (l, r) in ranges_sorted:
        if ln + acc < (end_pos + 1):
            acc += ln
        else:
            range_index = end_pos - acc
            if l < r:
                return l + range_index
            else:
                return l - range_index


setquest(13)

print('part1:', fast(1, 2025, True))
print('part2:', fast(2, 20252025))
print('part3:', fast(3, 202520252025))
