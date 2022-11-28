import string
import sys
from collections import defaultdict
import copy
import re
import sys
from collections import defaultdict
from operator import itemgetter

import numpy as np


def render(board, overlay=None):
    to_str = []
    for y, line in enumerate(board):
        for x, c in enumerate(line):
            if (y, x) in overlay:
                to_str.append(overlay[y,x])
            else:
                to_str.append(board[y,x])
            to_str.append(" ")
        to_str.append("\n")
    return "".join(to_str)


def get_dict_bounds(d):
    k = d.keys()
    return ((min(k, key=itemgetter(0))[0], min(k, key=itemgetter(1))[1]),
            (max(k, key=itemgetter(0))[0], max(k, key=itemgetter(1))[1]))


def render_array(bd):  # np.swapaxes(bd,0,1)
    as_str = np.array2string(bd, max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
                             formatter={'str_kind': lambda x: x})
    print('\x1b[1;1H\r', re.sub('[\[\]]', '', as_str), end='\n')


def dict_to_array(to_render):
    layer_bounds = get_dict_bounds(to_render)
    offset = (abs(min(layer_bounds[0][0], 0)), abs(min(layer_bounds[0][1], 0)))
    adjusted_bounds = layer_bounds[1][0] + offset[0] + 1, layer_bounds[1][1] + offset[1] + 1
    board = np.full((adjusted_bounds), fill_value=' ', dtype=str)
    for k, v in to_render.items():
        if not isinstance(k, tuple):
            continue
        board[k[0] + offset[0], k[1] + offset[1]] = v

    return board


#
# def prog_out_to_array(prog_output):
#     prog_ascii = [chr(c) for c in prog_output]
#     y = 0
#     x_off = 0
#     render = {}
#     for x, char in enumerate(prog_ascii):
#         if char == '\n':
#             y += 1
#             x_off = x+1
#         else:
#             render[x-x_off, y] = char
#     return dict_to_array(render)

# usage:
#  pass a dict where keys are (x,y) tuples to dict_to_array
#  the max bounds will be calculated, and then overlaid in a numpy 2d array


def get_neighbors(board, coord):
    neighbors = {}
    for direction in ro:
        x, y = np.add(coord, direction)
        if x < arr_bounds[0][0] or x >= arr_bounds[1][0] or y < arr_bounds[0][1] or y >= arr_bounds[1][1]:
            continue
        c = board[x, y]
        if c != '.' and c not in ascii_uppercase:
            continue
        neighbors[x, y] = c
    return neighbors


def get_nodes_at_tile(board, coord):
    nodes = []
    neighbors = get_neighbors(board, coord)
    for n_coords, n_c in neighbors.items():
        # print(n_coords)
        if n_coords in portals and isinstance(portal_coords := portals[n_coords], tuple):
            portal_coords = portal_coords
            nodes.append(portal_coords)
        else:
            nodes.append(n_coords)
    return nodes


def find_portals(board):
    portals = {}
    for x, line in enumerate(board):
        for y, c in enumerate(line):
            if c != '.':
                continue
            neighbors = get_neighbors(board, (x, y))
            for n_coords, n_c in neighbors.items():
                if n_c not in ascii_uppercase:
                    continue
                portal_neighbors = get_neighbors(board, n_coords)
                for n2_coords, n2_c in portal_neighbors.items():
                    if n2_c not in ascii_uppercase:
                        continue
                    portal_name = ''.join(sorted([n_c, n2_c]))
                    if portal_name not in portals:
                        portals[portal_name] = x,y
                        portals[n_coords] = portal_name
                    else:
                        end = portals[portal_name]
                        portals[n_coords] = end
                        portals[end] = n_coords
                        del portals[portal_name]
    return portals


def bfs(board, start, end):
    explored = []
    queue = [[start]]
    # print(queue)
    while queue:
        cur_path = queue.pop(0)

        node = cur_path[-1]
        if node == end:
            # print(f'end: {cur_path}')
            return cur_path

        if node not in explored:
            explored.append(node)
            # print(f'e {explored}')
            neighbors = get_nodes_at_tile(board, node)

            path_arr = {k: 'X' for k in cur_path}
            # render_array(dict_to_array(path_arr))
            # print(render(board, path_arr))
            # print(neighbors)
            # input()

            for neighbor in neighbors:
                new_path = cur_path.copy()
                new_path.append(neighbor)
                queue.append(new_path)


ascii_uppercase = set([c for c in string.ascii_uppercase])
ro = ((0, -1), (-1, 0), (1, 0), (0, 1))  # reading order
traversable = {'.', '@'}

f = 'd20e.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

parsed = np.array([[c for c in line.strip('\n')] for line in open(f).readlines()])
# print(parsed)
arr_bounds = ((0, 0), parsed.shape)

# render_array(parsed)
portals = find_portals(parsed)
# # print(portals)
# print()
# print(get_nodes_at_tile(parsed, (8,2)))
best = bfs(parsed, portals['AA'], portals['ZZ'])

path_arr = {k: 'X' for k in best}
# render_array(dict_to_array(path_arr))
print(f'p1: {len(best) - 1}')  #({best})')
