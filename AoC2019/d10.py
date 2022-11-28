import math
import sys
import copy
from collections import defaultdict
from PIL import Image, ImageDraw
import numpy as np


def renderboard(board, beam, loc="d10.png", overlay=None):
    to_render = copy.deepcopy(board)
    for y, line in enumerate(board):
        for x, tile in enumerate(line):
            if tile == '.':
                to_render[x][y] = 0
            else:
                to_render[x][y] = 1
    if overlay:
        for k, v in overlay.items():
            if v == '~':
                to_render[k[0]][k[1]] = 2
            else:
                to_render[k[0]][k[1]] = 3
    if beam:
        pass
    to_render = np.swapaxes(np.array(to_render, dtype=np.uint8), 0, 1)
    palette = [0,0,0, 0x60,0x20,0, 0x19,0x08,0, 0,0xFF,0, 0xFF,0,0]

    img = Image.fromarray(to_render, "P")
    img.putpalette(palette)
    # img.show()
    img = img.resize(np.multiply(to_render.shape, (16, 16)))
    beam = [(x[0]*16+8,x[1]*16+8) for x in beam]
    draw = ImageDraw.Draw(img)
    draw.line(beam, fill=4, width=8)
    del draw
    img.save(loc)


def render(board, dim, overlay=None):
    if overlay is None:
        overlay = {}
    to_str = []
    for y in range(dim[0]):
        for x in range(dim[1]):
            if (x, y) in overlay:
                to_str.append(overlay[(x, y)])
            else:
                to_str.append(board[y][x])
            to_str.append(" ")
        to_str.append("\n")
    return "".join(to_str)


def has_los(start, end, asteroids):
    rel = (start[0] - end[0], start[1] - end[1])
    step_x, step_y = rel

    for i in range(max(abs(step_x), abs(step_y))+1, 0, -1):
        if (step_x % i) == 0 and (step_y % i) == 0:
            step_x //= i
            step_y //= i
    step = (step_x, step_y)

    cur = (end[0] + step[0], end[1] + step[1])

    while cur != start:
        if cur in asteroids:
            return False
        cur = (cur[0] + step[0], cur[1] + step[1])

    return True


def euclid_dist(a, b):
    return math.sqrt(math.pow((a[0]-b[0]), 2) + math.pow((a[1]-b[1]), 2))


f = 'd10.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]
board = [[c for c in ln.strip()] for ln in open(f).readlines()]

board = [c for c in board]
board_shape = {len(board), len(board[0])}

asteroids = set()
for y, line in enumerate(board):
    for x, tile in enumerate(line):
        if tile == '#':
            asteroids.add((x, y))

can_see = copy.deepcopy(board)

best = (0, (0, 0))
for a1 in asteroids:
    ct = 0
    for a2 in asteroids:
        if a1 == a2:
            continue
        elif has_los(a1, a2, asteroids):
            ct += 1
    can_see[a1[1]][a1[0]] = str(ct)
    if best[0] < ct:
        best = ct, a1

# print(render(can_see, (board_data['height'], board_data['width'])))
print('p1:', best[0])

asteroids.remove(best[1])
display = {best[1]: '@'}

bins = defaultdict(list)
for a in asteroids:
    bins[(math.atan2(a[0] - best[1][0], a[1] - best[1][1])*-1)].append(a)

for b, c in bins.items():
    c.sort(key=lambda k: euclid_dist(k, best[1]))

s = [bins[k] for k in sorted(bins)]
popped = []
i = 0
beam = [best[1], (0, 0)]

while len(s) > 0:
    for b in s:
        last = b.pop(0)
        popped.append(last)
        display[last] = '~'
        beam[1] = last
        renderboard(board, beam, "d10\\frame" + str(len(popped)).zfill(6) + ".png", display)
    s = [x for x in s if x]

print('p2:', popped[199][0] * 100 + popped[199][1])

# I assume the intended solution, for part 1, is, for each asteroid, calculate the angle (atan2) to every other
# asteroid, and store each asteroid's coordinates in a bin for its calculated angle; then count the bins,
# and keep whichever asteroid had the most bins in the end. atan2(1,5) calculates the same as atan2(2,10),
# and floating point precision is way more than good enough considering the small total number of bins. Answer is
# final bin count.

# For part 2, sort the asteroids in each bin by euclidean distance from the center asteroid, then start looping
# through the bins in order, popping the closest member. Note that you may have to fiddle with the coordinates you
# feed into atan2 by swapping signs/etc until the loop properly starts in the up direction, and rotates clockwise.
# Answer is the coordinates of the 200th asteroid popped.
