import itertools
from aoc import *


def solve(p2=False):
    antinodes = set()
    for key, coords in inverse.items():
        if key == '.':
            continue

        for pair in itertools.permutations(coords, 2):
            diff = vsub(*pair)

            antinode = vadd(pair[0], ((0, 0) if p2 else diff))
            while antinode in grid:
                antinodes.add(antinode)
                antinode = vadd(antinode, diff)
                if antinode not in grid or not p2:
                    break

    if verbose:
        print_2d('  ', grid, {k: '#' for k in antinodes})
    return len(antinodes)


setday(8)

grid, inverse, unique = parsegrid()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', solve(False))
print('part2:', solve(True))
