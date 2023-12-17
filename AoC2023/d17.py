from aoc import *

def get_neighbors(coord, heading, moves_left, part2):
    neighbors = []
    for next_heading, dir in enumerate(DIRS):

        next_moves = moves_left - 1 if heading == next_heading else (10 if part2 else 3)

        if next_moves == 0 \
        or part2 and moves_left > 7 and next_heading != heading \
        or heading == (next_heading + 2) % 4: # no backsies
            continue

        next_coord = vadd(coord, dir)
        if next_coord not in grid:
            continue

        neighbors.append(((next_coord, next_heading, next_moves), grid[next_coord]))

    return neighbors


def wbfs(src, tgt, part2):
    q = [(0, (src, -1, 0), None)]

    parent = {}

    while q:
        cost, state, prev = heapq.heappop(q)
        (cur, heading, moves_left) = state

        if state in parent:
            continue
        parent[state] = prev
        if cur == tgt and (not part2 or moves_left < 8): # why 8? I don't know! I trial-and-errored
            tgt = (cur, heading, moves_left)
            break

        # pos = state
        # path = []
        # while pos[0] != src:
        #     path.append(pos)
        #     pos = parent[pos]
        # print_2d('  ', grid, {k[0]: str(grid[k[0]]) + DIR_s[k[1]] for k in path})

        for (n, ncost) in get_neighbors(*state, part2):
            if n in parent:
                continue
            heapq.heappush(q, (cost + ncost, n, state))

    if tgt not in parent:
        return None

    pos = tgt
    path = []
    while pos[0] != src:
        path.append(pos)
        pos = parent[pos]
    path.reverse()

    return path


def solve(part2):
    bounds = grid_bounds(grid)
    path = wbfs((0,0), (bounds[2], bounds[3]), part2)
    if verbose:
        print_2d('  ', grid, {k[0]: str(grid[k[0]]) + DIR_s[k[1]] for k in path})
    return sum(grid[c[0]] for c in path)


setday(17)

grid, inverse, unique = parsegrid()
grid = {k:int(v) for k,v in grid.items()}

verbose = '-v' in sys.argv or '--verbose' in sys.argv
DIR_s = ['>', '^', '<', 'v']

print('part1:', solve(False) )
print('part2:', solve(True) )
