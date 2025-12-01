import collections
import random
from math import *
from aoc import *


def grid_slice(d, start, end):
    (x1, y1), (x2, y2) = start, end
    if x1 == x2 and y1 != y2:
        step = (0, 1 if y2 > y1 else -1)
    elif x1 != x2 and y1 == y2:
        step = (1 if x2 > x1 else -1, 0)
    else:
        raise ValueError('Slice should be a straight line')

    p = start
    l = [d[p]]
    # print(step)
    while True:
        p = vadd(p, step)
        l.append(d[p])
        if p == end:
            break
    return l


def solve():
    edges_to_ids = defaultdict(set)
    ids_to_edges = defaultdict(set)

    # hard_coded, oh well
    edge_steps = [
        [(0, 0), (9, 0)],
        [(9, 0), (9, 9)],
        [(0, 9), (9, 9)],
        [(0, 0), (0, 9)]
    ]

    for piece_id, piece_grid in data.items():
        # print_2d(' ', piece_grid)
        x1, y1, x2, y2 = grid_bounds(piece_grid)

        edges = [grid_slice(piece_grid, start_pos, end_pos) for start_pos, end_pos in edge_steps]
        for edge in edges:
            s, s_r = ''.join(edge), ''.join(reversed(edge))
            edges_to_ids[s].add(piece_id)
            edges_to_ids[s_r].add(piece_id)
            ids_to_edges[piece_id].add(s)
            ids_to_edges[piece_id].add(s_r)
    edges_with_connections = {k: v for k, v in edges_to_ids.items() if len(v) == 2}
    edges_without_connections = collections.Counter([list(v)[0] for k, v in edges_to_ids.items() if len(v) == 1])
    corner_tiles = [k for k, v in edges_without_connections.items() if v == 4]
    edge_tiles = [k for k, v in edges_without_connections.items() if v == 2]

    # print(edges_to_ids)


    # print(corner_tiles)
    yield prod(corner_tiles)
    # input()

    print(edges_with_connections)
    input()

    unfound_tiles = set(data.keys())
    unfound_edges = {k for k, v in edges_to_ids.items()}
    first_corner = corner_tiles.pop()

    puzzle_grid = {(0, 0): {'tile_id': first_corner, 'grid': data[first_corner], 'unfound': edges_to_ids[first_corner]}}
    unfound_tiles.remove(first_corner)

    for grid_id, grid in data.items():
        all_rots = []
        r = grid
        for _ in range(4):
            r = rotate_2d(r, 90, in_place=True, width=9, height=9)
            print(r)
            all_rots.append(r)
            all_rots.append({(k[1], k[0]): v for k, v in r.items()})
        data[grid_id] = all_rots

    dir_map = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}

    # edges_to_ids
    # ids_to_edges
    def find_next_tile(cur):
        current_data = puzzle_grid[cur]
        current_grid = current_data['grid']
        current_id = current_data['tile_id']
        current_edges = current_data['unfound']
        for edge in current_edges:
            adjacent_tile_id = [n for n in edges_to_ids[edge] if n != current_id]
            if not adjacent_tile_id or adjacent_tile_id[0] not in unfound_tiles:
                continue
            adjacent_tile_id = adjacent_tile_id[0]
            print(adjacent_tile_id)
            for current_edge_index, current_edge_slice in enumerate(edge_steps):
                opposite_slice = current_edge_index - 2
                current_slice = grid_slice(current_grid, *current_edge_slice)
                print('comparing')
                print_2d(' ', current_grid)
                print('to')
                for adjacent_tile_grid in data[adjacent_tile_id]:
                    adjacent_slice = grid_slice(adjacent_tile_grid, *edge_steps[opposite_slice])
                    if adjacent_slice == current_slice:
                        print('found match!', adjacent_slice, current_slice, )
                        next_loc = vadd(cur, dir_map[current_edge_index])
                        puzzle_grid[next_loc] = {'tile_id': adjacent_tile_id, 'grid': adjacent_tile_grid}
                        unfound_tiles.remove(adjacent_tile_id)
                        return next_loc

                    print_2d(' ', adjacent_tile_grid)
            input()

    cur = (0, 0)
    while unfound_tiles:
        print('cur', cur)
        print('a', unfound_tiles)
        print('b', puzzle_grid.keys())
        cur = find_next_tile(cur)
        if not cur:
            cur = random.choice(tuple(puzzle_grid.keys()))

            # print(current_id, edge,

        # for found_tile_id, found_tile_data in puzzle_grid.items():
        #     uf = found_tile_data['unfound_edges']
        #     if not uf:
        #         continue
        #     print(found_tile_id, found_tile_data)
        #
        #     for unfound_edge in uf:
        #         matching_tiles = edges_to_ids[unfound_edge]
        #         if len(matching_tiles) == 1:
        #             del edges_to_ids[unfound_edge]
        #             found_tile_data['unfound_edges'].remove(unfound_edge)
        #             print('aaa', ids_to_edges[found_tile_id])
        #         print(matching_tiles)
        #     input()

    print(puzzle_grid)

    # print(puzzle_grid)
    # print(ids_to_edges)
    # print(edges_with_connections)

    # while edges_to_ids:
    #     pass

    yield None


def p2():
    return None


setday(20)

# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

with open_default() as file:
    data_raw = [chunk.strip().split('\n') for chunk in file.read().strip().split('\n\n')]
data = defaultdict(dict)
for tile in data_raw:
    n = get_ints(tile[0])[0]
    for y, line in enumerate(tile[1:]):
        for x, c in enumerate(line):
            data[n][(x, y)] = c

# print(data)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

gen = solve()
print('part1:', next(gen))  # 00:35:47
print('part2:', next(gen))

# print('part1: %d\npart2: %d' % solve())
