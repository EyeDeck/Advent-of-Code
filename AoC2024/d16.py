from aoc import *


def p1():
    def get_neighbors(node):
        pos, dir = node
        neighbors = [((pos, dir_prev[dir]), 1000), ((pos, dir_next[dir]), 1000)]
        forward_pos = vadd(pos, DIR_MAP[dir])
        if grid[forward_pos] != '#':
            neighbors.append(((forward_pos, dir), 1))
        return neighbors

    shortest_path = wbfs((unique['S'], '>'), (unique['E'], '>'), get_neighbors)

    while shortest_path[-1][0] == shortest_path[-2][0]:
        shortest_path.pop()

    print(shortest_path)
    acc = 0
    for i in range(len(shortest_path) - 1):
        move_a, move_b = shortest_path[i], shortest_path[i + 1]
        print(move_a, move_b)
        if move_a[1] != move_b[1]:
            acc += 1000
        else:
            acc += 1

    print_2d('.', grid, {k: v for k, v in shortest_path})
    return acc


def p2():
    def get_neighbors(node):
        pos, dir = node
        neighbors = [((pos, dir_prev[dir]), 1000), ((pos, dir_next[dir]), 1000)]
        forward_pos = vadd(pos, DIR_MAP[dir])
        if grid[forward_pos] != '#':
            neighbors.append(((forward_pos, dir), 1))
        return neighbors

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
        print('frontier', frontier)
        while frontier:
            new_frontier = set()
            for node in frontier:
                if node is None:
                    continue
                print('popped node', node)
                print('parent', parent[node])
                pos_heap.add(node[0])
                new_frontier.update({k for k in parent[node]})
            frontier = new_frontier
        print('heap:', pos_heap)
        return pos_heap

    shortest_paths = wbfs((unique['S'], '>'), (unique['E'], '>'), get_neighbors)

    print_2d('.', grid, {k: 'O' for k in shortest_paths})
    return len(shortest_paths)


setday(16)

# data = parselines()
# data = parselines(get_ints)
grid, inverse, unique = parsegrid()

# with open_default() as file:
#     data = get_ints(file.read())

verbose = '-v' in sys.argv or '--verbose' in sys.argv

DIR_MAP = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

dir_next = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
dir_prev = {'^': '<', '>': '^', 'v': '>', '<': 'v'}

print('part1:', p1())
print('part2:', p2())

# print('part1: %d\npart2: %d' % solve())
