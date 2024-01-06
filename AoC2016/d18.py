from aoc import *


def solve(h):
    w = max(grid.keys(), key=itemgetter(0))[0] + 1
    traps = set(inverse['^'])
    adj = [(-1,-1), (0,-1), (1,-1)]
    seen = set()
    for y in range(h):
        row = set()
        for x in range(w):
            a,b,c = [vadd((x,y), d) in traps for d in adj]
            if (a and b and not c) or (not a and b and c) or (a and not b and not c) or (not a and not b and c):
                row.add((x,y))
        traps |= row
        row = frozenset(x for x,y in row)
        if row in seen:
            print('cycling at row', y)
            break
        seen.add(row)
    # print_2d('.', {k:'^' for k in traps})
    return (h*w) - len(traps)


setday(18)

grid, inverse, unique = parsegrid()

print('part1:', solve(40) )
print('part2:', solve(400_000) )
