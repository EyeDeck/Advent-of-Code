from aoc import *


def try_lock_key(lock, key):
    for pos, c in lock.items():
        if c == '#' and key[pos] == '#':
            return 0
    return 1


setday(25)

with open_default() as file:
    data_raw = file.read().split('\n\n')

locks = []
keys = []
for raw_grid in data_raw:
    d = {}
    lines = raw_grid.split('\n')
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            d[(x, y)] = c

    if '#' in lines[0]:
        locks.append(d)
    else:
        keys.append(d)

print('part1:', sum(try_lock_key(lock, key) for lock in locks for key in keys))
print('part2:', 'Merry Christmas 🎄')
