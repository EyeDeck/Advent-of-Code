from aoc import *


def p1():
    start = unique['S']
    beams = {start}
    acc = 0
    while beams:
        next_beams = set()
        for b in beams:
            next_pos = vadd((0, 1), b)
            if next_pos not in grid:
                continue
            if grid[next_pos] == '^':
                acc += 1
                l, r = vadd((-1, 0), next_pos), vadd((1, 0), next_pos)

                next_beams.add(l)
                next_beams.add(r)
            else:
                next_beams.add(next_pos)

        beams = next_beams
    return acc


def p2():
    start = unique['S']
    beams = defaultdict(int, {start: 1})
    last_beams = 0
    while beams:
        next_beams = defaultdict(int)
        for b, ct in beams.items():
            next_pos = vadd((0, 1), b)
            if next_pos not in grid:
                continue
            if grid[next_pos] == '^':
                l, r = vadd((-1, 0), next_pos), vadd((1, 0), next_pos)

                next_beams[l] += ct
                next_beams[r] += ct
            else:
                next_beams[next_pos] += ct

        last_beams = beams
        beams = next_beams
    return sum(last_beams.values())


if __name__ == '__main__':
    setday(7)

    grid, inverse, unique = parsegrid()

    print('part1:', p1())
    print('part2:', p2())
