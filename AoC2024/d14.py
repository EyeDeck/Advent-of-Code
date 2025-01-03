import math

from aoc import *


def tick(robots, n):
    new_robots = []
    for robot in robots:
        nxt = vadd(robot[0], vmul(robot[1], (n, n)))
        nxt = vmod(nxt, (WIDTH, HEIGHT))
        new_robots.append([nxt, robot[1]])
    return new_robots


def p1():
    r = tick(robots, 100)

    positions = [k[0] for k in r]
    quadrants = [
        [p for p in positions if p[0] < WIDTH//2 and p[1] < HEIGHT//2],
        [p for p in positions if p[0] < WIDTH//2 and p[1] > HEIGHT//2],
        [p for p in positions if p[0] > WIDTH//2 and p[1] < HEIGHT//2],
        [p for p in positions if p[0] > WIDTH//2 and p[1] > HEIGHT//2]
    ]

    if verbose:
        print_2d('.', {k:'A' for k in quadrants[0]}, {k:'B' for k in quadrants[1]}, {k:'C' for k in quadrants[2]}, {k:'D' for k in quadrants[3]})

    return math.prod(len(q) for q in quadrants)


def p2():
    robots = []
    for i, line in enumerate(data):
        robots.append([(line[0], line[1]), (line[2], line[3])])

    i = 0
    while True:
        i += 1
        robots = tick(robots, 1)
        positions = {k[0] for k in robots}
        neighbor_ct = 0
        for pos in positions:
            for d in DIRS:
                if vadd(d, pos) in positions:
                    neighbor_ct += 1
        # heuristic, but works on the input data
        if neighbor_ct > len(data):
            if verbose:
                print_2d('.', {k: '#' for k in positions})
            return i
        else:
            print(i, end='\r')


setday(14)

data = parselines(get_ints)
robots = []
for i, line in enumerate(data):
    robots.append([(line[0], line[1]), (line[2], line[3])])

WIDTH = 101
HEIGHT = 103

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1() )
print('part2:', p2() )
