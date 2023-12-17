from aoc import *

DIRS = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

DIR_s = ['>', '^', '<', 'v']


# def get_neighbors(last_n):
#     c = last_n[0]
#     straight = (-1, -1)
#     print('last_n', last_n)
#     if len(last_n) > 3:
#         if len(set(c[0] for c in last_n)) == 1:
#             straight = (last_n[0][0], -1)
#             print('straight horizontal')
#         elif len(set(c[1] for c in last_n)) == 1:
#             straight = (-1, last_n[0][1])
#             print('straight vertical')
#     print('straight?', straight)
#
#     neighbors = []
#     for dir in DIRS:
#         # print(dir, c)
#         n = vadd(c, dir)
#         if n not in grid:
#             continue
#         if n[0] == straight[0] or n[1] == straight[1]:
#             continue
#         neighbors.append((n, grid[n]))
#     print('neighbors', neighbors)
#     return neighbors




def p1():
    def wbfs(src, tgt, edges):
        """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
        a list of `(node, cost)` pairs."""
        q = [(0, (src, -1, 0), None)]

        parent = {}

        while q:
            # print(parent)

            cost, state, prev = heapq.heappop(q)
            (cur, heading, moves_left) = state
            # print(cost, state, prev)

            if state in parent:
                continue
            parent[state] = prev
            if cur == tgt:
                # print('at cur', cur)
                tgt = (cur, heading, moves_left)
                break

            pos = state
            # print('pos1', pos)
            path = []
            # path_coords = set()
            while pos[0] != src:
                path.append(pos)
                # path_coords.add(pos[0])
                pos = parent[pos]
                # print('pos2', pos, parent)

            # print_2d('  ', grid, {k[0]: str(grid[k[0]]) + DIR_s[k[1]] for k in path})
            # input()

            # last_n = [cur]
            # print('cur', cur, last_n)
            # for i in range(3):
            #     if last_n[-1] not in parent:
            #         break
            #     if parent[last_n[-1]] is None:
            #         break
            #     last_n.append(parent[last_n[-1]])
            # print('last_n', last_n)

            for (n, ncost) in edges(*state):
                # print('n', n)
                if n in parent:
                    continue
                # if n[0] in path_coords:
                #     continue
                heapq.heappush(q, (cost + ncost, n, state))

        if tgt not in parent:
            return None

        pos = tgt
        path = []
        while pos[0] != src:
            # print(path)
            path.append(pos)
            pos = parent[pos]
        # path.append(src)
        path.reverse()
        path = [c[0] for c in path]
        return path

    def get_neighbors(coord, heading, moves_left):
        neighbors = []
        for next_heading, dir in enumerate(DIRS):
            next_moves = moves_left - 1 if heading == next_heading else 3
            if next_moves == 0:
                continue

            if heading == (next_heading + 2) % 4:  # no backsies
                continue

            next_coord = vadd(coord, dir)
            if next_coord not in grid:
                continue

            neighbors.append(((next_coord, next_heading, next_moves), grid[next_coord]))
        # print(coord, heading, moves_left, 'neighbors', neighbors)
        return neighbors
    # print(grid)

    bounds = grid_bounds(grid)

    path = wbfs((0,0), (bounds[2], bounds[3]), get_neighbors)
    # path.pop(0)
    # print([grid[c] for c in path])
    print_2d('  ', grid, {k:str(grid[k]) + '#' for k in path})

    return sum(grid[c] for c in path)
# not 905


def p2():
    def wbfs(src, tgt, edges):
        """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
        a list of `(node, cost)` pairs."""
        q = [(0, (src, -1, 0), None)]

        parent = {}

        while q:
            # print(parent)

            cost, state, prev = heapq.heappop(q)
            (cur, heading, moves_left) = state
            # print(cost, state, prev)

            if state in parent:
                continue
            parent[state] = prev
            if cur == tgt and moves_left < 8: # why 8? I don't know! I trial-and-errored
                # print('at cur', cur)
                tgt = (cur, heading, moves_left)
                break

            pos = state
            # print('pos1', pos)
            path = []
            # path_coords = set()
            while pos[0] != src:
                path.append(pos)
                # path_coords.add(pos[0])
                pos = parent[pos]
                # print('pos2', pos, parent)

            # print_2d('  ', grid, {k[0]: str(grid[k[0]]) + DIR_s[k[1]] for k in path})
            # input()

            # last_n = [cur]
            # print('cur', cur, last_n)
            # for i in range(3):
            #     if last_n[-1] not in parent:
            #         break
            #     if parent[last_n[-1]] is None:
            #         break
            #     last_n.append(parent[last_n[-1]])
            # print('last_n', last_n)

            for (n, ncost) in edges(*state):
                # print('n', n)
                if n in parent:
                    continue
                # if n[0] in path_coords:
                #     continue
                heapq.heappush(q, (cost + ncost, n, state))

        if tgt not in parent:
            return None

        pos = tgt
        path = []
        while pos[0] != src:
            # print(path)
            path.append(pos)
            pos = parent[pos]
        # path.append(src)
        path.reverse()
        path = [c[0] for c in path]
        return path

    def get_neighbors(coord, heading, moves_left):
        neighbors = []
        for next_heading, dir in enumerate(DIRS):

            next_moves = moves_left - 1 if heading == next_heading else 10
            if next_moves == 0:
                continue

            if moves_left > 7:
                if next_heading != heading:
                    continue

            if heading == (next_heading + 2) % 4:  # no backsies
                continue

            next_coord = vadd(coord, dir)
            if next_coord not in grid:
                continue

            neighbors.append(((next_coord, next_heading, next_moves), grid[next_coord]))
        # print(coord, heading, moves_left, 'neighbors', neighbors)
        return neighbors
    # print(grid)

    bounds = grid_bounds(grid)

    path = wbfs((0,0), (bounds[2], bounds[3]), get_neighbors)
    # path.pop(0)
    # print([grid[c] for c in path])
    print_2d('  ', grid, {k:str(grid[k]) + '#' for k in path})

    return sum(grid[c] for c in path)


setday(17)

# data = parselines()
# data = parselines(get_ints)
grid, inverse, unique = parsegrid()
grid = {k:int(v) for k,v in grid.items()}

# print('part1:', p1() )
print('part2:', p2() )
