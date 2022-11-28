from aoc import *
import math


def try_traj(x, y):
    this_traj = {(0, 0): 'S'}
    px, py = 0, 0
    while True:
        px += x
        py += y
        this_traj[px, -py] = '#'
        x -= 1 if x > 0 else 0 if x == 0 else -1
        y -= 1
        if (px, -py) in target:
            return this_traj
        if py < tgt[2] or px > tgt[1]:
            return None


def solve():
    hits = {}
    best_y = 0

    x_range = (math.ceil(-1/2 + math.sqrt(1+8*min(tgt[0:2]))/2), max(tgt[0:2])+1)
    y_range = min(tgt[2:4]), abs(min(tgt[2:4]))

    for x in range(*x_range):
        for y in range(*y_range):
            d = try_traj(x, y)
            if d is not None:
                hits[x, y] = d
                highest = -min(y[1] for y in d)
                best_y = max(best_y, highest)
                if '--render' in sys.argv:
                    print(f'\nVelocity ({x},{y}) (highest={highest}, samples={len(d)}):')
                    print_2d('.', target, d)
    return best_y, len(hits)


day = 17
f = f'd{day}.txt'
if len(sys.argv) > 1:
    if sys.argv[1][-4:] == '.txt':
        f = sys.argv[1]
    else:
        f = None
        raw = ' '.join(sys.argv[1:])
if f:
    with open(f) as file:
        raw = file.read()

tgt = [int(i) for i in re.findall('(-?\d+)', raw)]

target = {}
for x in range(tgt[0], tgt[1] + 1):
    for y in range(tgt[2], tgt[3] + 1):
        target[x, -y] = 'T'

p1, p2 = solve()
print(f'part1: {p1}')
print(f'part2: {p2}')
