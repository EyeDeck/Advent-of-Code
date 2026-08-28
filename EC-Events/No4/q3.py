from ec import *


def get_surrounded_for(width, height, h_o, v_o):
    board = {}
    for y in range(height + 1):
        p = int(h_o[y % len(h_o)])
        for x in range(p, width, 2):
            board[x * 2, y * 2] = '—'

    for x in range(width + 1):
        p = int(v_o[x % len(v_o)])
        for y in range(p, height, 2):
            board[x * 2 - 1, y * 2 + 1] = '|'

    adj = set()
    for point in board.keys():
        for DIR in DIRS:
            adj.add(vadd(point, DIR))

    surrounded = set()

    acc = 0
    for point in adj:
        if sum([(vadd(point, DIR) in board) for DIR in DIRS]) == 4:
            acc += 1
            surrounded.add(point)

    colored_tiles = {}
    color = True
    for y in range(height):
        pos = (0, y * 2 + 1)
        below = (0, y * 2 + 2)
        colored_tiles[pos] = color
        if below in board and board[below] == '—':
            color = not color

    for y in range(height):
        color = colored_tiles[0, y * 2 + 1]
        for x in range(width):
            pos = (x * 2, y * 2 + 1)
            right = (x * 2 + 1, y * 2 + 1)
            colored_tiles[pos] = color
            if right in board and board[right] == '|':
                color = not color

    if board and verbose:
        # print_2d('  ', board, {k: '/' if v else '\\' for k,v in colored_tiles.items()}, {k: '~' for k in surrounded})
        print_2d('  ', board)

    isolates_true = 0
    isolates_false = 0
    for isolate in surrounded:
        if colored_tiles[isolate]:
            isolates_true += 1
        else:
            isolates_false += 1

    return isolates_true, isolates_false


def solve(part):
    data = parse_lines(part)
    width, height = [get_ints(x)[0] for x in data[:2]]
    h_o, v_o = [x.split('=')[1] for x in data[2:4]]

    h_pattern_width = len(v_o)
    v_pattern_height = len(h_o)

    # can do this by breaking the whole grid down into parts and then multiplying
    # M M M . R
    # M M M . R
    # M M M . R
    # . . .
    # B B B  BR

    actual_h_width = h_pattern_width * 2
    actual_v_height = v_pattern_height * 2

    h_reps = width // actual_h_width
    v_reps = height // actual_v_height

    h_leftover = width % actual_h_width
    v_leftover = height % actual_v_height

    if verbose: print(f'main pattern (fits {h_reps * v_reps} times)')
    main_a, main_b = get_surrounded_for(actual_h_width, actual_v_height, h_o, v_o)

    if verbose: print(f'bottom pattern (fits {h_reps} times)')
    bot_a, bot_b = get_surrounded_for(actual_h_width, v_leftover, h_o, v_o)

    if verbose: print(f'right pattern (fits {v_reps} times)')
    right_a, right_b = get_surrounded_for(h_leftover, actual_v_height, h_o, v_o)

    if verbose: print('br pattern (fits once)')
    br_a, br_b = get_surrounded_for(h_leftover, v_leftover, h_o, v_o)

    if verbose: print('h_reps:', h_reps, 'v_reps:', v_reps, 'h_leftover:', h_leftover, 'v_leftover:', v_leftover)

    acc_a = main_a * h_reps * v_reps
    acc_b = main_b * h_reps * v_reps

    acc_a += bot_a * h_reps
    acc_b += bot_b * h_reps

    acc_a += right_a * v_reps
    acc_b += right_b * v_reps

    acc_a += br_a
    acc_b += br_b

    if part == 1:
        return acc_a + acc_b
    else:
        return max(acc_a, acc_b)


setquest(3)

print('part1:', solve(1))
print('part2:', solve(2))
print('part3:', solve(3))
