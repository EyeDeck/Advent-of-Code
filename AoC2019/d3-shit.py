inp = open("d3.txt").readlines()
wires = [i.split(",") for i in inp]
wires = [[(i[0], int(i[1:])) for i in w] for w in wires]

board = [{} for i in range(len(wires))]
for w in range(0,len(wires)):
    board[w] = {}
    x = 0
    y = 0
    l = 0
    for wire in wires[w]:
        inc = (0,0)
        if wire[0] == 'L':
            inc = (-1,0)
        elif wire[0] == 'R':
            inc = (1, 0)
        elif wire[0] == 'U':
            inc = (0, 1)
        else:  # 'D'
            inc = (0, -1)

        for i in range(0, wire[1]):
            l += 1
            x += inc[0]
            y += inc[1]
            if (x,y) not in board:
                board[w][(x,y)] = l

dists = []
for k, v in board[0].items():
    if k in board[1]:
        dists.append(abs(k[0]) + abs(k[1]))
dists = sorted(dists)
print('d1:', dists[0])

lens = []
for k, v in board[0].items():
    if k in board[1]:
        lens.append(v + board[1][k])
lens = sorted(lens)
print('d2:', lens[0])