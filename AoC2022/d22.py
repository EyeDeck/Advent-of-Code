from collections import *

from aoc import *

DIRS = [
    (1, 0),  # r
    (0, 1),  # d
    (-1, 0),  # l
    (0, -1),  # u
]
DIRS_C = ['>', 'v', '<', '^']
DIRS_R = {'>': 0, 'v': 1, '<': 2, '^': 3}

turn_map = {
    'R': 1,
    'L': -1
}


def p1():
    cur = (0, 0)
    heading = 0
    path = {}
    while True:
        if cur in board:
            break
        cur = vadd(cur, (1, 0))
    for d in dirs:
        # print(d)
        if isinstance(d, int):
            path[cur] = DIRS_C[heading]
            for i in range(d):
                nx = vadd(cur, DIRS[heading])
                if nx not in board:
                    # print(nx, 'not in board')
                    nx = vsub(nx, DIRS[heading])

                    while nx in board:
                        nx = vsub(nx, DIRS[heading])
                        # print('back', nx)

                    nx = vadd(nx, DIRS[heading])

                if board[nx] == '#':
                    # print('hit a wall')
                    break

                path[nx] = DIRS_C[heading]

                # print(cur)
                cur = nx

            # p_size = 20
            # cs = (cur[0]-p_size, cur[1]-p_size, cur[0]+p_size, cur[1]+p_size)
            # print(cs)
            # print_2d(' ', board, path) # , constrain = cs)
            # input()
        else:
            heading += 1 if d == 'R' else -1
            heading %= 4

            # print('heading=', heading, '(', DIRS_C[heading], ')')

    # print_2d(' ', board, path, {cur: '@'})

    col = cur[0] + 1
    row = cur[1] + 1
    # print(col, row, DIRS_C[heading])
    return row * 1000 + col * 4 + heading


def get_chunk(board, seen, cur, s):
    face = defaultdict(dict)
    stack = [(0, 0, cur)]
    i = 0

    while stack:
        from_face, dir_from, cur = stack.pop()
        x, y = cur
        face[i]['from'] = (from_face, dir_from)

        for x_o in range(x, x + s):
            for y_o in range(y, y + s):
                face[i][x_o, y_o] = board[x_o, y_o]

        i += 1

        for d, off in enumerate(DIRS):
            # print('cur, d, off', cur, d, off, vmul(DIRS[d], (s, s)))
            face_c = vadd(cur, vmul(DIRS[d], (s, s)))

            if face_c not in board:
                continue

            if frozenset([cur, face_c]) in seen:
                continue

            seen.add(frozenset([cur, face_c]))

            stack.append((i, d, face_c))

        # print(stack)
    return face


# output: next face, next heading, flip_x, flip_y, swap_axes
warp_map = {
    (1, '<'): (5, '>', False, True, False),
    (1, '^'): (6, '>', False, False, True),
    # (1, '>'): (2, '>'),
    # (1, 'v'): (3, 'v'),

    # (2, '<'): (1, '<'),
    (2, '^'): (6, '^', False, True, False),
    (2, '>'): (4, '<', False, True, False),
    (2, 'v'): (3, '<', False, False, True),

    (3, '<'): (5, 'v', False, False, True),
    # (3, '^'): (1, '^'),
    (3, '>'): (2, '^', False, False, True),
    # (3, 'v'): (4, 'v'),

    # (4, '<'): (5, '<'),
    # (4, '^'): (3, '^'),
    (4, '>'): (2, '<', False, True, False),
    (4, 'v'): (6, '<', False, False, True),

    (5, '<'): (1, '>', False, True, False),
    (5, '^'): (3, '>', False, False, True),
    # (5, '>'): (4, '>'),
    # (5, 'v'): (6, 'v'),

    (6, '<'): (1, 'v', False, False, True),
    # (6, '^'): (5, '^'),
    (6, '>'): (4, '^', False, False, True),
    (6, 'v'): (2, 'v', False, True, False),
}


def get_warp(c, h):
    # print('warping', c, h)
    curr_face = int(faces[c])
    # print('current face', faces[c])
    # print('current dir', DIRS_C[h])
    next_key = (curr_face, DIRS_C[h])
    # print(next_key)
    # print('face_bounds[curr_face][0]', face_bounds[curr_face][0],'face_bounds[curr_face][1]', face_bounds[curr_face][1])

    norm_x, norm_y = c[0] - face_bounds[curr_face - 1][0], c[1] - face_bounds[curr_face - 1][1]
    # print('norm_x, norm_y', norm_x, norm_y)

    next_face, next_dir, flip_x, flip_y, swap_axes = warp_map[next_key]

    if swap_axes:
        next_x, next_y = norm_y, norm_x
    else:
        next_x, next_y = norm_x, norm_y

    # print('next_face, next_dir, next_x, next_y', next_face, next_dir, flip_x, flip_y)
    next_x_min, next_y_min, next_x_max, next_y_max = face_bounds[next_face - 1]

    if not flip_x:
        next_x = next_x_min + next_x
    else:
        next_x = next_x_max - next_x

    if not flip_y:
        next_y = next_y_min + next_y
    else:
        next_y = next_y_max - next_y

    next_coord = (next_x, next_y)

    # print('goto', next_coord, next_dir)
    return next_coord, DIRS_R[next_dir]


def p2():
    cur = (0, 0)
    heading = 0
    path = {}
    while True:
        if cur in board:
            break
        cur = vadd(cur, (1, 0))
    # for d in dirs:
    while dirs:
        d = dirs.pop(0)
        # print(f'current pos {cur}, heading {DIRS_C[heading]}, next input:', d)
        if isinstance(d, int):
            path[cur] = DIRS_C[heading]
            for i in range(d):
                nx = vadd(cur, DIRS[heading])
                nx_h = heading
                if nx not in board:
                    nx, nx_h = get_warp(cur, heading)

                if board[nx] == '#':
                    # print('hit a wall')
                    break

                heading = nx_h

                path[nx] = DIRS_C[heading]

                # print(cur)
                cur = nx

            # p_size = 20
            # cs = (cur[0]-p_size, cur[1]-p_size, cur[0]+p_size, cur[1]+p_size)
            # print(cs)
            # print_2d(' ', board, path) # , constrain = cs)
            # input()
        elif d and d in 'LRlr':
            heading += 1 if d in 'Rr' else -1
            heading %= 4

            # print('heading=', heading, '(', DIRS_C[heading], ')')
        # else:
        #     print('invalid input')

        # if not dirs:
        #     print_2d('  ', board, path, {cur: '@'})
        #
        #     dirs.extend(int(i) if i.isnumeric() else i for i in input('moves: ').split())

    # print_2d(' ', board, path, {cur: '@'})

    col = cur[0] + 1
    row = cur[1] + 1
    # print(col, row, DIRS_C[heading])
    return row * 1000 + col * 4 + heading


day = 22
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    map_raw, face_raw, dir_raw = file.read().split('\n\n')

board = {}
for y, line in enumerate(map_raw.splitlines()):
    for x, c in enumerate(line):
        if c == ' ':
            continue
        board[x, y] = c

# to save time I just hand-edited the input to have an extra chunk in it formatted like
#         11112222
#         11112222
#         11112222
#         11112222
#         3333
#         3333
#         3333
#         3333
#     55554444
#     55554444
#     55554444
#     55554444
#     6666
#     6666
#     6666
#     6666
# (completely arbitrarily numbered based off what I had initially scribbled on a paper cube)
# but scaled up to 50x50 per side or whatever, because manually numbering the faces
# in a text editor took all of 2 minutes, while writing a smarter parser would have taken much longer
faces = {}
face_whatever = [set() for _ in range(6)]
for y, line in enumerate(face_raw.splitlines()):
    for x, c in enumerate(line):
        if c == ' ':
            continue
        faces[x, y] = c
        # print(c)
        face_whatever[int(c) - 1].add((x, y))

# print(face_whatever)

face_bounds = [(min(s, key=itemgetter(0))[0], min(s, key=itemgetter(1))[1], max(s, key=itemgetter(0))[0],
                max(s, key=itemgetter(1))[1],) for s in face_whatever]
# print(face_bounds)

dirs = [int(i) if i.isnumeric() else i for i in dir_raw.replace('R', ' R ').replace('L', ' L ').split(' ')]

# print_2d(' ', board)
# print(dirs)

print('part1:', p1())
print('part2:', p2())
