from aoc import *


def p1():
    p_data = parselines(get_ints)
    for iteration in range(1000):
        for particle in p_data:
            for i in range(3):
                particle[3 + i] += particle[6 + i]
                particle[i] += particle[3 + i]
    closest_i, closest_d = -1, INF
    for i, particle in enumerate(p_data):
        d_to_0 = vmagm(particle)
        if d_to_0 < closest_d:
            closest_i = i
            closest_d = d_to_0
    return closest_i


def p2():
    p_data = parselines(get_ints)
    for iteration in range(1000):
        p_count = defaultdict(int)
        for particle in p_data:
            for i in range(3):
                particle[3 + i] += particle[6 + i]
                particle[i] += particle[3 + i]
            p_count[tuple(particle[:3])] += 1
        dead_positions = set(k for k, v in p_count.items() if v > 1)
        p_data = [p for p in p_data if tuple(p[:3]) not in dead_positions]

    return len(p_data)


setday(20)

print('part1:', p1())
print('part2:', p2())
