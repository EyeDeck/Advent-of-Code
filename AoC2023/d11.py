from aoc import *


def solve(expansion):
    expansion -= 1
    grid, inverse, unique = parsegrid()
    galaxies = inverse['#']

    width  = max(grid.keys(), key=itemgetter(0))[0]
    height = max(grid.keys(), key=itemgetter(1))[1]

    # expand horizontally
    off = 0
    for x in range(width + 1):
        s = set()
        for y in range(height + 1):
            s.add(grid[x,y])
        if len(s) == 1 and s.pop() == '.':
            galaxies = [(g[0] + expansion if g[0] > x+off else g[0], g[1]) for g in galaxies]
            off += expansion

    # expand vertically
    off = 0
    for y in range(height + 1):
        s = set()
        for x in range(width + 1):
            s.add(grid[x, y][0])
        if len(s) == 1 and s.pop() == '.':
            galaxies = [(g[0], g[1] + expansion if g[1] > y+off else g[1]) for g in galaxies]
            off += expansion

    acc = 0
    for i in range(len(galaxies)):
        print(f'{i} / {len(galaxies)}', end='\r')
        for j in range(i, len(galaxies)):
            acc += vdistm(galaxies[i], galaxies[j])

    return acc


setday(11)

print('part1:', solve(2) )
print('part2:', solve(1_000_000) )
