from ec import *


def tick_board(board, width, height):
    diag = [(1, -1), (-1, -1), (-1, 1), (1, 1)]

    new_board = set()
    for x in range(width):
        for y in range(height):
            pos = (x, y)
            n = sum(1 for c in diag if vadd(c, pos) in board)
            if pos in board:
                if n & 1:
                    new_board.add(pos)
            else:
                if not n & 1:
                    new_board.add(pos)
    return new_board


def count_ticks(puzzle, tick_ct):
    data = parse_grid(puzzle)[0]
    board = set(k for k, v in data.items() if v == '#')
    bounds = grid_bounds(data)
    width, height = bounds[2]+1, bounds[3]+1

    acc = 0
    for i in range(tick_ct):
        board = tick_board(board, width, height)
        acc += len(board)
    return acc


def p3(width, height):
    initial_state = {(x, y): '#' for x in range(width) for y in range(height)}
    interesting_pattern = parse_grid(3)[0]
    pattern_size = grid_bounds(interesting_pattern)
    half_x, half_y = (pattern_size[2] + 1) // 2, (pattern_size[3] + 1) // 2

    offset = (width // 2) - half_x, (height // 2) - half_y,
    ip_pos = set(vadd(k, offset) for k, v in interesting_pattern.items() if v == '#')
    ip_neg = set(vadd(k, offset) for k, v in interesting_pattern.items() if v == '.')

    # print_2d(' ', {k: '#' for k in ip_pos})
    # print_2d(' ', {k: '.' for k in ip_neg})

    board = set(k for k, v in initial_state.items() if v == '#')

    interesting_states = []
    cycle_len = INF
    for i in range(1000000000):
        board = tick_board(board, width, height)

        # if i & 1 and board:
        #     print_2d('  ', {k: '#' for k in board})

        # culled proper cycle detection code, because initial state and algo are fixed,
        # and this one always loops back around to a fully empty state
        if i > 1 and len(board) == width * height:
            # print('found loop from', 0, 'to', i)
            cycle_len = i + 1
            break

        if ip_pos.issubset(board) and ip_neg.isdisjoint(board):
            interesting_states.append((i, len(board)))

    full_cycles = 1000000000 // cycle_len
    remaining = 1000000000 % cycle_len

    full_cycle_ct = sum(t[1] for t in interesting_states) * full_cycles
    remaining_ct = sum(t[1] for t in interesting_states if t[0] < remaining)

    return full_cycle_ct + remaining_ct


setquest(14)


print('part1:', count_ticks(1, 10))
print('part2:', count_ticks(2, 2025))
print('part3:', p3(34,34))
