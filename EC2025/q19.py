from ec import *





def p1():
    data = parse_lines(1, get_ints)
    board = set()
    x = 0
    max_height = 0
    for line in data:
        max_height = max(max_height, line[1] + line[2] + 1)

    for line in data:
        ahead, low, opening = line
        x = ahead
        for y in range(0, -(low), -1):
            board.add((x, y))
        for y in range(-(low + opening), -max_height, -1):
            board.add((x, y))

    print_2d('.', {k: '#' for k in board}, {(0, 0): 'S'})

    def wbfs(src, tgt, edges):
        """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
        a list of `(node, cost)` pairs."""
        q = [(0, src, None)]

        parent = {}

        cost = -1
        while q:
            cost, cur, prev = heapq.heappop(q)
            if cur in parent:
                continue
            parent[cur] = prev
            c_x, c_y = cur
            if c_x == tgt:
                break

            for (n, ncost) in edges(cur):
                if n in parent:
                    continue
                heapq.heappush(q, (cost + ncost, n, cur))

        return cost


    def get_neighbors(pos):
        n = []
        up = vadd((1, -1), pos)
        down = vadd((1, 1), pos)
        if up not in board and up[1] <= 0 and up[1] >= -max_height:
            n.append((up, 1))
        if down not in board and down[1] <= 0 and down[1] >= -max_height:
            n.append((down, 0))
        print(pos, n)
        return n

    cost = wbfs((0, 0), x, get_neighbors)

    return cost


def p2():
    data = parse_lines(2, get_ints)
    board = defaultdict(set)
    start = (0, 0)

    for line in data:
        ahead, low, opening = line
        x = ahead
        for y in range(-(low), -(low + opening), -1):
            board[x].add(y)

    printable = set()
    for x, ys in board.items():
        for y in ys:
            printable.add((x,y))

    print_2d('.', {k: '#' for k in printable}, {(0, 0): 'S'})

    def wbfs(q, tgt, edges, x_limit):
        # modified from library version to return cost, so I don't have to recalc it

        src = {t[1] for t in q}
        parent = {}

        while q:
            cost, cur, prev = heapq.heappop(q)
            if cur in parent:
                continue
            parent[cur] = (prev, cost)
            if cur in tgt:
                if all(n in parent for n in tgt):
                    break

            c_x, c_y = cur
            if c_x > x_limit:
                continue

            for (n, ncost) in edges(cur):
                if n in parent:
                    continue
                heapq.heappush(q, (cost + ncost, n, cur))

        if not any(n in parent for n in tgt):
            return None

        paths = {}
        for start in tgt:
            pos = start
            if pos not in parent:
                continue
            path = []
            while pos not in src:
                path.append(pos)
                pos, _ = parent[pos]
            path.append(pos)
            path.append(parent[start][1])
            path.reverse()
            paths[start] = path
        return paths

    def get_neighbors(pos):
        return [(vadd((1, -1), pos), 1), (vadd((1, 1), pos), 0)]

    in_state = [(0, start, None)]
    for x, targets in board.items():
        target_coords = {(x,y) for y in targets}
        print(x, targets)
        out_state = wbfs(in_state, target_coords, get_neighbors, x)
        print(out_state)
        in_state = [(v[0], k, None) for k,v in out_state.items()]
        print('is', in_state)

    return min(in_state, key=lambda x:x[0])[0]


def p3():
    data = parse_lines(3, get_ints)
    board = defaultdict(set)
    start = (0, 0)

    for line in data:
        ahead, low, opening = line
        x = ahead
        for y in range(low, low + opening):
            board[x].add(y)

    printable = set()
    for x, ys in board.items():
        for y in ys:
            printable.add((x,y))

    print_2d('.', {k: '#' for k in printable}, {(0, 0): 'S'})

    cur = [(0, start)]
    for x, targets in board.items():
        target_coords = {(x,y) for y in targets}
        print(target_coords)
        # die()

    cur = 0
    next_column = {}
    for x in board:
        next_column[cur] = x
        cur = x
    print(next_column)


    def get_neighbors(pos):
        n = []

        in_x, in_y = pos
        nc = next_column[in_x]
        dist = nc - in_x
        odd = nc & 1
        # print(f'dist {in_x} to {nc} = {dist}, odd {odd}')

        for y in board[nc]:
            # print('\t', y, abs(y - in_y), (abs(y - in_y) <= dist))
            if not ((y & 1) if odd else (y & 1 == 0)):
                continue
            if not (abs(y - in_y) <= dist):
                continue
            cost = (dist - (in_y - y)) // 2
            # print(f'dist from {pos} to {(nc, y)} = {dist} and reachable = {reachable} and cost = {cost}')
            # print(f'\tdist from {pos} to {(nc, y)} = {dist} and cost = {cost}')
            n.append(((nc, y), cost))
        return n

    # (0,0) to (7,7) = 7
    # (0,0) to (7,7) = 7

    # print(get_neighbors(start))

    def wbfs(q, tgt, edges, x_limit):
        # modified from library version to return cost, so I don't have to recalc it

        src = {t[1] for t in q}
        parent = {}

        while q:
            cost, cur, prev = heapq.heappop(q)
            if cur in parent:
                continue
            parent[cur] = (prev, cost)
            if cur in tgt:
                if all(n in parent for n in tgt):
                    break

            c_x, c_y = cur
            if c_x >= x_limit:
                continue

            for (n, ncost) in edges(cur):
                if n in parent:
                    continue
                heapq.heappush(q, (cost + ncost, n, cur))

        if not any(n in parent for n in tgt):
            return None

        paths = {}
        for start in tgt:
            pos = start
            if pos not in parent:
                continue
            path = []
            while pos not in src:
                path.append(pos)
                pos, _ = parent[pos]
            path.append(pos)
            path.append(parent[start][1])
            path.reverse()
            paths[start] = path
        return paths

    in_state = [(0, start, None)]
    for x, targets in board.items():
        print(x)

        target_coords = {(x,y) for y in targets}
        # print(x, targets)
        out_state = wbfs(in_state, target_coords, get_neighbors, x)
        # print(out_state)
        in_state = [(v[0], k, None) for k,v in out_state.items()]
        # print('is', in_state)

    return min(in_state, key=lambda x:x[0])[0]


setquest(19)

# print('part1:', p1())
# print('part2:', p2())
print('part3:', p3())
