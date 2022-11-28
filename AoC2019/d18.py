import re
import sys
import string
from collections import defaultdict, deque
import heapq as hq

import numpy as np


def render_array(bd):
    as_str = np.array2string(np.swapaxes(bd, 0, 1), max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
                             formatter={'str_kind': lambda x: x})
    print('\x1b[1;1H\r', re.sub('[\[\]]', '', as_str), end='\n')


def get_nodes_at_tile(board, coord, keys):
    nodes = []
    chars = []
    for dir in ro:
        x, y = np.add(coord, dir)
        if x < arr_bounds[0][0] or x >= arr_bounds[1][0] or y < arr_bounds[0][1] or y >= arr_bounds[1][1]:
            continue
        neighbor = board[x, y]
        # print(neighbor, keys, neighbor.swapcase(), keys)
        if neighbor in traversable or neighbor.islower() or neighbor.swapcase() in keys:
            # print('accepted', neighbor)
            nodes.append((x, y))
            chars.append(neighbor)
    return nodes, chars


def get_path_to_other_keys(board, key, key_ct):
    explored = set()
    found_keys = {}

    queue = deque([[key]])

    while queue and len(found_keys) < key_ct:
        cur_path = queue.popleft()
        cur_coords = cur_path[-1]
        if cur_coords not in explored:
            explored.add(cur_coords)

            # print(cur_path)
            cur_char = board[cur_coords]
            if cur_char in ascii_lowercase:
                required_keys = set()
                for coord in cur_path[:-1]:
                    inner_char = board[coord]
                    if inner_char in ascii_lowercase:
                        required_keys.add(inner_char)
                    if inner_char in ascii_uppercase:
                        required_keys.add(inner_char.lower())
                    # if key in required_keys:
                    #     required_keys.remove(key)
                    # for k in found_keys.keys():
                    #     required_keys.add(k)

                found_keys[cur_char] = (len(cur_path) - 1, required_keys)

            nodes, chars = get_nodes_at_tile(board, cur_coords, ascii_lowercase)

            # add neighbours of node to queue
            for node in nodes:
                new_path = cur_path.copy()
                new_path.append(node)
                queue.append(new_path)
    return found_keys


best_depths = {}


def get_best_depth(length, state, next_node):
    state = frozenset(state)
    if next_node not in best_depths:
        best_depths[next_node] = {}
    if state not in best_depths[next_node]:
        best_depths[next_node][state] = length
    ret = min(best_depths[next_node][state], length)
    best_depths[next_node][state] = ret
    return ret


def bfs(graph, key, key_ct):
    potential = []
    queue = [(0, [key], set())]

    while queue:
        cur_data = hq.heappop(queue)
        cur_cost = cur_data[0]
        cur_path = cur_data[1]
        cur_keys = cur_data[2]
        cur_head = cur_path[-1]
        # print(f'data {cur_data}, path {cur_path}, head {cur_head}')

        if len(cur_keys) == key_ct:
            # recalculate end cost (so I can experiment with fiddling with queue priorities and make this A*)
            end_cost = 0
            for i in range(0, len(cur_path) - 1):
                end_cost += graph[cur_path[i]][cur_path[i + 1]][0]  # [i+1][0]
            return end_cost, cur_path

        # if cur_head in explored:
        #     continue
        # explored.add(cur_head)
        neighbors = []
        for p_neighbor, p_reqs in graph[cur_head].items():
            if p_neighbor not in cur_path and p_reqs[1].issubset(cur_keys):
                neighbors.append(p_neighbor)

        for node in neighbors:
            new_path = cur_path.copy()
            new_path.append(node)
            new_keys = cur_keys.copy()
            new_keys.add(node)
            new_cost = heuristic(cur_cost, graph[cur_head][node][0], new_path)

        # if len(cur_keys) > 1:
            best_for_key_list = get_best_depth(new_cost, new_keys, node)
            # print(f'new path{new_path}\n\tnew keys {new_keys}\n\tnew_cost {new_cost}, best_cost {best_for_key_list}')
            if new_cost != best_for_key_list:
                continue

            to_push = (new_cost, new_path, new_keys)
            hq.heappush(queue, to_push)

    print(f'potentials: {potential}')
    return potential


# unused
def heuristic(total_cost, next_cost, path):
    return total_cost + next_cost


ascii_lowercase = set([c for c in string.ascii_lowercase])
ascii_uppercase = set([c for c in string.ascii_uppercase])
ro = ((0, -1), (-1, 0), (1, 0), (0, 1))  # reading order
traversable = {'.', '@'}

f = 'd18.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

parsed = np.array([[z for z in x.strip()] for x in open(f).readlines()])
arr_bounds = ((0, 0), parsed.shape)
print(arr_bounds)

start = np.where(parsed == '@')
start = (start[0][0], start[1][0])

keys = {}
for y, line in enumerate(parsed):
    for x, c in enumerate(line):
        if c in ascii_lowercase:
            keys[c] = y, x
# print(keys)

# print(bfs(parsed, start, key_ct))
traversal_requirements = {'@': get_path_to_other_keys(parsed, start, len(keys))}
print(traversal_requirements)
# sys.exit()
for key in keys:
    traversal_requirements[key] = get_path_to_other_keys(parsed, keys[key], len(keys))
print(traversal_requirements, '\n')

print(bfs(traversal_requirements, '@', len(keys)))
#
#
# to_insert = np.array([['1','#','2'],['#','#','#'],['3','#','4']])
# parsed[40,40] = '1'
# parsed[41,40] = '#'
# parsed[42,40] =
# parsed[40,40] = 1
# parsed[40,40] = 1
