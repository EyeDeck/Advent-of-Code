from ec import *


def p1():
    data = parse_grid(1)[0]
    print(data)
    board = set(k for k,v in data.items() if v == '#')

    DIAGDIRS = [
        (1, -1),
        (-1, -1),
        (-1, 1),
        (1, 1),
    ]

    acc = 0
    for i in range(10):
        # print(i)
        # print_2d('.', {k:'#' for k in board})
        new_board = set()
        for pos in data:
            print(pos, [1 for x in DIAGDIRS if vadd(x, pos) in board])
            n = sum(1 for x in DIAGDIRS if vadd(x, pos) in board)
            if pos in board:
                if n & 1:
                    new_board.add(pos)
            else:
                if not n & 1:
                    new_board.add(pos)

        board = new_board
        acc += len(board)

    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    return acc


def p2():
    data = parse_grid(2)[0]
    print(data)
    board = set(k for k,v in data.items() if v == '#')

    DIAGDIRS = [
        (1, -1),
        (-1, -1),
        (-1, 1),
        (1, 1),
    ]

    acc = 0
    for i in range(2025):
        # print(i)
        # print_2d('.', {k:'#' for k in board})
        new_board = set()
        for pos in data:
            # print(pos, [1 for x in DIAGDIRS if vadd(x, pos) in board])
            n = sum(1 for x in DIAGDIRS if vadd(x, pos) in board)
            if pos in board:
                if n & 1:
                    new_board.add(pos)
            else:
                if not n & 1:
                    new_board.add(pos)

        board = new_board
        acc += len(board)

    # data = parse_lines(1, get_ints)
    # data = parse_double_break(1)

    return acc


def p3():
    grid_size = 34
    initial_state = {(x,y):'#' for x in range(grid_size) for y in range(grid_size)}
    interesting_pattern = parse_grid(3)[0]
    pattern_size = grid_bounds(interesting_pattern)
    half_x, half_y = (pattern_size[2] + 1) // 2, (pattern_size[3] + 1) // 2
    print(pattern_size, half_x, half_y)

    offset = (grid_size // 2) - half_x, (grid_size // 2) - half_y,
    ip_pos = set(vadd(k, offset) for k,v in interesting_pattern.items() if v == '#')
    ip_neg = set(vadd(k, offset) for k,v in interesting_pattern.items() if v == '.')

    print(ip_pos, ip_neg)
    print_2d(' ', {k: '#' for k in ip_pos})
    print_2d(' ', {k: '.' for k in ip_neg})

    board = set(k for k,v in initial_state.items() if v == '#')

    # print_2d('.', {k: '#' for k in board})

    DIAGDIRS = [
        (1, -1),
        (-1, -1),
        (-1, 1),
        (1, 1),
    ]

    seen_states = {}
    interesting_states = []
    acc = 0
    cycle_len = INF
    for i in range(1000000000):
        new_board = set()
        for pos in initial_state:
            n = sum(1 for x in DIAGDIRS if vadd(x, pos) in board)
            if pos in board:
                if n & 1:
                    new_board.add(pos)
            else:
                if not n & 1:
                    new_board.add(pos)
        board = new_board

        hashable = frozenset(board)
        if hashable in seen_states:
            print('found loop from', seen_states[hashable], 'to', i)
            cycle_len = i
            print(interesting_states)
            break

        if ip_pos.issubset(board) and ip_neg.isdisjoint(board):
            interesting_states.append((i, len(board)))
        seen_states[hashable] = i

        # print(i)
        # print_2d('.', {k: '#' for k in board})

        # acc += len(board)
    full_cycles, remaining = 1000000000 // cycle_len, 1000000000 % cycle_len



    return sum(t[1] for t in interesting_states)*full_cycles + sum(t[1] for t in interesting_states if t[0] < remaining)


setquest(14)

# print('part1:', p1())
# print('part2:', p2())
print('part3:', p3())
