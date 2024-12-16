from aoc import *


def get_neighbors(node):
    pos, dir = node
    neighbors = [((pos, DIR_PREV[dir]), 1000), ((pos, DIR_NEXT[dir]), 1000)]
    forward_pos = vadd(pos, DIR_MAP[dir])
    if grid[forward_pos] != '#':
        neighbors.append(((forward_pos, dir), 1))
    return neighbors


def p1():
    shortest_path = wbfs((unique['S'], '>'), (unique['E'], '>'), get_neighbors)

    while shortest_path[-1][0] == shortest_path[-2][0]:
        shortest_path.pop()

    acc = 0
    for i in range(len(shortest_path) - 1):
        move_a, move_b = shortest_path[i], shortest_path[i + 1]
        if move_a[1] != move_b[1]:
            acc += 1000
        else:
            acc += 1

    if verbose:
        print_2d('.', grid, {k: v for k, v in shortest_path})
    return acc


def p2():
    def wbfs(src, tgt, edges):
        q = [(0, src)]
        min_costs = defaultdict(lambda: INF, {src: 0})
        parent = defaultdict(list)

        while q:
            cost, cur = heapq.heappop(q)

            if cost > min_costs[cur]:
                continue

            for neighbor, n_cost in edges(cur):
                new_cost = cost + n_cost
                if new_cost < min_costs[neighbor]:
                    min_costs[neighbor] = new_cost
                    heapq.heappush(q, (new_cost, neighbor))
                    parent[neighbor] = [cur]
                elif new_cost == min_costs[neighbor]:
                    parent[neighbor].append(cur)

        if tgt not in min_costs or min_costs[tgt] == INF:
            return None

        pos_heap = set()
        frontier = {k for k in parent[tgt]}
        while frontier:
            new_frontier = set()
            for node in frontier:
                if node is None:
                    continue
                pos_heap.add(node[0])
                new_frontier.update({k for k in parent[node]})
            frontier = new_frontier
        return pos_heap

    shortest_paths = wbfs((unique['S'], '>'), (unique['E'], '>'), get_neighbors)

    if verbose:
        print_2d('.', grid, {k: 'O' for k in shortest_paths})
    return len(shortest_paths)


setday(16)

grid, inverse, unique = parsegrid()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

DIR_MAP = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
DIR_NEXT = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
DIR_PREV = {'^': '<', '>': '^', 'v': '>', '<': 'v'}

print('part1:', p1())
print('part2:', p2())
