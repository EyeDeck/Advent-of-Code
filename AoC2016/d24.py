from aoc import *


def solve(p2):
    neighbors = {}
    for coord, tile in grid.items():
        if tile == '#':
            continue
        neighbors[coord] = [c for c in [vadd(d, coord) for d in DIRS] if grid[c] != '#']

    # print(neighbors)
    pois = {int(n):inverse[n][0] for n in inverse.keys() if n.isnumeric()}
    # print(pois)

    def r_path(unvisited, path):
        if not unvisited and (not p2 or path[-1] == 0):
            acc = 0
            for i in range(len(path)-1):
                a,b = path[i], path[i+1]
                acc += costs[a][b]
            return acc
        lowest = INF
        for n in unvisited:
            lowest = min(r_path(unvisited - {n}, path + [n]), lowest)
        return lowest

    costs = defaultdict(dict)
    for a, a_c in pois.items():
        for b, b_c in pois.items():
            if a == b:
                continue
            r = bfs(a_c, b_c, neighbors)
            # print(a,b)
            costs[a][b] = len(r)-1
    # print(costs)

    return r_path(set(pois) - (set() if p2 else {0}), [0])


setday(24)

grid, inverse, unique = parsegrid()

print('part1:', solve(False) )
print('part2:', solve(True) )
