import itertools
from aoc import *


def p1():
    antinodes = set()
    for key, coords in inverse.items():
        if key == '.':
            continue
        # print(key)
        for pair in itertools.permutations(coords, 2):
            diff = vsub(*pair)
            antinode = vadd(pair[0], diff)
            # print(pair, diff, '=', antinodes)
            if antinode in grid:
                antinodes.add(antinode)
    print_2d('  ', grid, {k: '#' for k in antinodes})
    return len(antinodes)


def p2():
    antinodes = set()
    for key, coords in inverse.items():
        if key == '.':
            continue
        # print(key)
        for pair in itertools.permutations(coords, 2):
            diff = vsub(*pair)
            antinode = pair[0]
            while antinode in grid:
                antinodes.add(antinode)
                antinode = vadd(antinode, diff)
                if antinode not in grid:
                    break

    print_2d('  ', grid, {k: '#' for k in antinodes})
    return len(antinodes)


setday(8)

grid, inverse, unique = parsegrid()

print('part1:', p1())
print('part2:', p2())
