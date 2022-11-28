import sys


def getneighbors(c, b, excl):
    r = []
    for d in DIRS:
        dr = (d[0] + c[0], d[1] + c[1])
        if dr in b and (excl is None or dr not in excl):
            r.append(dr)
    return r


def rgetneighbors(c, b, found):
    n = getneighbors(c, b, found)
    for coord in n:
        found.add(coord)
        rgetneighbors(coord, b, found)
    return found


def p1():
    cum = 0
    for coord, n in board.items():
        neigh = getneighbors(coord, board, None)
        for i in neigh:
            if board[i] <= n:
                break
        else:
            cum += n + 1
    return cum


def p2():
    basins = []
    while len(board) > 0:
        this_basin = set()
        basins.append(this_basin)

        sk, sv = board.popitem()
        this_basin.add(sk)
        rgetneighbors(sk, board, this_basin)

        for k in this_basin:
            if k in board:
                del board[k]

    lens = sorted([len(b) for b in basins])
    print(lens[-1], lens[-2], lens[-3])
    return lens[-1] * lens[-2] * lens[-3]


day = 9
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

DIRS = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

with open(f) as file:
    data = [line.strip() for line in file]
    board = {}
    for y, line in enumerate(data):
        for x, n in enumerate(line):
            board[(x, y)] = int(n)
    # easier to deal with if we just pop the 9s for this problem
    board = {k: v for k, v in board.items() if v != 9}

print(f'part1: {p1()}')
print(f'part2: {p2()}')
