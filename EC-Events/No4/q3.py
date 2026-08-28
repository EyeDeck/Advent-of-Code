from ec import *


def p1():
    data = parse_lines(1)
    width, height = [get_ints(x)[0] for x in data[:2]]
    h_o, v_o = [x.split('=')[1] for x in data[2:4]]
    print(width, height, h_o, v_o)

    board = {}
    for y in range(height+1):
        print(y)
        p = int(h_o[y % len(h_o)])
        for x in range(p,width,2):
            board[x*2,y*2] = '—'

    for x in range(width+1):
        p = int(v_o[x % len(v_o)])
        for y in range(p,height,2):
            board[x*2-1,y*2+1] = '|'

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

    # print_2d('  ', board)
    print_2d('  ', board, {k:'~' for k in surrounded})
    # print_2d('  ', {k:'.' for k in adj})


    return acc


def p2():
    data = parse_lines(2)
    width, height = [get_ints(x)[0] for x in data[:2]]
    h_o, v_o = [x.split('=')[1] for x in data[2:4]]
    # print(width, height, h_o, v_o)

    board = {}
    for y in range(height+1):
        # print(y)
        p = int(h_o[y % len(h_o)])
        for x in range(p,width,2):
            board[x*2,y*2] = '—'

    for x in range(width+1):
        p = int(v_o[x % len(v_o)])
        for y in range(p,height,2):
            board[x*2-1,y*2+1] = '|'

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

    # print_2d('  ', board)
    # print_2d('  ', board, {k:'~' for k in surrounded}, {k:'.' for k in adj})
    # print_2d('  ', {k:'.' for k in adj})

    # real_tiles = set()
    # for x in range(width):
    #     for y in range(height):
    #         real_tiles.add((x*2, y*2+1))
    #
    # print_2d('  ', board, {k: '#' for k in real_tiles})

    colored_tiles = {}
    color = True
    for y in range(height):
        pos = (0, y*2+1)
        below = (0, y*2+2)
        colored_tiles[pos] = color
        if below in board and board[below] == '—':
            color = not color

    for y in range(height):
        color = colored_tiles[0,y*2+1]
        for x in range(width):
            pos = (x*2, y*2+1)
            right = (x*2+1, y*2+1)
            colored_tiles[pos] = color
            if right in board and board[right] == '|':
                color = not color

    # print(board)
    # print(colored_tiles)

    print_2d('  ', board, {k: '~' for k in surrounded}, {k: 'A' if v else 'B' for k,v in colored_tiles.items()})

    isolates_true = 0
    isolates_false = 0
    for isolate in surrounded:
        if colored_tiles[isolate]:
            isolates_true += 1
        else:
            isolates_false += 1

    return isolates_true, isolates_false
    return max(isolates_true, isolates_false)


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

    if board:
        print_2d('  ', board) #, {k: '~' for k in surrounded}, {k: 'A' if v else 'B' for k,v in colored_tiles.items()})


    isolates_true = 0
    isolates_false = 0
    for isolate in surrounded:
        if colored_tiles[isolate]:
            isolates_true += 1
        else:
            isolates_false += 1

    return isolates_true, isolates_false


def p3():
    data = parse_lines(2)
    width, height = [get_ints(x)[0] for x in data[:2]]
    h_o, v_o = [x.split('=')[1] for x in data[2:4]]
    h_pattern_width = len(h_o)+1
    v_pattern_height = len(v_o)+1

    h_pattern_width_d = h_pattern_width * 2
    v_pattern_height_d = v_pattern_height * 2
    print(width, height, h_o, v_o)

    print(h_pattern_width, f'({h_pattern_width_d})', v_pattern_height, f'({v_pattern_height_d})')

    # can do this by breaking the whole grid down into parts and then multiplying
    # M M M . R
    # M M M . R
    # M M M . R
    # . . .
    # B B B  BR

    # use a 2*2 base grid to naturally preserve the toggle state
    main_tile_a, main_tile_b = get_surrounded_for(h_pattern_width_d+1, v_pattern_height_d+1, h_o, v_o)

    # how many times the main tile repeats, horizontally then vertically
    h_main_tiles = width // h_pattern_width_d
    v_main_tiles = height // v_pattern_height_d

    # this is the overwhelming majority of the grid in a large input
    acc_a = main_tile_a * h_main_tiles * v_main_tiles
    acc_b = main_tile_b * h_main_tiles * v_main_tiles


    # the leftover rows/columns
    right_tile_w = width % h_pattern_width_d
    bottom_tile_h = height % v_pattern_height_d

    print('per tile:', main_tile_a, main_tile_b)
    print('number of tiles:', h_main_tiles, 'x', v_main_tiles)
    print('actual:', get_surrounded_for(width - right_tile_w, height - bottom_tile_h, h_o, v_o))
    print('calculated:', (acc_a, acc_b))


    # print(main_tile_a, main_tile_b, right_tile_w, bottom_tile_h)

    # right_tile_a, right_tile_b = get_surrounded_for(right_tile_w, v_pattern_height_d+1, h_o, v_o)
    #
    # bottom_tile_a, bottom_tile_b = get_surrounded_for(h_pattern_width_d+1, bottom_tile_h, h_o, v_o)
    #
    # br_tile_a, br_tile_b = get_surrounded_for(right_tile_w, bottom_tile_h, h_o, v_o)
    #
    #
    #
    # acc_a += right_tile_a * v_main_tiles
    # acc_b += right_tile_b * v_main_tiles
    #
    # acc_a += bottom_tile_a * h_main_tiles
    # acc_b += bottom_tile_b * h_main_tiles
    #
    # acc_a += br_tile_a
    # acc_b += br_tile_b

    return acc_a, acc_b

# not 683828295010696
# not 683831186196428 (or +1)


def p3():
    data = parse_lines(3)
    width, height = [get_ints(x)[0] for x in data[:2]]
    h_o, v_o = [x.split('=')[1] for x in data[2:4]]
    # h_pattern_width = len(h_o)
    # v_pattern_height = len(v_o)
    h_pattern_width = len(v_o)
    v_pattern_height = len(h_o)

    print(width, height, h_o, v_o)

    print(h_pattern_width, v_pattern_height)

    # can do this by breaking the whole grid down into parts and then multiplying
    # M M M . R
    # M M M . R
    # M M M . R
    # . . .
    # B B B  BR

    acc_a = 0
    acc_b = 0

    actual_h_width = h_pattern_width * 2
    actual_v_height = v_pattern_height * 2

    h_reps = width // (h_pattern_width * 2)
    v_reps = height // (v_pattern_height * 2)

    h_leftover = width % (h_pattern_width * 2)
    v_leftover = height % (v_pattern_height * 2)

    print(f'main pattern (fits {h_reps * v_reps} times)')
    main_a, main_b = get_surrounded_for((h_pattern_width * 2), (v_pattern_height * 2), h_o, v_o)

    print(f'bottom pattern (fits {h_reps} times)')
    bot_a, bot_b = get_surrounded_for((h_pattern_width * 2), v_leftover, h_o, v_o)
    print(f'right pattern (fits {v_reps} times)')
    right_a, right_b = get_surrounded_for(h_leftover, (v_pattern_height * 2), h_o, v_o)
    print('br pattern (fits once)')
    br_a, br_b = get_surrounded_for(h_leftover, v_leftover, h_o, v_o)

    print('h_reps:', h_reps, 'v_reps:', v_reps, 'h_leftover:', h_leftover, 'v_leftover:', v_leftover)

    acc_a += main_a * h_reps * v_reps
    acc_b += main_b * h_reps * v_reps

    acc_a += bot_a * h_reps
    acc_b += bot_b * h_reps

    acc_a += right_a * v_reps
    acc_b += right_b * v_reps

    acc_a += br_a
    acc_b += br_b

    return acc_a, acc_b




setquest(3)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
