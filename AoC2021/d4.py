import sys


def apply_draw(draw):
    for board in boards:
        for k, v in board.items():
            if v == draw:
                board[k] = -1


def get_winners():
    wins = []
    for board in boards:
        for line in to_check:
            for coord in line:
                if board[coord] != -1:
                    break
            else:
                wins.append(board)
                break
    return wins if len(wins) > 0 else None


def p1():
    for draw in draws:
        apply_draw(draw)
        result = get_winners()
        if result:
            cum = 0
            for v in result[0].values():
                if v != -1:
                    cum += v
            return cum * draw
    return None


def p2():
    last = None
    last_draw = 0
    for draw in draws:
        apply_draw(draw)
        result = get_winners()
        if result is None:
            pass
        elif len(result) == 1:
            last = result[0]
            last_draw = draw
            boards.remove(last)
        elif len(result) > 1:
            for win in result:
                boards.remove(win)
    cum = 0
    for v in last.values():
        if v != -1:
            cum += v
    return cum * last_draw


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
                b[(x, y)] = int(num)
        boards.append(b)
        # print(b)

    to_check = []
    for x in range(5):
        v = []
        h = []
        for y in range(5):
            v.append((x, y))
            h.append((y, x))
        to_check.append(v)
        to_check.append(h)
    # print(to_check)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
