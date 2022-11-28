import string
import sys
from collections import defaultdict, deque
import copy
import re
import sys
from collections import defaultdict
from operator import itemgetter

import numpy as np


# def render(board, overlay=None):
#     to_str = []
#     for y, line in enumerate(board):
#         for x, c in enumerate(line):
#             if (y, x) in overlay:
#                 to_str.append(overlay[y,x])
#             else:
#                 to_str.append(board[y,x])
#             to_str.append(" ")
#         to_str.append("\n")
#     return "".join(to_str)


def render(board, overlay=None):
    to_str = []
    overlay = {(n[0], n[1]):'~' for n in overlay}
    # print(overlay)
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


# def find_portals(board):
#     portals = {}
#     for x, line in enumerate(board):
#         for y, c in enumerate(line):
#             if c != '.':
#                 continue
#             neighbors = get_neighbors(board, (x, y))
#             for n_coords, n_c in neighbors.items():
#                 if n_c not in ascii_uppercase:
#                     continue
#                 portal_neighbors = get_neighbors(board, n_coords)
#                 for n2_coords, n2_c in portal_neighbors.items():
#                     if n2_c not in ascii_uppercase:
#                         continue
#                     portal_name = ''.join(sorted([n_c, n2_c]))
#                     if portal_name not in portals:
#                         portals[portal_name] = x,y
#                         # portals[n_coords] = portal_name
#                     else:
#                         end = portals[portal_name]
#                         portals[n_coords] = end
#                         portals[end] = (x,y)
#                         del portals[portal_name]
#     return portals

def find_portals(board):
    fboard = copy.deepcopy(board)
    portals_raw = defaultdict(list)
    for x, line in enumerate(fboard):
        for y, c in enumerate(line):
            if c in ascii_uppercase:
                fboard[x,y] = ' '
                adj = get_neighbors(fboard, (x,y))
                portal_coords = None
                name = c
                for coords, char in adj.items():
                    # print(char)
                    if char == '.':
                        portal_coords = coords
                    elif char in ascii_uppercase:
                        fboard[coords] = ' '
                        name += char
                        adj2 = get_neighbors(fboard, coords)
                        for coords2, char2 in adj2.items():
                            if char2 == '.':
                                portal_coords = coords2
                portals_raw[name].append(portal_coords)
                # print(portal_coords)
                # print(adj)
    portals_out = {}
    for label, portals in portals_raw.items():
        if len(portals) == 2:
            portals_out[portals[0]] = portals[1]
            portals_out[portals[1]] = portals[0]
        else:
            portals_out[label] = portals[0]
    # print(portals_out)
    return portals_out
   # print(portals_raw)



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
    # print(coord, coord in portals)

    if coord in portals and isinstance(portal_coords := portals[coord], tuple):
        nodes.append(portal_coords)

    for n_coords, n_c in neighbors.items():
        nodes.append(n_coords)
    return nodes


def bfs(board, start, end):
    explored = set()
    queue = deque([[start]])
    # print(queue)
    while queue:
        cur_path = queue.popleft()

        node = cur_path[-1]
        if node == end:
            # print(f'end: {cur_path}')
            return cur_path

        if node not in explored:
            explored.add(node)
            # print(f'e {explored}')
            neighbors = get_nodes_at_tile(board, node)

            # path_arr = {k: 'X' for k in cur_path}
            # render_array(dict_to_array(path_arr))
            # print(render(board, path_arr))
            # print(neighbors)
            # input()

            for neighbor in neighbors:
                new_path = cur_path[:]
                new_path.append(neighbor)
                queue.append(new_path)

# n_mem = {}
# def get_neighbors2(board, coord):
#     if coord in n_mem:
#         return n_mem[coord]
#     else:
#         ans = get_neighbors2_int(board, coord)
#         n_mem[coord] = ans
#         return ans

def get_neighbors2(board, coord):
    neighbors = {}
    for direction in ro:
        x, y = coord[0] + direction[0], coord[1] + direction[1]
        #x, y = np.add(coord[:2], direction)
        # if x < arr_bounds[0][0] or x >= arr_bounds[1][0] or y < arr_bounds[0][1] or y >= arr_bounds[1][1]:
        #     continue
        c = board[x, y]
        if c != '.': #and c not in ascii_uppercase:
            continue
        neighbors[x, y] = c
    # print(neighbors)
    return neighbors


# def get_nodes_at_tile2(board, coord):
#     nodes = []
#     neighbors = get_neighbors2(board, coord)
#     for n_coords, n_c in neighbors.items():
#         # print(f'testing {n_coords} in {portals}')
#         x_y = n_coords[0], n_coords[1]
#         if x_y in portals and isinstance(portal_coords := portals[x_y], tuple):
#             # print(portal_coords)
#             portal_coords = portal_coords[0], portal_coords[1], n_coords[2] + portal_coords[2]
#             # print(portal_coords, portal_coords[2], portal_coords[2] < 0)
#             if portal_coords[2] < 0 or portal_coords[2] > max_depth:
#                 continue
#             nodes.append(portal_coords)
#         else:
#             nodes.append(n_coords)
#     # input(f'neighbors for node {coord} are {nodes}')
#
#     return nodes


# def get_nodes_at_tile2(board, coord):
#     nodes = []
#     x_y = coord[0], coord[1]
#     print(coord)
#     if x_y in portals and isinstance(portal_coords := portals[x_y], tuple):
#         portal_coords = portal_coords[0], portal_coords[1], coord[2] + portal_coords[2]
#         if portal_coords[2] < 0 or portal_coords[2] > max_depth:
#             return nodes
#         nodes.append(portal_coords)
#     else:
#         neighbors = get_neighbors2(board, coord)
#         for n_coords, n_c in neighbors.items():
#             nodes.append(n_coords)
#     # for n_coords, n_c in neighbors.items():
#     return nodes


def get_nodes_at_tile2(board, coord):
    nodes = []

    depth = coord[2]
    coord = coord[0], coord[1]


    # print(coord, coord in portals)
    # print([board[c[0], c[1]] for c in neighbors.keys()])

    if coord in portals:  # and isinstance(portal_coords := portals[coord], tuple):
        portal_coords = portals[coord]
        new_coord = (portal_coords[0], portal_coords[1], depth + portal_coords[2])
        if 0 <= new_coord[2] < max_depth:
            nodes.append(new_coord)
            # return nodes
    neighbors = get_neighbors2(board, coord)
    for n_coords, n_c in neighbors.items():
        nodes.append((n_coords[0], n_coords[1], depth))
    return nodes


def bfs2(board, start, end):
    explored = set()
    # steps = 0
    queue = deque([[start]])
    # print(queue)
    while queue:
        cur_path = queue.popleft()

        node = cur_path[-1]
        if node == end:
            # print(f'end: {cur_path}')
            # print(steps)
            return cur_path

        if node not in explored:
            explored.add(node)
            # print(f'e {explored}')
            neighbors = get_nodes_at_tile2(board, node)

            #print(f'neighbors {neighbors}')
            #

            # path_arr = {k: 'X' for k in cur_path}
            # input(render(board, path_arr))

            for neighbor in neighbors:
                # steps += 1
                new_path = cur_path[:]
                new_path.append(neighbor)
                queue.append(new_path)


# def bfs2(board, start, end):
#     explored = []
#     queue = [start]
#     # print(queue)
#     while queue:
#         node = queue.pop(0)
#
#         if node == end:
#             # print(f'end: {cur_path}')
#             return 1
#
#         if node not in explored:
#             explored.append(node)
#             # print(f'e {explored}')
#             neighbors = get_nodes_at_tile2(board, node)
#
#             # print(f'neighbors {neighbors}')
#             #
#
#             # path_arr = {node:'X'}
#             # input(render(board, path_arr))
#
#             for neighbor in neighbors:
#                 # new_path = cur_path.copy()
#                 # new_path.append(neighbor)
#                 queue.append(neighbor)


def get_outer_layer(board):
    bounds = None
    for x, line in enumerate(board):
        for y, c in enumerate(line):
            if c == '#':
                bounds = [x, y, 0, 0]
                s_x, s_y = x, y
                while True:
                    s_x += 1
                    # print(board[s_x, y])
                    if board[s_x, y] == ' ':
                        bounds[2] = s_x - 1
                        break
                while True:
                    s_y += 1
                    if board[x, s_y] == ' ':
                        bounds[3] = s_y - 1
                        break
                # outer_layer = set()
                # for x2 in range(bounds[0]-1, bounds[2] + 2):
                #     outer_layer.add((x2, bounds[1]-1))
                #     outer_layer.add((x2, bounds[3]+1))
                # for y2 in range(bounds[1]-1, bounds[3] + 2):
                #     outer_layer.add((bounds[0]-1, y2))
                #     outer_layer.add((bounds[2]+1, y2))
                outer_layer = set()
                for x2 in range(bounds[0], bounds[2] + 1):
                    outer_layer.add((x2, bounds[1]))
                    outer_layer.add((x2, bounds[3]))
                for y2 in range(bounds[1], bounds[3] + 1):
                    outer_layer.add((bounds[0], y2))
                    outer_layer.add((bounds[2], y2))

                path_arr = {k: 'X' for k in outer_layer}
                # render_array(dict_to_array(path_arr))
                return outer_layer


def add_portal_levels(board, portals):
    outer_layer = get_outer_layer(board)
    # print(outer_layer)
    new_portals = {}
    for in_, out_ in portals.items():
        depth = 0
        if not isinstance(in_, tuple):
            pass
        elif in_ in outer_layer:
            depth = -1
        else:
            depth = 1
        new_portals[in_] = out_[0], out_[1], depth
    return new_portals
    # print(new_portals)


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
# print(portals)

portals_text = {k:'@' for k in portals}
# print(render(parsed, portals_text))
# sys.exit()
# print()
# print(get_nodes_at_tile(parsed, (8,2)))

p1 = bfs(parsed, portals['AA'], portals['ZZ'])

path_arr = {k: 'X' for k in p1}
# print(render(parsed, p1))
print(f'p1: {len(p1) - 1}')  #({best})')

portals = add_portal_levels(parsed, portals)
max_depth = len(portals) // 2 - 2
# print(portals)
# portals_text = {k:'@' for k in portals}
# print(render(parsed, portals_text))

# sys.exit()

# import cProfile
# cProfile.run('bfs2(parsed, portals["AA"], portals["ZZ"])')
p2 = bfs2(parsed, portals['AA'], portals['ZZ'])

# path_arr = {k: 'X' for k in p2}
# render_array(dict_to_array(path_arr))
# print(render(parsed, path_arr))
print(f'p2: {len(p2) - 1}')
# print(p2)
