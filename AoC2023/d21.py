from aoc import *

def solve():
    _, _, w, h = grid_bounds(grid)
    w += 1
    h += 1

    cycle_len = 26501365 // w

    tiles = {unique['S']}
    visited, visited_alt = set(), set()

    steps = []

    step = 1
    while len(steps) < 3:
        new_tiles = set()
        while tiles:
            tile = tiles.pop()
            for dir in DIRS:
                neighbor = vadd(tile, dir)
                if neighbor in visited:
                    continue
                if grid[(neighbor[0] % w, neighbor[1] % h)] != '#':
                    new_tiles.add(neighbor)
                    visited.add(neighbor)
        tiles = new_tiles

        if step == 64:
            p1 = len(visited)

        if (step % w) == 65:
            steps.append(len(visited))
            print(step)
            # print(steps)

        visited, visited_alt = visited_alt, visited
        step += 1

        # print_2d(' ', grid, {k:'~' for k in visited}, {k:'@' for k in tiles}, constrain=(-1000, -1000, 1000, 1000))
        # input()

    # I still only have an extremely vague idea why this works
    diff0 = steps[0]
    diff1 = steps[1] - steps[0]
    diff2 = steps[2] - steps[1]
    return p1, diff0 + diff1 * cycle_len + (cycle_len * (cycle_len - 1) // 2) * (diff2 - diff1)


def p2():
    _, _, w, h = grid_bounds(grid)
    w += 1
    h += 1

    tiles = {unique['S']}
    visited, visited_alt = set(), set()

    for step in range(w//2 + w*2):
        new_tiles = set()
        while tiles:
            tile = tiles.pop()
            for dir in DIRS:
                neighbor = vadd(tile, dir)
                if neighbor in visited:
                    continue
                if grid[(neighbor[0] % w, neighbor[1] % h)] != '#':
                    new_tiles.add(neighbor)
                    visited.add(neighbor)
        tiles = new_tiles

        visited, visited_alt = visited_alt, visited
        step += 1

    # print_2d(' ', grid, {k:'~' for k in visited}, {k:'@' for k in tiles}, constrain=(-1000, -1000, 1000, 1000))

    points_of_interest = [
                (-1,-2),( 0,-2),( 1,-2),
        (-2,-1),(-1,-1),( 0,-1),( 1,-1), ( 2,-1),
        (-2, 0),(-1, 0),( 0, 0),( 1, 0), ( 2, 0),
        (-2, 1),(-1, 1),( 0, 1),( 1, 1), ( 2, 1),
                (-1, 2),( 0, 2),( 1, 2)
    ]

    poi_map = [
                  'top_l_o', 'point_u','top_r_o',
        'top_l_o', 'top_l_i',  'even',  'top_r_i',  'top_r_o',
        'point_l',  'even',    'odd',     'even',   'point_r',
        'bot_l_o', 'bot_l_i',  'even',   'bot_r_i', 'bot_r_o',
                   'bot_l_o', 'point_d','bot_r_o'
    ]

    parts_dict = {}

    for label, offset in zip(poi_map, points_of_interest):
        topl, botr = vmul((w,h),offset), vmul((w,h),vadd(offset,(1,1)))

        acc = 0
        for x in range(topl[0], botr[0]):
            for y in range(topl[1], botr[1]):
                if (x,y) in visited_alt:
                    acc += 1

        print(label,offset, topl, 'to', botr, '=', acc)

        parts_dict[label] = acc

    print(parts_dict)

    cycle_len =  26501365 // w

    counts_of_parts = {
        ('odd',):  (((2 * ((cycle_len//2) - 1)) + 1) ** 2),
        ('even',): ( (2 * ( cycle_len//2)     )      ** 2),
        ('point_u', 'point_l', 'point_r', 'point_d'): 1,
        ('top_l_o', 'top_r_o', 'bot_l_o', 'bot_r_o'): cycle_len,
        ('top_l_i', 'top_r_i', 'bot_l_i', 'bot_r_i'): cycle_len-1
    }

    print(counts_of_parts)

    acc = 0
    for keyset, mult in counts_of_parts.items():
        for key in keyset:
            acc += parts_dict[key] * mult

    return acc

setday(21)

grid, inverse, unique = parsegrid()

print('part1: %s\npart2: %s' % solve())
print('part2 (alt): %s' % p2())
