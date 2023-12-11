import copy


from aoc import *


def swap_axes(grid):
    new = []
    for x in range(len(grid[0])):
        line = []
        for y in range(len(grid)):
            line.append(grid[y][x])
        new.append(''.join(line))
    return new


def p1():
    g = copy.deepcopy(data)
    for i in range(2):
        for y in range(len(g) - 1, -1, -1):
            line = [c for c in g[y]]
            if len(set(line)) == 1:
                g.insert(y, g[y])
        g = swap_axes(g)
    grid = {}
    inverse = defaultdict(list)
    for y, line in enumerate(g):
        for x, c in enumerate(line):
            grid[(x,y)] = c
            inverse[c].append((x,y))
    print_2d('.', grid)
    print(sorted(inverse['#']))
    acc = 0
    for a in inverse['#']:
        for b in inverse['#']:
            if a == b:
                continue
            acc += vdistm(a,b)
    return acc // 2


def p2_ded():
    # works, but wbfs is too slow (oops...)
    def get_neighbors(c):
        neighbors = []
        for dir in DIRS:
            n = vadd(dir, c)
            if n not in grid:
                continue
            neighbors.append((n, grid[n][1]))
        return neighbors

    grid, inverse, unique = parsegrid()
    for k,v in grid.items():
        grid[k] = (v, 1)
    width, height = max(grid.keys(), key=itemgetter(0))[0], max(grid.keys(), key=itemgetter(1))[1]
    for x in range(width+1):
        s = set()
        for y in range(height+1):
            s.add(grid[x,y][0])
        # print(s)
        if len(s) == 1:
            for y in range(height+1):
                grid[x,y] = (grid[x,y][0],  10)
                # grid[x, y] = (grid[x, y][0], grid[x, y][1] * 10)

    for y in range(height+1):
        s = set()
        for x in range(width+1):
            s.add(grid[x,y][0])
        # print(s)
        if len(s) == 1:
            for x in range(width+1):
                grid[x,y] = (grid[x,y][0],  10)
                # grid[x, y] = (grid[x, y][0], grid[x, y][1] * 10)

    acc = 0
    done = set()
    ct = 0
    for i, a in enumerate(inverse['#']):
        print(f'{i} / {len(inverse["#"])}', end='\r')
        for b in inverse['#']:
            # print(a, b, end=' ')
            if a == b:
                continue
            pair = frozenset([a, b])
            if pair in done:
                continue
            ct += 1

            result = wbfs(a, b, get_neighbors)

            acc += sum([grid[c][1] for c in result]) - 1
            done.add(pair)

    return acc

def p2(expansion):
    expansion -= 1
    grid, inverse, unique = parsegrid()
    galaxies = inverse['#']

    for k, v in grid.items():
        grid[k] = v
    width, height = max(grid.keys(), key=itemgetter(0))[0], max(grid.keys(), key=itemgetter(1))[1]

    off = 0
    for x in range(width + 1):
        s = set()
        s_l = []
        for y in range(height + 1):
            s.add(grid[x,y])
            s_l.append(grid[x,y])
        if len(s) == 1:
            galaxies = [(g[0] + expansion if g[0] > x+off else g[0], g[1]) for g in galaxies]
            off += expansion
        print(s_l)
        print(x, s, galaxies)

    off = 0
    for y in range(height + 1):
        s = set()
        for x in range(width + 1):
            s.add(grid[x, y][0])
        # print(s)
        if len(s) == 1:
            galaxies = [(g[0], g[1] + expansion if g[1] > y+off else g[1]) for g in galaxies]
            off += expansion

    # for _ in range(1):
    #     x = 0
    #     while x < width+1:
    #         row = [grid[x,y] for y in range(height+1)]
    #         if len(set(row)) == 1:
    #             # print(x, galaxies, '\n', [(g[0] + 1 if g[0] > x else g[0], g[1]) for g in galaxies], '\n')
    #             galaxies = [(g[0] + 1 if g[0] > x else g[0], g[1]) for g in galaxies]
    #             x += 1
    #         x += 1
    #     # galaxies = [(y,x) for x,y in galaxies]


    print_2d('.', {k:'#' for k in galaxies})
    print(sorted(galaxies))

    acc = 0
    for a in galaxies:
        for b in galaxies:
            if a == b:
                continue
            acc += vdistm(a,b)

    print(acc // 2)



setday(11)

data = parselines()

# for x in range(len(data[0])-1, -1, -1):
#     col = [data[y][x] for y in range(len(data)-1, -1, -1)]
#     print(col)

# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2(2) )
print('part2:', p2(1_000_000) )
