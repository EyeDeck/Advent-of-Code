from aoc import *


def solve():
    hex_map = {d: HEXDIRS[i] for i, d in enumerate(['n', 'nw', 'sw', 's', 'se', 'ne'])}
    furthest = 0
    start = (0, 0, 0)
    pos = start
    for step in data:
        pos = vadd(pos, hex_map[step])
        furthest = max(furthest, hexdist(start, pos))
    return hexdist(start, pos), furthest


setday(11)

with open_default() as file:
    data = file.read().strip().split(',')

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1: %d\npart2: %d' % solve())
