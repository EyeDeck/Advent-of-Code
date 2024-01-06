from aoc import *


def solve():
    def test(time):
        for i, disc in enumerate(discs):
            ct, pos = disc
            if (pos + (i + 1) + time) % ct != 0:
                return False
        return True

    i = 0
    while not test(i):
        i += 1
    return i


setday(15)

data = parselines()

discs = []
for line in data:
    line = line.split()
    # n = int(line[1].strip('#'))
    positions = int(line[3])
    pos = int(line[-1].strip('.'))
    discs.append([positions, pos])

print('part1:', solve() )
discs.append([11, 0])
print('part2:', solve() )
