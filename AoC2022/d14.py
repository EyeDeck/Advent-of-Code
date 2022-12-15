import copy
import argparse
from operator import itemgetter
from aoc import print_2d
from PIL import Image, ImageColor


def p1(board):
    i = 0
    while step(board):
        i += 1
        # print_2d('.', board, constrain=(-9999, -9999, 9999, 9999))
    return i


step_order = [
    lambda x, y: (x, y + 1),
    lambda x, y: (x - 1, y + 1),
    lambda x, y: (x + 1, y + 1)
]


def step(board):
    x, y = 500, 0
    if (x, y) in board:
        return False
    while True:
        for func in step_order:
            n = func(x, y)
            if n not in board:
                x, y = n
                break
        else:
            board[x, y] = 'o'
            return True
        if y > board['abyss']:
            return False


def p2(board):
    abyss = board['abyss']
    # for i in range(-(abyss//5) - 1, abyss + 2):
    for i in range(-abyss - 1, abyss + 2):
        board[500 + i, (abyss + 1)] = '#'

    front = {(500, 0)}
    acc = 0
    ticks_since_frame = 100
    frame = 1

    if RENDER:
        inputs = board, {(499, 0): ' '}
        squished = {}
        for d in inputs:
            squished.update({k: v for k, v in d.items() if isinstance(k, tuple)})

        color_map = {' ': '#000', '.': '#FFF484', 'o': '#EFD57C', '#': '#9E9E9E'}
        color_map = {k: ImageColor.getcolor(v, 'RGB') for k, v in color_map.items()}

        bounds = min(squished, key=itemgetter(0))[0], min(squished, key=itemgetter(1))[1], \
                 max(squished, key=itemgetter(0))[0], max(squished, key=itemgetter(1))[1]
        o_x, o_y = bounds[:2]
        w, h = bounds[2] - o_x + 1, (bounds[3] - o_y + 1)

        img = Image.new('RGB', (w, h))

        for k, v in squished.items():
            x, y = k[0] - o_x, k[1] - o_y,
            img.putpixel((x, y), color_map[v])

    while front:
        c = front.pop()
        board[c] = 'o'
        acc += 1
        new = [d for d in (f(*c) for f in step_order) if d not in board]

        front.update(new)

        if RENDER:
            print('frame', frame, end='\r')
            x, y = c[0] - o_x, c[1] - o_y,
            for coord in new:
                img.putpixel((coord[0]-o_x, coord[1]-o_y), color_map['.'])
            img.putpixel((x, y), color_map['o'])

            ticks_since_frame += 1
            if ticks_since_frame >= (len(front) // FRAME_SCALE):
                scaled_img = img.resize((w * SIZE_SCALE, h * SIZE_SCALE), 0) if SIZE_SCALE != 1 else img
                scaled_img.save(f'media\\d14\\{str(frame).zfill(5)}.png')
                frame += 1
                ticks_since_frame = 0

    if RENDER:
        img.save(f'media\\d14\\{str(frame).zfill(5)}.png')

    return acc


day = 14

parser = argparse.ArgumentParser()
parser.add_argument('file', default=f'd{day}.txt')
parser.add_argument('-f-mult', default=1, type=int)
parser.add_argument('-f-scale', default=4, type=int)
parser.add_argument('-r', '--render', action='store_true')
parser.add_argument('-p1', '--skip-p1', action='store_true')
args = parser.parse_intermixed_args()

FRAME_SCALE = args.f_mult
SIZE_SCALE = args.f_scale
RENDER = args.render
f = args.file

with open(f) as file:
    board = {}
    for line in [[tuple(int(i) for i in coord.split(',')) for coord in line.strip().split(' -> ')] for line in file]:
        for i in range(len(line) - 1):
            [x1, y1], [x2, y2] = line[i], line[i + 1]
            if x1 == x2:
                y1, y2 = sorted([y1, y2])
                for y in range(y1, y2 + 1):
                    board[x1, y] = '#'
            elif y1 == y2:
                x1, x2 = sorted([x1, x2])
                for x in range(x1, x2 + 1):
                    board[x, y1] = '#'
            else:
                raise Exception('bad input?')
    board['abyss'] = max(board.keys(), key=itemgetter(1))[1] + 1

if not args.skip_p1:
    print('part1:', p1(copy.deepcopy(board)))

print('part2:', p2(copy.deepcopy(board)))
