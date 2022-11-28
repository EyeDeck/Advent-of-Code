inp = open('d3.txt').readlines()
wires = [i.split(",") for i in inp]
wires = [[(i[0], int(i[1:])) for i in w] for w in wires]

dirs = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

board = [{} for i in range(len(wires))]
for w in range(0, len(wires)):
    x, y, ln = 0, 0, 0

    for wire in wires[w]:
        inc = dirs[wire[0]]

        for i in range(0, wire[1]):
            ln += 1
            x += inc[0]
            y += inc[1]
            if (x, y) not in board:
                board[w][(x, y)] = ln

dists, lens = [], []
for k, v in board[0].items():
    if k in board[1]:
        dists.append(abs(k[0]) + abs(k[1]))
        lens.append(v + board[1][k])
print('d1: {}\nd2: {}'.format(min(dists), min(lens)))
