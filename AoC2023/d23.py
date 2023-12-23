from aoc import *
import networkx as nx


def bfs(src, tgt, neighbors):
    q = deque([src])

    parent = {}

    while q:
        cur = q.popleft()
        if cur == tgt:
            break

        for n in neighbors[cur]:
            if n in parent:
                continue
            parent[n] = cur
            q.append(n)

    if tgt not in parent:
        return None

    pos = tgt
    path = []
    while pos != src:
        path.append(pos)
        pos = parent[pos]
    path.append(src)
    path.reverse()
    return path


def p1():
    dmap = {
        (1, 0): '>',
        (0, -1): '^',
        (-1, 0): '<',
        (0, 1): 'v'
    }

    start, end = unique['S'], unique['E']
    G = nx.DiGraph()

    G.add_node(start)
    G.add_node(end)
    for c, tile in grid.items():
        if tile not in 'v>':
            continue
        G.add_node(c)

    def flood(start):
        q = [vadd(start, ((1,0) if grid[start] == '>' else (0,1)))]
        parent = {start: None, q[0]: start}
        ends = []
        while q:
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

                parent[n] = cur

                if ntile == '.':
                    q.append(n)

                if ntile == 'E' or ntile in 'v>' and ntile == dmap[dir]:
                    ends.append(n)

        weights = {}
        for c in ends:
            path = []
            cur = c
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            weights[c] = len(path)
        return weights

    print(flood(start))

    for node in G.nodes():
        if node == end:
            continue
        edges = flood(node)
        print(node, grid[node], edges)
        for edge, w in edges.items():
            G.add_edge(node, edge, weight=w)

    return nx.dag_longest_path_length(G)


def p2():
    start, end = unique['S'], unique['E']
    G = nx.Graph()
    G.add_node(start)
    G.add_node(end)

    p2_grid = {k:'.' if v in '>v' else v for k,v in grid.items()}

    def backtrack(start):
        w = 1
        prev = parent[start]
        while prev not in G.nodes():
            w += 1
            prev = parent[prev]

        G.add_edge(start, prev, weight=w)
        print('added edge from', start, p2_grid[cur], 'to', prev, p2_grid[prev], 'with weight', w)

    intersections = set()
    parent = {start: None}
    q = deque([start])
    while q:
        cur = q.pop()
        # print(p2_grid[cur])

        neighbors = []
        for dir in DIRS:
            n = vadd(dir, cur)
            if n in parent:
                continue

            if n not in p2_grid:
                continue

            ntile = p2_grid[n]
            if ntile == '#':
                continue

            parent[n] = cur
            neighbors.append(n)

        if len(neighbors) > 1:
            # print(cur, neighbors)
            G.add_node(cur)
            intersections.add(cur)

            # backtrack(cur)

        for n in neighbors:
            q.append(n)

    # backtrack(end)

    print_2d(' ', grid, {k:'+' for k in intersections})
    print_2d('         ', {k:f'+{k}' for k in intersections})

    for intersection in intersections:
        parent = {intersection: None}
        q = deque([intersection])
        while q:
            cur = q.pop()

            neighbors = []
            for dir in DIRS:
                n = vadd(dir, cur)
                if n in parent:
                    continue

                if n not in p2_grid:
                    continue

                ntile = p2_grid[n]
                if ntile == '#':
                    continue

                if n in intersections or ntile in 'SE':
                    w = 1
                    while cur not in intersections:
                        w += 1
                        cur = parent[cur]
                    print(cur, p2_grid[cur], 'connects to', n, p2_grid[n])
                    G.add_edge(cur, n, weight=w)
                    # do the stuff
                else:
                    parent[n] = cur
                    q.append(n)

        print(intersection)

    longest = 0
    for path in nx.all_simple_paths(G, start, end):
        # print(path)
        l = nx.path_weight(G, path, 'weight')
        if l > longest:
            longest = l
            print(longest)

    return longest


setday(23)

grid, inverse, unique = parsegrid()

print('part1:', p1() )
print('part2:', p2() )

