import math
import random
import re
import sys
from collections import defaultdict

import numpy as np

from aoc import memo


def get_int(bit_array, rev):
    if rev:
        return sum(v << i for i, v in enumerate(bit_array))
    else:
        return sum(v << i for i, v in enumerate(reversed(bit_array)))


def get_edge(tile, direction, rev=False):
    if direction == 0:  # UP
        if rev:
            return get_int(tile[0, :], True)
        else:
            return get_int(tile[0, :], False)
    if direction == 2:  # DOWN
        if rev:
            return get_int(tile[-1, :], True)
        else:
            return get_int(tile[-1, :], False)
    if direction == 3:  # LEFT
        if rev:
            return get_int(tile[:, 0], True)
        else:
            return get_int(tile[:, 0], False)
    if direction == 1:  # RIGHT
        if rev:
            return get_int(tile[:, -1], True)
        else:
            return get_int(tile[:, -1], False)


def apply_orientation(arr, rotation, flip_v, flip_h):
    arr_copy = np.copy(arr)
    if rotation:
        arr_copy = np.rot90(arr_copy, rotation)
    if flip_v:
        arr_copy = np.flip(arr_copy, 1)
    if flip_h:
        arr_copy = np.flip(arr_copy, 0)
    return arr_copy


def get_mutated_tile(tile, rotation, flip_v, flip_h):
    # @memo
    return apply_orientation(tiles[tile], rotation, flip_v, flip_h)


def find_match(tile, side, orientation):
    target = get_mutated_tile(tile, *orientation)
    opposite_side = (side + 2) % 4
    matches = []
    side_to_match = get_edge(target, side)
    # print(side_to_match, 'was found this many times:', all_edges_ct[side_to_match])
    for e in all_tiles:
        if side_to_match not in all_tile_edges[e]:  # MASSIVE speedup
            continue
        for rotations in range(0, 2):
            for flipv in range(0, 2):
                for fliph in range(0, 2):
                    if tile == e:
                        continue
                    candidate = get_mutated_tile(e, rotations, flipv, fliph)
                    if side_to_match == get_edge(candidate, opposite_side):
                        return e, (rotations, flipv, fliph)


corners = [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # oops
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def get_adj_unfilled(x, y):
    adjs = []
    for m_x, m_y in dirs:
        adj_x, adj_y = x + m_x, y + m_y
        try:
            adj = tile_map[adj_x, adj_y]
            if adj_x < 0 or adj_y < 0:
                continue
            # print('got', adj_x, adj_y)
            if adj == -1:
                adjs.append((adj_x, adj_y))
        except IndexError:
            continue
    return adjs


def start_filling_at(x, y):
    # print('starting to fill at ', x, y)
    unfilled = get_adj_unfilled(x, y)
    # print('unfilled:', unfilled)
    if len(unfilled) == 0:
        return
    # random.shuffle(unfilled)  # makes it more interesting
    for coords_to_fill in unfilled:
        if tile_map[coords_to_fill] != -1:
            return
        # print('offset:', (coords_to_fill[0] - x, coords_to_fill[1] - y))
        direction = dirs.index((coords_to_fill[0] - x, coords_to_fill[1] - y))
        # print('calced direction', coords_to_fill[0], x, coords_to_fill[1], y, '=', direction)
        found_id, found_orientation = find_match(tile_map[x, y], direction, orientations[x, y])

        tile_map[coords_to_fill] = found_id
        # print('coords:', coords_to_fill)
        # print(found_id, found_orientation, orientations[coords_to_fill])
        orientations[coords_to_fill] = found_orientation

        # print(get_mutated_tile(tile_map[x, y], *orientations[x, y]), '\n MATCHES on side', direction, '\n',
        #       get_mutated_tile(found_id, *found_orientation))

        print(tile_map)
        start_filling_at(*coords_to_fill)


def render_array(bd):
    # as_str = np.array2string(np.swapaxes(bd, 0, 1), max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
    as_str = np.array2string(bd, max_line_width=220, separator=' ', threshold=1000, edgeitems=1000,
                             formatter={'str_kind': lambda x: x})
    # print('\x1b[1;1H\r', re.sub('[\[\]]', '', as_str), end='\n')
    print('', re.sub('[\[\]]', '', as_str), end='\n')


def search_for_sea_monsters_at(to_search, x, y):
    try:
        for y2, x2 in sea_set:
            # print('looking in ', x+x2, y+y2)
            point = to_search[x + x2, y + y2]
            if point != '#':
                # print(point)
                return False
        for y2, x2 in sea_set:
            to_search[x + x2, y + y2] = 'O'
        return True
    except IndexError:
        return False


def search_for_sea_monsters():
    monster_ct = 0
    for rotations in range(0, 2):
        for flipv in range(0, 2):
            for fliph in range(0, 2):
                to_search = apply_orientation(full_map, rotations, flipv, fliph)
                for map_x, map_y in np.ndindex(full_map.shape):
                    res = search_for_sea_monsters_at(to_search, map_x, map_y)
                    # print(map_x,map_y,res, rotations, flipv, fliph)
                    if res:
                        monster_ct += 1
                if monster_ct > 0:
                    # print(rotations, flipv, fliph, monster_ct)
                    # render_array(to_search)
                    pass
    return monster_ct


def p2():
    return None


f = 'd20.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [[x for x in tile.split('\n')] for tile in file.read().strip('\n').split('\n\n')]

tiles = {}
for tile in data:
    key = [int(i) for i in tile.pop(0).replace(':', '').split(' ') if i.isdigit()][0]
    tile = [[1 if y == '#' else 0 for y in x] for x in tile]
    tiles[key] = np.array(tile, dtype=np.uint8)

all_tile_edges = {}
all_edges_ct = defaultdict(int)
for k, v in tiles.items():
    edges = set()
    all_tile_edges[k] = edges

    for d in range(4):
        edges.add(get_edge(v, d, True))
        edges.add(get_edge(v, d, False))

    for edge in edges:
        all_edges_ct[edge] += 1

    pass
# print(all_edges_ct)

corner_tiles = set()
all_tiles = set()
ret = 1
for tile, edges in all_tile_edges.items():
    uniques = 0
    for edge in edges:
        if all_edges_ct[edge] == 1:
            uniques += 1
    if uniques == 4:
        corner_tiles.add(tile)
        ret *= tile
    all_tiles.add(tile)

print(f'part1: {ret}')

edge_len = int(math.sqrt(len(tiles)))
tile_size = 10

# map of keys
tile_map = np.ndarray((edge_len, edge_len), dtype=int)

orientations = np.ndarray((edge_len, edge_len), dtype=tuple)

tile_map.fill(-1)
orientations.fill(tuple())
# print(tile_map)


tile_map[0, 0] = corner_tiles.pop()
top_left = [get_edge(tiles[tile_map[0, 0]], i, False) for i in range(0, 4)]
tl_rot = [all_edges_ct[e] for e in top_left]
rot = 0
while tl_rot != [1, 2, 2, 1]:
    tl_rot = tl_rot[1:] + tl_rot[:1]
    rot += 1
# print(top_left, tl_rot, rot)
orientations[0, 0] = (rot, 0, 0)

all_tiles |= corner_tiles

start_filling_at(0, 0)

# print(tile_map)
# print(orientations)

inset_size = tile_size - 2

full_map = np.full((edge_len * inset_size, edge_len * inset_size), dtype=str, fill_value='.')

sea_monster = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
'''.strip('\n').split('\n')
sea_monster_arr = [[c for c in line] for line in sea_monster]
sea_set = set()
for x, line in enumerate(sea_monster):
    for y, c in enumerate(line):
        if c == '#':
            sea_set.add((y, x))
# print(sea_set)
# print('SsSsSsS')
# for line in sea_monster:
#     print(line)
# print('SsSsSsS\n', sea_set)

for ix, iy in np.ndindex(tile_map.shape):
    # full_map = np.full((edge_len * inset_size, edge_len * inset_size), dtype=str, fill_value='.')
    # print(ix, iy, tile_map[ix, iy])
    to_copy = get_mutated_tile(tile_map[ix, iy], *orientations[ix, iy])
    to_copy = apply_orientation(to_copy, 1, 0, 1)
    # print(to_copy)
    for y in range(1, 9):
        for x in range(1, 9):
            full_map[ix * inset_size + x - 1, iy * inset_size + y - 1] = '#' if to_copy[x, y] == 1 else '.'
    # render_array(full_map)

ct = search_for_sea_monsters()
# print(ct, len(sea_set))
# print((full_map == "#"), (full_map == "#").sum())

print(f'part1: {ret}')
print(f'part2: {(full_map == "#").sum() - (ct * len(sea_set))}')

# render_array(full_map)
# print('\n\nRotated 90 deg:')
# render_array( apply_orientation(full_map, 1, 0, 1) )
