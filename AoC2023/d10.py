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
    'S': (SOUTH,) #, WEST),  # HARDCODED fix later
}

def get_next(pos, prev):
    adj = [vadd(pos,c) for c in valids[grid[pos]]]
    if prev in adj:
        adj.remove(prev)
    # print(adj)
    return adj[0]

def p1():
    start = inverse['S'][0]
    pos = start
    prev = (0,0)
    path = []
    while pos != start or prev == (0,0):
        path.append(pos)
        pos, prev = get_next(pos, prev), pos
        # print(pos)
    # print(path, len(path))
    return len(path)//2


# def flood_fill(pos, grid, path, seen):
#     queue = [pos]
#     splat = []
#     while queue:
#         pos = queue.pop()
#         for dir in DIRS:
#             nxt = vadd(dir, pos)
#             if nxt in path:
#                 continue
#             if nxt in seen:
#                 continue
#             if nxt not in grid:
#                 print(pos, 'fell off grid', splat)
#                 return []
#             queue.append(nxt)
#             splat.append(nxt)
#             seen.add(nxt)
#         # print(queue)
#     splat.append(pos)
#     return splat

def flood_fill(pos, grid, path):
    queue = {pos}
    splat = []
    seen = set()

    i = 0
    while queue:
        i += 1
        # print(len(queue))

        if i % 1000 == 0:
            print_2d(' ', grid, {k: '@' for k in splat}, constrain=(-256, -256, 512, 512))

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
            splat.append(nxt)
            seen.add(nxt)
    splat.append(pos)
    return splat

# def p2():
#     start = inverse['S'][0]
#     pos = start
#     prev = (0, 0)
#     path = []
#     while pos != start or prev == (0, 0):
#         path.append(pos)
#         pos, prev = get_next(pos, prev), pos
#         # print(pos)
#     # print(path, len(path))
#     path = set(path)
#     seen = set()
#     print_2d('.', grid, {k:'@' for k in path})
#     splotch = []
#     # width = max(grid.keys(), key=lambda x:x[0])[0]
#     # height = max(grid.keys(), key=lambda x:x[1])[1]
#     # print(width, height)
#     # corners = [(0,0), (width,0), (0,height), (width, height)]
#     to_add = {}
#     for k in grid:
#         for dir in DIRS:
#             nxt = vadd(dir, k)
#             if nxt not in grid:
#                 to_add[nxt] = '.'
#     grid.update(to_add)
#     splotch = flood_fill((0,0), grid, path, seen)
#     inv = set(grid.keys())
#     for c in splotch:
#         # print(c, '<- c', len(splotch))
#         if c in inv:
#             inv.remove(c)
#     for c in path:
#         if c in inv:
#             inv.remove(c)
#     print()
#     print_2d('.', grid, {k: '@' for k in inv}, {k: '_' for k in path})
#     return len(inv)



def p2():
    def get_next(pos, prev):
        adj = [vadd(c, vadd(pos, c)) for c in valids[scaled_grid[pos]]]
        # adj = (adj[0] * 2, adj[1] * 2)
        if prev in adj:
            adj.remove(prev)
        # print(adj)
        return adj[0]

    scaled_grid = {}
    for k,v in grid.items():
        scaled_grid[(k[0]*2, k[1]*2)] = v

    print_2d('.', scaled_grid)

    start = vmul(inverse['S'][0], (2,2))
    pos = start
    prev = (0,0)
    path = []
    while pos != start or prev == (0,0):
        path.append(pos)
        pos, prev = get_next(pos, prev), pos
        in_between = ((pos[0] + prev[0]) // 2, (pos[1] + prev[1]) // 2)
        print(pos, prev, in_between)
        path.append(in_between)

    # outset twice
    for i in range(2):
        to_add = {}
        for k in scaled_grid:
            for dir in DIRS:
                nxt = vadd(dir, k)
                if nxt not in scaled_grid:
                    to_add[nxt] = '.'
        scaled_grid.update(to_add)

    print_2d(' ', scaled_grid, {k: '@' for k in path}, constrain=(-256, -256, 512, 512))

    splotch = flood_fill((0,0), scaled_grid, path)
    inv = set(scaled_grid.keys())
    for c in splotch:
        # print(c, '<- c', len(splotch))
        if c in inv:
            inv.remove(c)
    for c in path:
        if c in inv:
            inv.remove(c)
    # print()
    # print_2d('.', grid, {k: '@' for k in inv}, {k: '_' for k in path})

    print('INV', inv)
    print('\n')
    evens = [c for c in inv if c[0]&1==0 and c[1]&1==0]
    print('EVENS', evens)

    return len(evens)


setday(10)

# data = parselines()
# data = parselines(get_ints)
grid, inverse, unique = parsegrid()

# print('part1:', p1() )
print('part2:', p2() )
