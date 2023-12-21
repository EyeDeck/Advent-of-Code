from aoc import *


def p1():
    tiles = {unique['S']}
    for step in range(64):
        new_tiles = set()
        while tiles:
            tile = tiles.pop()
            for dir in DIRS:
                neighbor = vadd(tile, dir)
                if grid[neighbor] != '#':
                    new_tiles.add(neighbor)
        tiles = new_tiles
        # print_2d(' ', grid, {k:'@' for k in tiles})
        # print(len(tiles))
    return len(tiles)


def p2():
    _, _, w, h = grid_bounds(grid)
    print(w,h)
    w += 1
    h += 1
    #
    # grid_starts = [
    #     (-1,-1), ( 0,-1), ( 1,-1),
    #     (-1, 0), ( 0, 0), ( 1, 0),
    #     (-1, 1), ( 0, 1), ( 1, 1),
    # ]
    #
    # sets = set()
    # for start_point in grid_starts:
    #     print()
    #     tiles = {tuple(((n+1)*65) for n in start_point)}
    #     # print(tiles)
    #     for step in range(65): # range(131+65):
    #         new_tiles = set()
    #         while tiles:
    #             tile = tiles.pop()
    #             for dir in DIRS:
    #                 neighbor = vadd(tile, dir)
    #                 if neighbor[0] < 0 or neighbor[0] > w:
    #                     continue
    #                 if neighbor[1] < 0 or neighbor[1] > h:
    #                     continue
    #                 if grid[neighbor] != '#':
    #                     new_tiles.add(neighbor)
    #         tiles = new_tiles
    #     print_2d(' ', grid, {k: '@' for k in tiles}, constrain=(-1000, -1000, 1000, 1000))
    #     hashable = frozenset(tiles)
    #     if hashable in sets:
    #         print('already seen')
    #     sets.add(hashable)
    #     print(start_point, '=', len(tiles))

    # 26501365 // 131 = 202300
    # 26501365 %  131 = 65

    #  X X
    #   X   =  7388 tiles
    #  X X

    #   X
    #  X X  =  7424 tiles
    #   X

    # 3812 5665 3801
    #
    # 5650 7388 5680
    #
    # 3805 5665 3801

    # so...
    #                5665
    #           3812 7388 3801
    #      3812 7388 7424 7388 3801
    # 5650 7388 7424 7388 7424 7388 5680
    #      3805 7388 7424 7388 3801
    #           3805 7388 3801
    #                5665

    #                     5665
    #                3812 7424 3801
    #           3812 7388 7388 7388 3801
    #      3812 7388 7388 7424 7388 7388 3801
    # 5650 7424 7388 7424 7388 7424 7388 7424 5680
    #      3805 7388 7388 7424 7388 7388 3801
    #           3805 7388 7388 7388 3801
    #                3805 7424 3801
    #                     5665

    # middle +
    # straights
    # inner corners
    # diagonals
    # outer points

    # (7388) +
    # ((202300-1) * 7424 * 4) +
    # (((202300 * 202301) // 2) * 7388 * 4 ) - (202300 * 7388 * 4)) +
    # ((3812 + 3801 + 3805 + 3801) * 202300) +
    # (5665 + 5650 + 5680 + 5665) +

    # (7388) + ((202300-1) * 7424 * 4) + ((((202300 * 202301) // 2) * 7388 * 4 ) - (202300 * 7388 * 4)) + ((3812 + 3801 + 3805 + 3801) * 202300) + (5665 + 5650 + 5680 + 5665)

    # too low: 23570681402
    # too low: 151181876491452
    # too low: 604718182160052
    # not right: 2424693743732066
    # not right: 606164518217666 ???
    # not right: 606188489692441 ...

    s          = 26501365 // w
    # a = 7388
    #
    # point_u    = 5665 * 1
    # point_l    = 5650 * 1
    # point_r    = 5680 * 1
    # point_d    = 5665 * 1
    # orth       = 7424 * (s-1) * 4
    # inner_corn = ((7388 * ((s-1) * s) // 2) - (7388 * (s-1))) * 4
    # top_l_diag = 3812 * (s-1)
    # top_r_diag = 3801 * (s-1)
    # bot_l_diag = 3805 * (s-1)
    # bot_r_diag = 3801 * (s-1)
    # print( middle +
    #        point_u + point_l + point_r + point_d +
    #        orth + inner_corn +
    #        top_l_diag + top_r_diag + bot_l_diag + bot_r_diag)

    # ((2 * s) +1) ** 2
    # ((2 * s) ** 2

    # s          =  26501365 // 131
    #
    # middle     = 7388 * (((2 * ((s//2)-1)) + 1) ** 2)
    # off        = 7424 * ((2 * ((s//2))) ** 2)
    #
    # point_u    = 5665 * 1
    # point_l    = 5650 * 1
    # point_r    = 5680 * 1
    # point_d    = 5665 * 1
    #
    # top_l_diag_a = 959 * (s+1)
    # top_l_diag_b = 6541 * (s+0)
    #
    # top_r_diag_a = 982 * (s+1)
    # top_r_diag_b = 6548 * (s+0)
    #
    # bot_l_diag_a = 973 * (s+1)
    # bot_l_diag_b = 6533 * (s+0)
    #
    # bot_r_diag_a = 979 * (s+1)
    # bot_r_diag_b = 6556 * (s+0)
    #
    # print( middle + off +
    #        point_u + point_l + point_r + point_d +
    #        top_l_diag_a + top_l_diag_b + top_r_diag_a + top_r_diag_b +
    #        bot_l_diag_a + bot_l_diag_b + bot_r_diag_a + bot_r_diag_b)

    # ...this isn't quite working.



    tiles = {unique['S']}
    visited = set()
    other_set = set()

    steps = []
    # toggle = False
    step = 0
    while len(steps) < 3:
        # toggle = not toggle
        # if toggle and step == w//2 or (step % w) == 65:
        # print(step)
        if step == 64:
            print('step 64', len(visited))

        if (step % w) == 65: # and step & 1 == 1:
            # steps.append((step, len(tiles), len(visited), len(other_set), len(tiles.union(visited))))
            steps.append(len(visited))
            print(steps)

        visited, other_set = other_set, visited

        # (tiles_a if toggle else tiles_b).update(tiles)

        new_tiles = set()
        while tiles:
            tile = tiles.pop()
            for dir in DIRS:
                neighbor = vadd(tile, dir)
                if neighbor in visited:
                    continue
                # print(neighbor, (neighbor[0] % w, neighbor[1] % h))
                if grid[(neighbor[0] % w, neighbor[1] % h)] != '#':
                    new_tiles.add(neighbor)
                    visited.add(neighbor)
        tiles = new_tiles
        step += 1
        # full = len([c for c in grid.keys() if c in tiles])
        # print(toggle, step)

        # print_2d(' ', grid, {k:'~' for k in visited}, {k:'@' for k in tiles}, constrain=(-1000, -1000, 1000, 1000))
        # input()
    print(w + (26501365 % w))
    print(len(tiles))

    diff0 = steps[0]
    diff1 = steps[1] - steps[0]
    diff2 = steps[2] - steps[1]
    print(diff0, diff1, diff2)
    return diff0 + diff1 * s + (s * (s - 1) // 2) * (diff2 - diff1)

setday(21)

grid, inverse, unique = parsegrid()

# print('part1:', p1() )
print('part2:', p2() )
