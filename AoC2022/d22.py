from collections import *

from aoc import *


# print_2d(padding, *dicts, constrain=(-256, -256, 256, 256)):
# print_2d_repl(padding, *dicts, constrain=(-256, -256, 256, 256)):

DIRS = [
    (1, 0),  # r
    (0, 1),  # d
    (-1, 0),  # l
    (0, -1),  # u
]
DIRS_C = ['>', 'v', '<', '^']

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
        print(d)
        if isinstance(d, int):
            path[cur] = DIRS_C[heading]
            for i in range(d):
                nx = vadd(cur, DIRS[heading])
                if nx not in board:
                    print(nx, 'not in board')
                    nx = vsub(nx, DIRS[heading])

                    while nx in board:
                        nx = vsub(nx, DIRS[heading])
                        print('back', nx)

                    nx = vadd(nx, DIRS[heading])

                print('hit a wall')
                if board[nx] == '#':
                    break

                path[nx] = DIRS_C[heading]

                print(cur)
                cur = nx

            # p_size = 20
            # cs = (cur[0]-p_size, cur[1]-p_size, cur[0]+p_size, cur[1]+p_size)
            # print(cs)
            # print_2d(' ', board, path) # , constrain = cs)
            # input()
        else:
            heading += 1 if d == 'R' else -1
            heading %= 4

            print('heading=', heading, '(', DIRS_C[heading], ')')

    print_2d(' ', board, path, {cur: '@'})

    col = cur[0] + 1
    row = cur[1] + 1
    print(col, row, DIRS_C[heading])
    return row * 1000 + col * 4 + heading


# def get_chunk(board, seen, cur, s):
#     face = {}
#     x, y = cur
#     for x_o in range(x, x + s):
#         for y_o in range(y, y + s):
#             face[x_o-x, y_o-y] = board[x_o, y_o]
#
#     for d, off in enumerate(DIRS):
#         print('cur, d, off', cur, d, off, vmul(DIRS[d], (s, s)))
#         face_c = vadd(cur, vmul(DIRS[d], (s, s)))
#         if face_c not in board:
#             continue
#
#         if (cur, face_c) in seen:
#             continue
#
#         seen.add((cur, face_c))
#         print(face_c, board[face_c], DIRS_C[d])
#         face[d] = get_chunk(board, seen, face_c, s)
#     return face


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
            print('cur, d, off', cur, d, off, vmul(DIRS[d], (s, s)))
            face_c = vadd(cur, vmul(DIRS[d], (s, s)))

            if face_c not in board:
                continue

            if frozenset([cur, face_c]) in seen:
                continue

            seen.add(frozenset([cur, face_c]))

            stack.append((i, d, face_c))

        print(stack)
    return face


warp_map = {
    (1, '<'): (5, '>', -1),
    (1, '^'): (6, '>', 1),
    # (1, '>'): (2, '>'),
    # (1, 'v'): (3, 'v'),

    # (2, '<'): (1, '<'),
    (2, '^'): (6, '^', 1),
    (2, '>'): (4, '<', -1),
    (2, 'v'): (3, '<', 1),

    (3, '<'): (5, 'v', 1),
    # (3, '^'): (1, '^'),
    (3, '>'): (2, '^', 1),
    # (3, 'v'): (4, 'v'),

    # (4, '<'): (5, '<'),
    # (4, '^'): (3, '^'),
    (4, '>'): (2, '<', -1),
    (4, 'v'): (6, '<', 1),

    (5, '<'): (1, '>', -1),
    (5, '^'): (3, '>', 1),
    # (5, '>'): (4, '>'),
    # (5, 'v'): (6, 'v'),

    (6, '<'): (1, 'v', 1),
    # (6, '^'): (5, '^'),
    (6, '>'): (4, '^', 1),
    (6, 'v'): (2, 'v', 1),
}


def p2():
    face_size = 4

    cur = (0, 0)
    heading = 0
    path = {}
    while True:
        if cur in board:
            break
        cur = vadd(cur, (1, 0))
    top_l = cur
    # front, right, back, left, up, down
    face_map = {}

    seen = set()
    cube_map = get_chunk(board, seen, cur, face_size)

    # print(cube_map)
    for k, v in cube_map.items():
        print(k, v)
        print_2d(' ', v)

    # for y in range(cur[1], face_size):
    #     for x in range(cur[0], face_size):
    #         faces[0][x,y] = board[x,y]
    #         del board[x,y]
    # faces[0] =
    # print_2d(' ', faces[0])

    return None


def get_warp(c, h):
    print('warping', c, h)
    print('current face', faces[c])
    print('current dir', DIRS_C[h])
    next_key = (int(faces[c]), DIRS_C[h])
    print(next_key)
    print('next edge', warp_map[next_key])
    new_coord = c
    new_heading = h

    return new_coord, new_heading

def p2():
    cur = (0, 0)
    heading = 0
    path = {}
    while True:
        if cur in board:
            break
        cur = vadd(cur, (1, 0))
    for d in dirs:
        print(d)
        if isinstance(d, int):
            path[cur] = DIRS_C[heading]
            for i in range(d):
                nx = vadd(cur, DIRS[heading])
                if nx not in board:
                    nx, nx_h = get_warp(cur, heading)

                print('hit a wall')
                if board[nx] == '#':
                    break

                path[nx] = DIRS_C[heading]

                print(cur)
                cur = nx

            # p_size = 20
            # cs = (cur[0]-p_size, cur[1]-p_size, cur[0]+p_size, cur[1]+p_size)
            # print(cs)
            # print_2d(' ', board, path) # , constrain = cs)
            # input()
        else:
            heading += 1 if d == 'R' else -1
            heading %= 4

            print('heading=', heading, '(', DIRS_C[heading], ')')

    print_2d(' ', board, path, {cur: '@'})

    col = cur[0] + 1
    row = cur[1] + 1
    print(col, row, DIRS_C[heading])
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

faces = {}
for y, line in enumerate(face_raw.splitlines()):
    for x, c in enumerate(line):
        if c == ' ':
            continue
        faces[x, y] = c

face_whatever = [{} for _ in range(6)]

dirs = [int(i) if i.isnumeric() else i for i in dir_raw.replace('R', ' R ').replace('L', ' L ').split(' ')]

print_2d(' ', board)
# print(dirs)

# print('part1:', p1() )
print('part2:', p2())
