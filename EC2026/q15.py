from ec import *

def p1():
    grid, inverse, unique = parse_grid(1)

    src = (unique['S'], 0, frozenset())
    tgt = (unique['E'], 0, frozenset(inverse['@']))

    def get_neighbors(pos):
        neighbors = []
        for d_i, d_v in enumerate(DIRS):
            if d_i == (pos[1]-2) % 4:
                continue
            n = vadd(pos[0], d_v)
            if n not in grid:
                continue
            if grid[n] == '#':
                continue
            elif grid[n] == '@':
                neighbors.append(((n, d_i, frozenset({*pos[2], n})), 1))
            elif grid[n] in '.E':
                neighbors.append(((n, d_i, pos[2]), 1))
        return neighbors

    path = wbfs(src, tgt, get_neighbors)
    return len(path) - 1


def p2():
    grid, inverse, unique = parse_grid(2)

    src = (unique['S'], 0, 0)
    tgt = (unique['E'], 0, 2026)

    def get_neighbors(pos):
        neighbors = []
        for d_i, d_v in enumerate(DIRS):
            if d_i == (pos[1]-2) % 4:
                continue
            n = vadd(pos[0], d_v)
            if n not in grid:
                continue
            if grid[n] == '#':
                continue
            elif grid[n] == '@':
                neighbors.append(((n, d_i, pos[2]+1), 1))
            elif grid[n] in '.E':
                neighbors.append(((n, d_i, pos[2]), 1))
        return neighbors

    path = wbfs(src, tgt, get_neighbors)
    if verbose:
        print_2d(' ', grid, {pos[0]:'~' for pos in path})
    return len(path) - 1
# surprisingly just a dumb bruteforce worked...and I only looked for exactly 2026, not "at least"


def p3():
    def wbfs(src, tgt, edges):
        """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
        a list of `(node, cost)` pairs."""
        q = [(0, src, None)]

        parent = {}

        best = INF

        while q:
            if len(q) % 250000 == 0:
                for thingy in q:
                    if thingy[1][2] == why:
                        from_end = tgt[0][0] - thingy[1][0][0]
                        adj = thingy[0] + from_end
                        if adj < best:
                            best = adj
                            print(best, thingy)

            cost, cur, prev = heapq.heappop(q)
            if cur in parent:
                continue
            parent[cur] = prev
            if cur == tgt:
                break

            for (n, ncost) in edges(cur):
                if n in parent:
                    continue
                heapq.heappush(q, (cost + ncost, n, cur))

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

    grid, inverse, unique = parse_grid(3)

    why = 202620262026

    src = unique['S']
    tgt = unique['E']

    simplified_grid = defaultdict(lambda: [list() for _ in range(4)])

    # fill in S -> E, single steps
    for x in range(src[0], tgt[0]):
        simplified_grid[(x, src[1])][2] = [((x+1, src[1]), 1, 0), ]
        # print(grid[(x, src[1])], grid[(x+1, src[1])])

    # then S <- E, single steps
    for x in range(tgt[0], src[0], -1):
        simplified_grid[(x, src[1])][0] = [((x-1, src[1]), 1, 0), ]

    print('simple grid with backbone:')
    print(simplified_grid)

    # now do loops
    for loop_type in [True, False]:
        for start_point in simplified_grid:
            for loop_start in [(start_point, 1), (start_point, 3)]:
                pos, dir = loop_start
                pos = vadd(pos, DIRS[dir])
                if grid[pos] == '#':
                    continue
                sec = 0
                sulphur = 0
                while (loop_type == True and pos not in simplified_grid) or (loop_type == False and pos != start_point):
                    sec += 1
                    if grid[pos] == '@':
                        sulphur += 1
                    next_pos = vadd(pos, DIRS[dir])
                    if grid[next_pos] == '#':
                        for d_i, d_v in enumerate(DIRS):
                            if d_i == (dir - 2) % 4:
                                continue
                            next_pos = vadd(pos, d_v)
                            if grid[next_pos] != '#':
                                pos = next_pos
                                dir = d_i
                                break
                    else:
                        pos = next_pos
                if loop_type:
                    print('half loop', loop_start, 'ended at', (pos, dir), 'after', sec, 'sec, with', sulphur, 'sulphur')
                else:
                    print('full loop', loop_start, 'ended at', (pos, dir), 'after', sec, 'sec, with', sulphur, 'sulphur')

                simplified_grid[start_point][dir].append((pos, sec, sulphur))

    print('full simple grid:')
    print(simplified_grid)

    def get_neighbors(state):
        # print('state:', state)
        pos, dir, sulphur = state
        neighbors = []
        for d_i, ns in enumerate(simplified_grid[pos]):
            if d_i == dir:
                continue
            # print('for', d_i, ns)
            for n in ns:
                # print(n)
                next_pos, next_sec, next_sulphur = n
                s_add = sulphur+next_sulphur
                if s_add <= why:
                    neighbors.append(((next_pos, (d_i-2)%4, sulphur+next_sulphur), next_sec))
                if next_pos == pos:
                    loops_until = (why-sulphur) // next_sulphur
                    s_add = sulphur+(next_sulphur*loops_until)
                    if s_add <= why:
                        neighbors.append(((next_pos, (d_i-2)%4, s_add), next_sec*loops_until))
        return neighbors

    # (pos, direction, sulphur)
    path = wbfs((src, 0, 0), (tgt, 0, why), get_neighbors)
    print(path)
    return


def p3():
    grid, inverse, unique = parse_grid(3)

    why = 202620262026

    src = unique['S']
    tgt = unique['E']

    simplified_grid = defaultdict(lambda: [list() for _ in range(4)])

    # fill in S -> E, single steps
    for x in range(src[0], tgt[0]):
        simplified_grid[(x, src[1])][2] = [((x+1, src[1]), 1, 0), ]
        # print(grid[(x, src[1])], grid[(x+1, src[1])])

    # then S <- E, single steps
    for x in range(tgt[0], src[0], -1):
        simplified_grid[(x, src[1])][0] = [((x-1, src[1]), 1, 0), ]

    print('simple grid with backbone:')
    print(simplified_grid)

    # now do loops
    for loop_type in [True, False]:
        for start_point in simplified_grid:
            for loop_start in [(start_point, 1), (start_point, 3)]:
                pos, dir = loop_start
                pos = vadd(pos, DIRS[dir])
                if grid[pos] == '#':
                    continue
                sec = 1
                sulphur = 0
                while (loop_type == True and pos not in simplified_grid) or (loop_type == False and pos != start_point):
                    sec += 1
                    if grid[pos] == '@':
                        sulphur += 1
                    next_pos = vadd(pos, DIRS[dir])
                    if grid[next_pos] == '#':
                        for d_i, d_v in enumerate(DIRS):
                            if d_i == (dir - 2) % 4:
                                continue
                            next_pos = vadd(pos, d_v)
                            if grid[next_pos] != '#':
                                pos = next_pos
                                dir = d_i
                                break
                    else:
                        pos = next_pos
                if loop_type:
                    print('half loop', loop_start, 'ended at', (pos, dir), 'after', sec, 'sec, with', sulphur, 'sulphur')
                else:
                    print('full loop', loop_start, 'ended at', (pos, dir), 'after', sec, 'sec, with', sulphur, 'sulphur')

                simplified_grid[start_point][dir].append((pos, sec, sulphur))

    print('full simple grid:')
    print(simplified_grid)

    def get_neighbors(state):
        # print('state:', state)
        pos, dir, sulphur = state
        neighbors = []
        for d_i, ns in enumerate(simplified_grid[pos]):
            if d_i == dir:
                continue
            # print('for', d_i, ns)
            for n in ns:
                # print(n)
                next_pos, next_sec, next_sulphur = n
                s_add = sulphur+next_sulphur
                if s_add <= why:
                    neighbors.append(((next_pos, (d_i-2)%4, sulphur+next_sulphur), next_sec))
                if next_pos == pos:
                    loops_until = (why-sulphur) // next_sulphur
                    s_add = sulphur+(next_sulphur*loops_until)
                    if s_add <= why:
                        neighbors.append(((next_pos, (d_i-2)%4, s_add), next_sec*loops_until))
        return neighbors

    def bfs(src, tgt, neighbors):
        q = deque([[0, src]])

        parent = {}

        while q:
            cur = q.popleft()
            if cur == tgt:
                break

            for n in neighbors(cur):
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

    def wbfs(src, tgt, edges):
        """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
        a list of `(node, cost)` pairs."""
        q = deque([[0, src]])

        parent = {}

        while q:
            # print(q)
            cost, cur = q.popleft()
            print(cost, cur)
            if cur == tgt:
                break

            for (n, ncost) in edges(cur):
                if n in parent:
                    continue
                parent[n] = cur
                # heapq.heappush(q, (cost + ncost, n, cur))
                q.append([cost + ncost, n])

        if tgt not in parent:
            return None

        return cost

    # (pos, direction, sulphur)
    path = wbfs((src, 0, 0), (tgt, 0, why), get_neighbors)
    print(path)
    return

# wait I have a better idea
def p3():
    grid, inverse, unique = parse_grid(3)

    why = 202620262026

    src = unique['S']
    tgt = unique['E']

    simplified_grid = defaultdict(lambda: [list() for _ in range(4)])

    # fill in S -> E, single steps
    for x in range(src[0], tgt[0]):
        simplified_grid[(x, src[1])][2] = [((x+1, src[1]), 1, 0), ]
        # print(grid[(x, src[1])], grid[(x+1, src[1])])

    # then S <- E, single steps
    for x in range(tgt[0], src[0], -1):
        simplified_grid[(x, src[1])][0] = [((x-1, src[1]), 1, 0), ]

    print('simple grid with backbone:')
    print(simplified_grid)

    loop_point_list = []

    # now do loops
    for start_point in simplified_grid:
        pos, dir = start_point, 1
        pos = vadd(pos, DIRS[dir])
        if grid[pos] == '#':
            continue
        sec = 1
        sulphur = 0
        while pos != start_point:
            sec += 1
            if grid[pos] == '@':
                sulphur += 1
            next_pos = vadd(pos, DIRS[dir])
            if grid[next_pos] == '#':
                for d_i, d_v in enumerate(DIRS):
                    if d_i == (dir - 2) % 4:
                        continue
                    next_pos = vadd(pos, d_v)
                    if grid[next_pos] != '#':
                        pos = next_pos
                        dir = d_i
                        break
            else:
                pos = next_pos
        print('full loop found at', start_point, 'is' , sec, 'sec, producing', sulphur, 'sulphur')
        loop_point_list.append((start_point, sec, sulphur))

    loop_point_list.sort(key=lambda x: x[2]/x[1], reverse=True)
    print('full simple grid:')
    print(loop_point_list)

    loop_points = {}
    for loop_point in loop_point_list:
        loop_points[loop_point[0]] = (loop_point[1], loop_point[2])

    print(loop_points)

    def get_neighbors(pos):
        neighbors = []
        for d_i, d_v in enumerate(DIRS):
            if d_i == (pos[1]-2) % 4:
                continue
            n = vadd(pos[0], d_v)
            if n not in grid:
                continue
            if grid[n] == '#':
                continue
            elif grid[n] == '@':
                if n == best_loop[0]:
                    neighbors.append(((n, d_i, pos[2]+1, True), 1))
                else:
                    neighbors.append(((n, d_i, pos[2]+1, pos[3]), 1))
            elif grid[n] in '.E':
                if n == best_loop[0]:
                    neighbors.append(((n, d_i, pos[2], True), 1))
                else:
                    neighbors.append(((n, d_i, pos[2], pos[3]), 1))
        return neighbors

    best_loop = loop_point_list[0]
    print('best_loop', best_loop)
    fudge_factor = (why-300) // best_loop[2]
    sulphur_fudge = fudge_factor * best_loop[2]
    time_fudge = fudge_factor * best_loop[1]
    print('fudge factor:', fudge_factor, 'sulphur_fudge', sulphur_fudge, 'time_fudge', time_fudge, 's_tgt', why - sulphur_fudge)

    # (pos, direction, sulphur)
    path = wbfs((src, 0, 0, False), (tgt, 0, why - sulphur_fudge, True), get_neighbors)
    print(path)

    return len(path) + time_fudge - 1


if __name__ == '__main__':
    setquest(15)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
