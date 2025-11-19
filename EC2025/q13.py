from collections import deque

from ec import *


def p1():
    data = [line[0] for line in parse_lines(1, get_ints)]
    # print(data)
    wheel = deque([1])
    toggle = True
    for n in data:
        if toggle:
            wheel.append(n)
        else:
            wheel.appendleft(n)
        toggle = not toggle
    start_pos = wheel.index(1)
    next_pos = (start_pos + 2025) % len(wheel)
    # print(wheel, start_pos, wheel[next_pos])
    # data =
    # data = parse_double_break(1)

    return wheel[next_pos]


def p2():
    data = [tuple(int(s) for s in line.split('-')) for line in parse_lines(2)]
    # print(data)
    wheel = deque([1])
    toggle = True
    for n in data:
        if toggle:
            wheel.extend([i for i in range(n[0], n[1]+1)])
        else:
            wheel.extendleft([i for i in range(n[0], n[1]+1)])
        toggle = not toggle
    start_pos = wheel.index(1)
    next_pos = (start_pos + 20252025) % len(wheel)
    # print(wheel, start_pos)

    return wheel[next_pos]


def p3():
    data = [tuple(int(s) for s in line.split('-')) for line in parse_lines(3)]
    # print(data)
    wheel = deque([1])
    toggle = True
    for n in data:
        if toggle:
            wheel.extend([i for i in range(n[0], n[1]+1)])
        else:
            wheel.extendleft([i for i in range(n[0], n[1]+1)])
        toggle = not toggle
    start_pos = wheel.index(1)
    next_pos = (start_pos + 202520252025 ) % len(wheel)
    # print(wheel, start_pos)

    return wheel[next_pos]


setquest(13)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
