from aoc import *
import networkx as nx


def define_edges(G, grid, p2):
    slope_map = {
        (1, 0): '>',
        (0, -1): '^',
        (-1, 0): '<',
        (0, 1): 'v'
    }

    for node in G.nodes():
        parent = {node: None}
        q = deque([node])
        while q:
            # print(q)
            cur = q.pop()

            for dir in DIRS:
                n = vadd(dir, cur)
                if n in parent:
                    continue

                if n not in grid:
                    continue

                ntile = grid[n]
                if ntile == '#':
                    continue

                if n in G.nodes():
                    w = 1
                    while cur not in G.nodes():
                        w += 1
                        cur = parent[cur]
                    # print(cur, grid[cur], 'connects to', n, grid[n])
                    G.add_edge(cur, n, weight=w)
                elif ntile == '.' or (p2 or ntile in 'v>' and ntile == slope_map[dir]):
                    parent[n] = cur
                    q.append(n)


def find_intersections(grid, start, end, G):
    G.add_node(start)
    G.add_node(end)

    intersections = set()
    parent = {start: None}
    q = deque([start])
    while q:
        cur = q.pop()

        neighbors = []
        for dir in DIRS:
            n = vadd(dir, cur)
            if n in parent:
                continue

            if n not in grid:
                continue

            ntile = grid[n]
            if ntile == '#':
                continue

            parent[n] = cur
            neighbors.append(n)

        if len(neighbors) > 1:
            G.add_node(cur)
            intersections.add(cur)

        for n in neighbors:
            q.append(n)
    return G

def solve(p2):
    open = {k for k,v in grid.items() if v == '.'}
    start, end = min(open, key=itemgetter(1)), max(open, key=itemgetter(1))

    G = find_intersections(grid, start, end, nx.Graph() if p2 else nx.DiGraph())

    define_edges(G, grid, p2)

    if p2:
        longest = 0
        for path in nx.all_simple_paths(G, start, end):
            # print(path)
            l = nx.path_weight(G, path, 'weight')
            if l > longest:
                longest = l
                print(longest, end='...\r')
        return longest
    else:
        return nx.dag_longest_path_length(G)


setday(23)

grid, inverse, unique = parsegrid()

print('part1:', solve(False) )
print('part2:', solve(True) )

