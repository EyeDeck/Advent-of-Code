from collections import deque

from ec import *


def bruteforce(n, turns, p1=False):
    if p1:
        data = [(line[0], line[0]) for line in parse_lines(n, get_ints)]
    else:
        data = [tuple(int(s) for s in line.split('-')) for line in parse_lines(n)]

    wheel = deque([1])
    toggle = True
    start_pos = 0

    for l, r in data:
        if toggle:
            wheel.extend(i for i in range(l, r + 1))
        else:
            wheel.extendleft(i for i in range(l, r + 1))
            start_pos += r - l + 1
        toggle = not toggle

    next_pos = (start_pos + turns) % len(wheel)
    return wheel[next_pos]


setquest(13)

print('part1:', bruteforce(1, 2025, True))
print('part2:', bruteforce(2, 20252025))
print('part3:', bruteforce(3, 202520252025))
