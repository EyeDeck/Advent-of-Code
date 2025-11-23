import math

from aoc import *

@memo
def rotate(s):
    l = len(s)
    sq = int(math.sqrt(l))
    seq = [(sq - 1 - (i % sq)) * sq + (i // sq) for i in range(l)]
    return ''.join(s[i] for i in seq)

@memo
def flip(s):
    l = len(s)
    sq = int(math.sqrt(l))
    seq = [(sq - 1) - i % sq + (i // sq * sq) for i in range(l)]
    return ''.join(s[i] for i in seq)


@memo
def get_next(s):
    for _ in range(4):
        if s in data:
            return data[s]
        f = flip(s)
        if f in data:
            return data[f]
        s = rotate(s)


def make_dict(s, l):
    s_split = [s[i:i + l] for i in range(0, l * l, l)]
    return {(x, y): c for y, line in enumerate(s_split) for x, c in enumerate(line)}


def get_chunk(d, x, y, x_len, y_len):
    s = []
    for ry in range(0, y_len):
        for rx in range(0, x_len):
            s.append(d[rx + x, ry + y])
    return ''.join(s)


def offset_2d(d, x, y):
    return {vadd(k, (x, y)): v for k, v in d.items()}


def solve(step_count):
    grid_size = 3
    board = make_dict('.#...####', 3)
    for i in range(step_count):
        next_board = {}
        n, other_n = (2, 3) if grid_size % 2 == 0 else (3, 4)

        for y in range(0, grid_size // n):
            for x in range(0, grid_size // n):
                # let's LARP as a functional language here for no reason lol
                next_board.update(offset_2d(make_dict(get_next(get_chunk(board, x * n, y * n, n, n)), n + 1), x * (n + 1), y * (n + 1)))

        board = next_board
        grid_size = grid_size // n * other_n
        if verbose:
            print(f'after step {i + 1}, grid_size={grid_size}')
            print_2d(' ', board)
            input()
    return sum(1 for v in board.values() if v == '#')


setday(21)

data = {k: v for k, v in parselines(lambda x: x.replace('/', '').split(' => '))}

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', solve(5))
print('part2:', solve(18))
