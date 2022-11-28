import copy
import sys
import numpy as np
from PIL import Image


def render_image(board, loc="d3.png", overlay=None):
    to_render = copy.deepcopy(board)
    for x, line in enumerate(board):
        for y, tile in enumerate(line):
            if tile == '.':
                to_render[x,y] = 0
            else:
                to_render[x,y] = 1
    if overlay:
        for k, v in overlay.items():
            if v is not None:
                to_render[k[1], k[0]] = v

    to_render = np.array(to_render, dtype=np.uint8)
    palette = [0xFE,0xFE,0xFE, 0x20,0x66,0x20, 0x10,0,0xFF, 0,0x7B,0xFF]

    img = Image.fromarray(to_render, "P")
    img.putpalette(palette)
    img = img.resize((width*3,height*3))
    img.save(loc)


def explore_trees(x_inc, y_inc, render=0):  # render: every nth frame
    x = 0
    y = 0
    trees = 0
    while True:
        if data[y,x] == "#":
            trees += 1
            visited[(x,y)] = 2
        else:
            visited[(x,y)] = 3

        if render:
            if (img_index[0] % render) == 0:
                render_image(data, f'd3/frame{str(img_index[0] // render).zfill(4)}.png', visited)
            img_index[0] += 1

        x = (x + x_inc) % width
        y += y_inc
        if y >= height:
            return trees


f = 'd3.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = np.array([[c.strip() for c in line.strip('\n')] for line in file])

height = len(data)  # y
width = len(data[0])  # x

visited = {}
print(f'p1: {explore_trees(3, 1, 0)}')

visited = {}
img_index = [0]
things = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
ans = 1
for thing in things:
    ans *= explore_trees(thing[0], thing[1], 4)

print(f'p2: {ans}')
