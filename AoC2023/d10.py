from aoc import *

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

valids = {
    '|': (NORTH, SOUTH),
    '-': (EAST, WEST),
    'L': (NORTH, EAST),
    'J': (NORTH, WEST),
    '7': (SOUTH, WEST),
    'F': (SOUTH, EAST),
    '.': (),
}

verbose = '-v' in sys.argv or '--verbose' in sys.argv

def p1():
    def get_next(pos, prev):
        adj = [vadd(pos, c) for c in valids[grid[pos]]]
        if prev in adj:
            adj.remove(prev)

        return adj[0]

    start = inverse['S'][0]
    pos = start
    prev = (0,0)
    path = []
    while pos != start or prev == (0,0):
        path.append(pos)
        pos, prev = get_next(pos, prev), pos

    return len(path)//2


def p2():
    def get_next(pos, prev):
        adj = [vadd(c, vadd(pos, c)) for c in valids[scaled_grid[pos]]]
        if prev in adj:
            adj.remove(prev)
        return adj[0]

    def flood_fill(pos, grid, path):
        queue = {pos}
        splat = set()
        seen = set()

        while queue:
            # print_2d(' ', grid, {k: '@' for k in splat}, constrain=(-256, -256, 512, 512))

            pos = queue.pop()
            for dir in DIRS:
                nxt = vadd(dir, pos)
                if nxt in path:
                    continue
                if nxt in seen:
                    continue
                if nxt not in grid:
                    continue

                queue.add(nxt)
                splat.add(nxt)
                seen.add(nxt)
        splat.add(pos)
        return splat

    # upscale our grid by 2x, so we can check in between pipes
    scaled_grid = {}
    for k,v in grid.items():
        scaled_grid[(k[0]*2, k[1]*2)] = v

    start = vmul(inverse['S'][0], (2,2))
    pos = start
    prev = (0,0)
    path = set()
    while pos != start or prev == (0,0):
        path.add(pos)
        pos, prev = get_next(pos, prev), pos
        in_between = ((pos[0] + prev[0]) // 2, (pos[1] + prev[1]) // 2)
        path.add(in_between)

    # outset twice
    for i in range(2):
        to_add = {}
        for k in scaled_grid:
            for dir in DIRS:
                nxt = vadd(dir, k)
                if nxt not in scaled_grid:
                    to_add[nxt] = '.'
        scaled_grid.update(to_add)

    # find everything outside the loop
    splotch = flood_fill((-1,-1), scaled_grid, path)

    # now remove that, and the path, from all known positions
    inv = set(scaled_grid.keys()) - splotch - path

    # finally cut that down to "original" coords
    evens = [c for c in inv if c[0]&1==0 and c[1]&1==0]

    if verbose:
        print('enclosed:')
        print_2d('.', scaled_grid, {k: 'I' for k in inv}, {k: '~' for k in path}, constrain=(-256, -256, 512, 512))

        def downscale(d):
            return {(k[0]//2, k[1]//2):v for k,v in d.items() if k[0]&1==0 and k[1]&1==0}

        print('\ndownscaled:')
        print_2d('.', downscale(scaled_grid), downscale({k: 'I' for k in inv}), downscale({k: '~' for k in path}))

    return len(evens)


setday(10)

grid, inverse, unique = parsegrid()

# find a direction S can go
for dir in DIRS:
    s_adj = vadd(dir, inverse['S'][0])
    if s_adj in grid and vmul((-1,-1), dir) in valids[grid[s_adj]]:
        valids['S'] = (dir,)
        break

print('part1:', p1() )
print('part2:', p2() )
