from aoc import *


def bfs(src, tgt, neighbors):
    q = deque([src])

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

@memo
def get_neighbors(c):
    x, y = c
    adjacent = []
    for xm, ym in DIRS:
        adj = (x+xm, y+ym)
        if adj not in board:
            continue
        if ord(board[c]) + 1 >= ord(board[adj]):
            adjacent.append(adj)

    return adjacent


def p1():
    return len(bfs(src, dest, get_neighbors)) - 1


def p2():
    src = [k for k, v in board.items() if v == 'a']
    paths = [bfs(s, dest, get_neighbors) for s in src ]
    paths = [len(p)-1 for p in paths if p]
    return min(paths)


day = 12
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

board = {}
with open(f) as file:
    for y, line in enumerate(file.readlines()):
        for x, c in enumerate(line.strip()):
            board[x,y] = c

src = [k for k, v in board.items() if v == 'S'][0]
dest = [k for k, v in board.items() if v == 'E'][0]

board[src] = 'a'
board[dest] = 'z'

print(f'part1: {p1()}')
print(f'part2: {p2()}')
