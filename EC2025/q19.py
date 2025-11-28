from ec import *


def solve(n):
    data = parse_lines(n, get_ints)
    board = defaultdict(list)
    start = (0, 0)

    for line in data:
        x, low, opening = line
        min_y = low
        max_y = low + opening - 1

        # trim parts of ranges that are inaccessible (on the wrong part of the checkerboard)
        if min_y & 1 != x & 1:
            min_y += 1
        if max_y & 1 != x & 1:
            max_y -= 1

        if min_y > max_y:
            continue

        board[x].append((min_y, max_y))

    for k in board.keys():
        board[k] = merge_ranges(board[k])

    cur = 0
    next_columns = {}
    for x in board:
        next_columns[cur] = x
        cur = x

    cur_x = 0
    cur_ranges = [start]
    acc = 0
    while cur_x in next_columns:
        next_x = next_columns[cur_x]
        projections = []

        dist = next_x - cur_x
        for y_range in cur_ranges:
            y_min, y_max = y_range
            next_min = max(0, y_min - dist)
            next_max = y_max + dist
            # print(y_range, 'projects to', next_min, next_max, 'on', next_x)
            projections.append([next_min, next_max])

        next_ranges = intersect_ranges(projections, board[next_x])
        acc += (next_ranges[0][0] - cur_ranges[0][0]) + dist

        cur_x = next_x
        cur_ranges = next_ranges

    return acc // 2


setquest(19)

print('part3:', solve(1))
print('part3:', solve(2))
print('part3:', solve(3))
