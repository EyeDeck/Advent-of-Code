import sys
import re
import colorama
import numpy as np
from collections import Counter
from PIL import Image, ImageDraw, ImageFont


def get_neighbors(board, x, y):
    neighbors = []
    for x_mod, y_mod in dirs:
        x2 = x + x_mod
        y2 = y + y_mod
        if x2 < arr_bounds[0][0] or x2 >= arr_bounds[1][0] or y2 < arr_bounds[0][1] or y2 >= arr_bounds[1][1]:
            continue
        else:
            neighbors.append(board[x2][y2])
    return neighbors


def get_los(board, x, y):
    neighbors = []
    for x_mod, y_mod in dirs:
        x2 = x + x_mod
        y2 = y + y_mod
        while arr_bounds[0][0] <= x2 < arr_bounds[1][0] and arr_bounds[0][1] <= y2 < arr_bounds[1][1]:
            c = board[x2][y2]
            if c != '.':
                neighbors.append(c)
                break
            x2 += x_mod
            y2 += y_mod
    return neighbors


def render_array(bd):
    # as_str = np.array2string(np.swapaxes(bd, 0, 1), max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
    as_str = np.array2string(bd, max_line_width=200, separator=' ', threshold=1000, edgeitems=1000,
                             formatter={'str_kind': lambda x: x})
    # print('\x1b[1;1H\r', re.sub('[\[\]]', '', as_str), end='\n')
    print(' ', re.sub('[\[\]]', '', as_str), end='\n')


def render_image(board, loc="dxx.png", scale=4):
    char_arr = board.view(np.uint32).astype(np.uint8)
    palette = [0 for _ in range(128*3)]
    palette[46*3:46*3+3] = [0, 0, 0]  # .
    palette[76*3:76*3+3] = [0x50, 0x50, 0x50]  # L
    palette[35*3:35*3+3] = [0, 0xFF, 0]  # #

    img = Image.fromarray(char_arr, "P").resize((char_arr.shape[0]*scale, char_arr.shape[1]*scale))
    img.putpalette(palette)
    img.save(loc)


def step_board(board, adj_func, los_max):
    new = np.empty_like(board)
    for x, row in enumerate(board):
        for y, c in enumerate(row):
            if c == '.':
                new[x, y] = '.'
            elif c == 'L':
                adj_ct = Counter(adj_func(board, x, y))
                if '#' not in adj_ct:
                    new[x, y] = '#'
                else:
                    new[x, y] = 'L'
            elif c == '#':
                adj_ct = Counter(adj_func(board, x, y))
                if '#' in adj_ct and adj_ct['#'] >= los_max:
                    new[x, y] = 'L'
                else:
                    new[x, y] = '#'
    return new


def p1():
    stepped = np.copy(data)
    i = 0
    render_image(stepped, f'd11_1\\{str(i).zfill(4)}.png', 4)
    while True:
        last = np.copy(stepped)
        stepped = step_board(last, get_neighbors, 4)
        i += 1
        render_image(stepped, f'd11_1\\{str(i).zfill(4)}.png', 4)
        if np.array_equal(last, stepped):
            return (last == '#').sum()


def p2():
    stepped = np.copy(data)
    i = 0
    render_image(stepped, f'd11_2\\{str(i).zfill(4)}.png', 4)
    while True:
        last = np.copy(stepped)
        stepped = step_board(last, get_los, 5)
        i += 1
        render_image(stepped, f'd11_2\\{str(i).zfill(4)}.png', 4)
        if np.array_equal(last, stepped):
            return (last == '#').sum()


# colorama.init()

f = 'd11.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = np.array(np.swapaxes([[c for c in line.strip()] for line in file], 0, 1))

arr_bounds = ((0, 0), data.shape)
render_image(data)

# render_array(data)

dirs = []
for x in range(-1, 2):
    for y in range(-1, 2):
        dirs.append((x, y))
dirs.remove((0, 0))
print(dirs)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
