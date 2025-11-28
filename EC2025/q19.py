from ec import *


def wbfs(src, tgt, edges):
    """Find a path from `src` to `tgt`.  `edges` takes a node label and returns
            a list of `(node, cost)` pairs.
    modified from library version to return cost, so I don't have to recalc it
    """
    q = [(0, src, None)]

    parent = {}

    while q:
        cost, cur, prev = heapq.heappop(q)
        if cur in parent:
            continue
        parent[cur] = (prev, cost)
        if cur in tgt:
            return cost

        for (n, ncost) in edges(cur):
            if n in parent:
                continue
            heapq.heappush(q, (cost + ncost, n, cur))

    return None


def solve(n):
    data = parse_lines(n, get_ints)
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

    # print_2d('.', {k: '#' for k in printable}, {(0, 0): 'S'})

    cur = 0
    next_column = {}
    for x in board:
        next_column[cur] = x
        cur = x

    def get_neighbors(pos):
        n = []

        in_x, in_y = pos
        nc = next_column[in_x]
        dist = nc - in_x
        odd = nc & 1
        for y in board[nc]:
            if not ((y & 1) if odd else (y & 1 == 0)):
                continue
            if not (abs(y - in_y) <= dist):
                continue
            cost = (dist - (in_y - y)) // 2
            n.append(((nc, y), cost))
        return n

    target_coords = {(x,y) for y in board[max(board.keys())]}
    return wbfs(start, target_coords, get_neighbors)


setquest(19)

print('part1:', solve(1))
print('part2:', solve(2))
print('part3:', solve(3))
