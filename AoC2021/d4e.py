import sys


def solve_boards():
    for board in boards:
        for i, draw in enumerate(draws):
            if draw not in board:
                continue
            x, y = board[draw]
            del board[draw]
            board[(x,y)] = None
            if check_win(board, x, y):
                board['round'] = i
                board['draw'] = draw

                cum = 0
                for k,v in board.items():
                    if isinstance(k, tuple) and v is not None:
                        cum += v

                board['sum'] = cum
                board['score'] = cum * draw
                break


def check_win(board, x, y):
    for i in range(5):
        if board[(x,i)] is not None:
            break
    else:
        return True

    for i in range(5):
        if board[(i,y)] is not None:
            break
    else:
        return True

    return False


day = 4
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().split('\n\n')
    draws = [int(i) for i in data[0].split(',')]
    boards_raw = data[1:]
    boards = []
    for board in boards_raw:
        lines = board.split('\n')
        b = {}
        for x, line in enumerate(lines):
            for y, num in enumerate(line.split()):
                n = int(num)
                b[(x, y)] = n
                b[n] = (x, y)
        boards.append(b)

solve_boards()

mx, mxb = 0, None
mn, mnb = len(draws) + 1, None
for board in boards:
    r = board['round']
    if mx < r:
        mx = r
        mxb = board
    if mn > r:
        mn = r
        mnb = board

print(f'part1: { mnb["score"] }')
print(f'part2: { mxb["score"] }')