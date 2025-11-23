import math

from aoc import *


# def rotate(s):
#     # I'm sure it's not that hard to generalize this, but screw it
#     if len(s) == 9:
#         # 012    630
#         # 345 => 741
#         # 687    852
#         # 012345678 => 630741852
#
#         return ''.join(s[i] for i in [6, 3, 0, 7, 4, 1, 8, 5, 2])
#     else:
#         # 0123    c840
#         # 4567 => d951
#         # 89ab    ea62
#         # cdef    fb73
#         # 0123456789abcdef => c840d951ea62fb73
#         return ''.join(s[i] for i in [0xc, 8, 4, 0, 0xd, 9, 5, 1, 0xe, 0xa, 6, 2, 0xf, 0xb, 7, 3])
#
#
# def flip(s):
#     l = len(s)
#     sq = int(math.sqrt(l))
#     seq = [(sq - 1) - i % sq + (i // sq * sq) for i in range(l)]
#     return ''.join(s[i] for i in seq)
#
#
# def get_next(s):
#     for _ in range(4):
#         if s in data:
#             return data[s]
#         f = flip(s)
#         if f in data:
#             return data[f]
#         s = rotate(s)


@memo
def make_dict(s, l):
    s_split = [s[i:i + l] for i in range(0, l * l, l)]
    return {(x, y): c for y, line in enumerate(s_split) for x, c in enumerate(line)}


def squish(x, y, d):
    s = []
    for cy in range(y):
        for cx in range(x):
            s.append(d[cx, cy])
    return ''.join(s)


def get_chunk(x, y, x_len, y_len, d):
    chunk = {}
    for ry in range(0, y_len):
        for rx in range(0, x_len):
            chunk[rx, ry] = d[rx + x, ry + y]
    return chunk


def offset_2d(d, x, y):
    return {vadd(k, (x, y)): v for k, v in d.items()}


@memo
def get_next(s, l):
    if s in data:
        # print('straight hit on', s)
        return data[s]

    as_dict = make_dict(s, l)
    for i in range(4):
        flipped = {(k[1], k[0]): v for k, v in as_dict.items()}
        squished_flipped = squish(l, l, flipped)
        if squished_flipped in data:
            # print('found (f)', squished_flipped)
            return data[squished_flipped]
        as_dict = rotate_2d(as_dict, 90, True, l - 1, l - 1)
        squished = squish(l, l, as_dict)
        if squished in data:
            # print('found (r)', squished)
            return data[squished]


def p1():
    grid_size = 3
    board = make_dict('.#...####', 3)
    for i in range(18):
        # print('------', i)
        next_board = {}
        n = 2 if grid_size % 2 == 0 else 3

        for y in range(0, grid_size // n):
            for x in range(0, grid_size // n):

                chunk = get_chunk(x * n, y * n, n, n, board)
                # print('subchunk', x, y)
                # print_2d(' ', chunk)
                squished = squish(n, n, chunk)

                # print('squished:', squished)
                next_chunk = get_next(squished, n)
                next_chunk_dict = offset_2d(make_dict(next_chunk, n+1), x*(n+1), y*(n+1))
                # print('found to make:', next_chunk)
                # print_2d(' ', next_chunk_dict)
                next_board.update(next_chunk_dict)

        board = next_board
        grid_size = get_2d_dim(board, 0)+1
        # print('new board:', grid_size)
        # print_2d(' ', board)
        # input()
    return sum(1 for v in board.values() if v == '#')


# 210 too high

def p2():
    return None


setday(21)

data = {k: v for k, v in parselines(lambda x: x.replace('/', '').split(' => '))}

# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

# with open_default() as file:
#     data = get_ints(file.read())

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())

# print('part1: %d\npart2: %d' % solve())
