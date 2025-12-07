from aoc import *


def solve():
    start = unique['S']
    beams = defaultdict(int, {start: 1})
    last_beams = None
    acc = 0
    while beams:
        last_beams = beams
        next_beams = defaultdict(int)
        for b, ct in beams.items():
            next_pos = vadd((0, 1), b)
            if next_pos not in grid:
                continue
            if grid[next_pos] == '^':
                acc += 1
                l, r = vadd((-1, 0), next_pos), vadd((1, 0), next_pos)

                next_beams[l] += ct
                next_beams[r] += ct
            else:
                next_beams[next_pos] += ct
        beams = next_beams
    return acc, sum(last_beams.values())


if __name__ == '__main__':
    setday(7)

    grid, inverse, unique = parsegrid()

    print('part1: %d\npart2: %d' % solve())
